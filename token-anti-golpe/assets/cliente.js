/* Token Anti-Golpe | Colégio de Presidentes da Capital (OAB SP) */
(function () {
  "use strict";
  var T = window.Token;
  var CHAVE = "tag.cliente.v1";
  var dados = T.carregar(CHAVE, { vinculos: [] });
  if (!dados || !Array.isArray(dados.vinculos)) dados = { vinculos: [] };
  dados.vinculos = dados.vinculos.filter(function (v) { return v && T.idValido(v.id) && T.segredoValido(v.segredo); });
  var $ = function (id) { return document.getElementById(id); };
  var pendente = null;
  var ANEL = 2 * Math.PI * 24;

  if (!T.salvar("tag.teste", 1)) $("sem-armazenamento").classList.remove("oculto");

  function gravar() {
    if (!T.salvar(CHAVE, dados)) $("sem-armazenamento").classList.remove("oculto");
  }

  function limparEndereco() {
    try { history.replaceState(null, "", location.pathname); } catch (e) { location.hash = ""; }
  }

  // ------------------------------------------------ vínculo recebido

  function receber(texto) {
    var r = T.lerVinculo(texto);
    limparEndereco(); // tira o segredo da barra de endereço e do histórico na hora
    if (r.erro === "expirado") {
      alert("Este QR Code ou link expirou (vale " + T.VALIDADE_HORAS + " horas). Peça um novo ao seu advogado, pessoalmente ou em videochamada.");
      return true;
    }
    if (r.erro) return false;
    var v = r.vinculo;
    if (dados.vinculos.some(function (x) { return x.segredo === v.segredo; })) {
      alert("Este vínculo já está salvo neste celular.");
      return true;
    }
    var mesmaOab = dados.vinculos.filter(function (x) {
      return T.normalizarOab(x.oab) === T.normalizarOab(v.oab);
    });
    pendente = v;
    $("v-adv").textContent = v.advogado;
    $("v-oab").textContent = v.oab;
    $("v-cli").textContent = v.cliente ? "Cliente: " + v.cliente : "";
    $("v-validade").textContent = "QR Code gerado em " + new Date(v.criado * 1000).toLocaleString("pt-BR") + ".";
    $("v-duplicado").classList.toggle("oculto", !mesmaOab.length);
    $("b-confirmar").textContent = mesmaOab.length ? "Estou com o advogado agora, substituir" : "Confirmar vínculo";
    $("b-confirmar").classList.toggle("perigo", !!mesmaOab.length);
    $("tela-vinculo").classList.remove("oculto");
    $("tela-vinculo").scrollIntoView({ behavior: "smooth" });
    return true;
  }

  $("b-confirmar").addEventListener("click", function () {
    if (!pendente) return;
    var alvo = T.normalizarOab(pendente.oab);
    var substitui = dados.vinculos.some(function (x) { return T.normalizarOab(x.oab) === alvo; });
    if (substitui && !confirm("Você já tem um token desse advogado. Golpistas enviam novos QR Codes por mensagem justamente para trocar o seu token. Só continue se estiver frente a frente ou em videochamada com o seu advogado. Substituir?")) return;
    dados.vinculos = dados.vinculos.filter(function (x) { return T.normalizarOab(x.oab) !== alvo; });
    dados.vinculos.push({
      id: T.id(), advogado: pendente.advogado, oab: pendente.oab,
      cliente: pendente.cliente, segredo: pendente.segredo, criado: new Date().toISOString()
    });
    gravar();
    pendente = null;
    $("tela-vinculo").classList.add("oculto");
    desenhar();
    alert("Vínculo confirmado. Confira agora, junto com o advogado, se o código é igual nas duas telas.");
  });

  $("b-cancelar").addEventListener("click", function () {
    pendente = null;
    $("tela-vinculo").classList.add("oculto");
  });

  $("b-colar").addEventListener("click", function () {
    var txt = $("colar").value;
    $("colar").value = "";
    if (!receber(txt)) alert("Link inválido. Confira com o seu advogado.");
    return;
    $("colar").value = "";
  });

  // ------------------------------------------------ tokens

  function desenhar() {
    $("tela-vazia").classList.toggle("oculto", dados.vinculos.length > 0);
    $("lista").innerHTML = dados.vinculos.map(function (v) {
      return '<article class="token" data-id="' + v.id + '">' +
        '<div class="quem">Advogado(a) <b>' + T.esc(v.advogado) + '</b><br>' + T.esc(v.oab) + '</div>' +
        '<div class="linha"><div class="numero" data-codigo>··· ···</div>' +
        '<div class="tempo"><svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="24" fill="none" stroke="#24476b" stroke-width="5"/>' +
        '<circle data-anel cx="28" cy="28" r="24" fill="none" stroke="#d9a354" stroke-width="5" stroke-linecap="round" stroke-dasharray="' + ANEL + '"/></svg>' +
        '<span data-seg></span></div></div>' +
        '<form class="conferir" data-conferir>' +
        '<input inputmode="numeric" autocomplete="off" maxlength="7" placeholder="Código" aria-label="Código informado pelo advogado">' +
        '<button class="botao" type="submit">Conferir</button></form>' +
        '<div class="resultado" data-resultado></div>' +
        '<div class="rodape"><button class="botao secundario" type="button" data-excluir>Remover deste celular</button></div>' +
        '</article>';
    }).join("");
    tique(T.segundosRestantes());
  }

  function buscar(id) {
    for (var i = 0; i < dados.vinculos.length; i++) if (dados.vinculos[i].id === id) return dados.vinculos[i];
    return null;
  }

  function tique(restantes) {
    Array.prototype.forEach.call(document.querySelectorAll("#lista .token"), function (el) {
      var v = buscar(el.getAttribute("data-id"));
      if (!v) return;
      T.codigo(v.segredo).then(function (cod) {
        el.querySelector("[data-codigo]").textContent = T.formatar(cod);
      });
      var seg = el.querySelector("[data-seg]");
      seg.textContent = restantes;
      seg.classList.toggle("fim", restantes <= 5);
      el.querySelector("[data-anel]").setAttribute("stroke-dashoffset", ANEL * (1 - restantes / T.PERIODO));
    });
  }

  $("lista").addEventListener("submit", function (e) {
    var f = e.target.closest("[data-conferir]");
    if (!f) return;
    e.preventDefault();
    var el = f.closest(".token");
    var v = buscar(el.getAttribute("data-id"));
    var r = el.querySelector("[data-resultado]");
    T.confere(v.segredo, f.querySelector("input").value).then(function (ok) {
      r.className = "resultado " + (ok ? "ok" : "erro");
      r.textContent = ok
        ? "Código confere. O contato é de " + v.advogado + "."
        : "Código NÃO confere. Encerre o contato e ligue para o escritório pelo número que você já conhecia.";
      f.querySelector("input").value = "";
      clearTimeout(r._t);
      r._t = setTimeout(function () { r.className = "resultado"; }, 60000);
    });
  });

  $("lista").addEventListener("click", function (e) {
    if (!e.target.closest("[data-excluir]")) return;
    var v = buscar(e.target.closest(".token").getAttribute("data-id"));
    if (v && confirm("Remover o token de " + v.advogado + " deste celular? Para voltar a usar, será preciso um novo vínculo com o advogado.")) {
      dados.vinculos = dados.vinculos.filter(function (x) { return x.id !== v.id; });
      gravar();
      desenhar();
    }
  });

  // ------------------------------------------------ início

  desenhar();
  if (location.hash) receber(location.hash);
  window.addEventListener("hashchange", function () { if (location.hash) receber(location.hash); });
  T.relogio(tique);
})();
