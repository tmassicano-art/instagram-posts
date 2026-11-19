/*
 * Token Anti-Golpe | Colégio de Presidentes da Capital (OAB SP)
 * Núcleo comum: TOTP (RFC 6238, HMAC-SHA1, 6 dígitos, 30 segundos),
 * base32, links de vínculo e armazenamento local.
 *
 * Nada aqui envia dados pela rede. O segredo de cada vínculo fica apenas
 * no aparelho do advogado e no aparelho do cliente.
 */
(function (global) {
  "use strict";

  var PERIODO = 30;
  var DIGITOS = 6;
  var EMISSOR = "OAB SP Colégio da Capital";
  var B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

  // ------------------------------------------------------------ base32

  function b32enc(bytes) {
    var bits = 0, val = 0, out = "";
    for (var i = 0; i < bytes.length; i++) {
      val = (val << 8) | bytes[i];
      bits += 8;
      while (bits >= 5) {
        out += B32[(val >>> (bits - 5)) & 31];
        bits -= 5;
      }
    }
    if (bits > 0) out += B32[(val << (5 - bits)) & 31];
    return out;
  }

  function b32dec(texto) {
    var s = String(texto).toUpperCase().replace(/[^A-Z2-7]/g, "");
    var bits = 0, val = 0, out = [];
    for (var i = 0; i < s.length; i++) {
      val = (val << 5) | B32.indexOf(s[i]);
      bits += 5;
      if (bits >= 8) {
        out.push((val >>> (bits - 8)) & 255);
        bits -= 8;
      }
    }
    return new Uint8Array(out);
  }

  function novoSegredo() {
    return b32enc(crypto.getRandomValues(new Uint8Array(20)));
  }

  function segredoValido(s) {
    return typeof s === "string" && /^[A-Z2-7]{16,}$/.test(s.toUpperCase().replace(/\s/g, ""));
  }

  // ------------------------------------------------------------ TOTP

  var _chaves = {};

  function chave(segredo) {
    if (!_chaves[segredo]) {
      _chaves[segredo] = crypto.subtle.importKey(
        "raw", b32dec(segredo), { name: "HMAC", hash: "SHA-1" }, false, ["sign"]
      );
    }
    return _chaves[segredo];
  }

  function hotp(segredo, contador) {
    var msg = new Uint8Array(8);
    var alto = Math.floor(contador / 4294967296);
    var baixo = contador >>> 0;
    for (var i = 3; i >= 0; i--) { msg[i] = alto & 255; alto = alto >>> 8; }
    for (var j = 7; j >= 4; j--) { msg[j] = baixo & 255; baixo = baixo >>> 8; }
    return chave(segredo).then(function (k) {
      return crypto.subtle.sign("HMAC", k, msg);
    }).then(function (sig) {
      var h = new Uint8Array(sig);
      var o = h[h.length - 1] & 15;
      var bin = ((h[o] & 127) << 24) | (h[o + 1] << 16) | (h[o + 2] << 8) | h[o + 3];
      var cod = String(bin % Math.pow(10, DIGITOS));
      while (cod.length < DIGITOS) cod = "0" + cod;
      return cod;
    });
  }

  function contadorAgora(ms) {
    return Math.floor((ms === undefined ? Date.now() : ms) / 1000 / PERIODO);
  }

  function codigo(segredo, ms) {
    return hotp(segredo, contadorAgora(ms));
  }

  function segundosRestantes(ms) {
    var t = (ms === undefined ? Date.now() : ms) / 1000;
    return PERIODO - Math.floor(t % PERIODO);
  }

  /* Aceita a janela atual e as vizinhas (90 segundos no total), porque o
     código é lido em voz alta e o relógio dos aparelhos nunca é idêntico. */
  function confere(segredo, digitado, ms) {
    var alvo = String(digitado).replace(/\D/g, "");
    if (alvo.length !== DIGITOS) return Promise.resolve(false);
    var c = contadorAgora(ms);
    return Promise.all([hotp(segredo, c - 1), hotp(segredo, c), hotp(segredo, c + 1)])
      .then(function (lista) { return lista.indexOf(alvo) !== -1; });
  }

  function formatar(cod) {
    return cod.slice(0, 3) + " " + cod.slice(3);
  }

  // ------------------------------------------------------------ vínculo

  function b64url(txt) {
    var bytes = new TextEncoder().encode(txt);
    var bin = "";
    for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
    return btoa(bin).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function deb64url(s) {
    s = s.replace(/-/g, "+").replace(/_/g, "/");
    while (s.length % 4) s += "=";
    var bin = atob(s);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }

  /* O segredo vai no fragmento (#) do link, que o navegador nunca envia
     ao servidor que hospeda as páginas. O link vale por VALIDADE_HORAS:
     um QR Code fotografado ou encaminhado depois disso não cria vínculo. */
  var VALIDADE_HORAS = 72;

  function linkVinculo(perfil, cliente, agoraMs) {
    var dados = {
      v: 2, a: perfil.nome, o: perfil.oab, c: cliente.nome, s: cliente.segredo,
      t: Math.floor((agoraMs === undefined ? Date.now() : agoraMs) / 1000)
    };
    var url = new URL("cliente.html", global.location.href);
    url.search = "";
    url.hash = "v=" + b64url(JSON.stringify(dados));
    return url.toString();
  }

  function validadeAte(criadoSeg) {
    return new Date((criadoSeg + VALIDADE_HORAS * 3600) * 1000);
  }

  /* Devolve {vinculo} ou {erro: "invalido" | "expirado"}. */
  function lerVinculo(texto, agoraMs) {
    var d;
    try {
      var m = String(texto).match(/[#&]v=([A-Za-z0-9_-]+)/);
      if (!m) return { erro: "invalido" };
      d = JSON.parse(deb64url(m[1]));
    } catch (e) {
      return { erro: "invalido" };
    }
    if (!d || d.v !== 2 || !segredoValido(d.s) || typeof d.a !== "string" || typeof d.o !== "string" ||
        !d.a.trim() || !d.o.trim() || typeof d.t !== "number") {
      return { erro: "invalido" };
    }
    var agora = (agoraMs === undefined ? Date.now() : agoraMs) / 1000;
    if (agora - d.t > VALIDADE_HORAS * 3600 || d.t - agora > 3600) {
      return { erro: "expirado", validade: validadeAte(d.t) };
    }
    return {
      vinculo: {
        advogado: d.a.slice(0, 80), oab: d.o.slice(0, 30), cliente: String(d.c || "").slice(0, 80),
        segredo: d.s.toUpperCase().replace(/\s/g, ""), criado: d.t
      }
    };
  }

  /* "OAB/SP 123.456" e "123456 SP" viram "SP123456", para comparar inscrições. */
  function normalizarOab(oab) {
    var s = String(oab).toUpperCase();
    var uf = (s.match(/\b(AC|AL|AP|AM|BA|CE|DF|ES|GO|MA|MT|MS|MG|PA|PB|PR|PE|PI|RJ|RN|RS|RO|RR|SC|SP|SE|TO)\b/) || [""])[0];
    var num = s.replace(/\D/g, "").replace(/^0+/, "");
    return uf + num;
  }

  function uriAutenticador(perfil, cliente) {
    var rotulo = EMISSOR + ":" + perfil.nome + " (" + perfil.oab + ")";
    return "otpauth://totp/" + encodeURIComponent(rotulo) +
      "?secret=" + cliente.segredo +
      "&issuer=" + encodeURIComponent(EMISSOR) +
      "&algorithm=SHA1&digits=" + DIGITOS + "&period=" + PERIODO;
  }

  // ------------------------------------------------------------ armazenamento

  function carregar(nome, padrao) {
    try {
      var bruto = global.localStorage.getItem(nome);
      return bruto ? JSON.parse(bruto) : padrao;
    } catch (e) {
      return padrao;
    }
  }

  function salvar(nome, valor) {
    try {
      global.localStorage.setItem(nome, JSON.stringify(valor));
      return true;
    } catch (e) {
      return false;
    }
  }

  function idValido(x) {
    return typeof x === "string" && /^[A-Z2-7]{4,16}$/.test(x);
  }

  function id() {
    return b32enc(crypto.getRandomValues(new Uint8Array(5)));
  }

  // ------------------------------------------------------------ interface

  function qrSvg(texto, celula) {
    var qr = global.qrcode(0, "M");
    qr.addData(texto, "Byte");
    qr.make();
    return qr.createSvgTag({ cellSize: celula || 5, margin: 4, scalable: true });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* Chama fn a cada virada de segundo; fn recebe os segundos restantes. */
  function relogio(fn) {
    var ultimo = -1;
    function tique() {
      var r = segundosRestantes();
      if (r !== ultimo) { ultimo = r; fn(r); }
    }
    tique();
    return setInterval(tique, 250);
  }

  global.Token = {
    PERIODO: PERIODO,
    DIGITOS: DIGITOS,
    EMISSOR: EMISSOR,
    b32enc: b32enc,
    b32dec: b32dec,
    novoSegredo: novoSegredo,
    segredoValido: segredoValido,
    hotp: hotp,
    codigo: codigo,
    confere: confere,
    formatar: formatar,
    segundosRestantes: segundosRestantes,
    VALIDADE_HORAS: VALIDADE_HORAS,
    linkVinculo: linkVinculo,
    lerVinculo: lerVinculo,
    validadeAte: validadeAte,
    normalizarOab: normalizarOab,
    idValido: idValido,
    uriAutenticador: uriAutenticador,
    carregar: carregar,
    salvar: salvar,
    id: id,
    qrSvg: qrSvg,
    esc: esc,
    relogio: relogio
  };
})(typeof window !== "undefined" ? window : globalThis);
