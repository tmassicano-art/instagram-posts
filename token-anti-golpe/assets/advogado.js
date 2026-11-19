/* Token Anti-Golpe | Colégio de Presidentes da Capital (OAB SP) */
(function () {
  "use strict";
  var T = window.Token;
  var CHAVE = "tag.advogado.v1";
  var dados = T.carregar(CHAVE, { perfil: null, clientes: [] });
  if (!dados || !Array.isArray(dados.clientes)) dados = { perfil: null, clientes: [] };
  dados.clientes = dados.clientes.filter(function (c) { return c && T.idValido(c.id) && T.segredoValido(c.segredo); });
  var $ = function (id) { return document.getElementById(id); };
  var atual = null, abaAtual = "link";

  if (!T.salvar("tag.teste", 1)) $("sem-armazenamento").classList.remove("oculto");

  function gravar() {
    if (!T.salvar(CHAVE, dados)) $("sem-armazenamento").classList.remove("oculto");
  }

  // ------------------------------------------------ telas

  function mostrar() {
    var temPerfil = !!(dados.perfil && dados.perfil.nome);
    $("tela-perfil").classList.toggle("oculto", temPerfil);
    $("tela-painel").classList.toggle("oculto", !temPerfil);
    if (temPerfil) {
      $("saudacao").textContent = dados.perfil.nome + " · " + dados.perfil.oab;
      desenharLista();
    }
  }

  $("form-perfil").addEventListener("submit", function (e) {
    e.preventDefault();
    dados.perfil = { nome: $("p-nome").value.trim(), oab: $("p-oab").value.trim() };
    gravar();
    mostrar();
  });

  $("b-perfil").addEventListener("click", function () {
    $("p-nome").value = dados.perfil.nome;
    $("p-oab").value = dados.perfil.oab;
    $("tela-perfil").classList.remove("oculto");
    $("tela-painel").classList.add("oculto");
    if (dados.clientes.length) {
      alert("Atenção: os clientes já vinculados continuarão vendo o nome antigo até receberem um novo vínculo.");
    }
  });

  // ------------------------------------------------ lista

  var ANEL = 2 * Math.PI * 24;

  function desenharLista() {
    var termo = $("busca").value.trim().toLowerCase();
    var lista = dados.clientes
      .filter(function (c) { return !termo || c.nome.toLowerCase().indexOf(termo) !== -1; })
      .sort(function (a, b) { return a.nome.localeCompare(b.nome, "pt-BR"); });

    if (!dados.clientes.length) {
      $("lista").innerHTML = '<div class="cartao vazio">Nenhum cliente cadastrado ainda.<br>Clique em <b>Novo cliente</b> para criar o primeiro vínculo.</div>';
      return;
    }
    if (!lista.length) {
      $("lista").innerHTML = '<div class="cartao vazio">Nenhum cliente encontrado.</div>';
      return;
    }
    $("lista").innerHTML = lista.map(function (c) {
      return '<article class="token" data-id="' + c.id + '">' +
        '<div class="quem">Cliente <b>' + T.esc(c.nome) + '</b></div>' +
        '<div class="linha"><div class="numero" data-codigo>··· ···</div>' +
        '<div class="tempo"><svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="24" fill="none" stroke="#24476b" stroke-width="5"/>' +
        '<circle data-anel cx="28" cy="28" r="24" fill="none" stroke="#d9a354" stroke-width="5" stroke-linecap="round" stroke-dasharray="' + ANEL + '"/></svg>' +
        '<span data-seg></span></div></div>' +
        '<div class="rodape">' +
        '<button class="botao secundario" type="button" data-acao="qr">Entregar ao cliente</button>' +
        '<button class="botao secundario" type="button" data-acao="excluir">Excluir</button>' +
        '</div></article>';
    }).join("");
    atualizarCodigos(T.segundosRestantes());
  }

  function atualizarCodigos(restantes) {
    var cartoes = document.querySelectorAll("#lista .token");
    Array.prototype.forEach.call(cartoes, function (el) {
      var c = buscar(el.getAttribute("data-id"));
      if (!c) return;
      T.codigo(c.segredo).then(function (cod) {
        el.querySelector("[data-codigo]").textContent = T.formatar(cod);
      });
      var seg = el.querySelector("[data-seg]");
      seg.textContent = restantes;
      seg.classList.toggle("fim", restantes <= 5);
      el.querySelector("[data-anel]").setAttribute("stroke-dashoffset", ANEL * (1 - restantes / T.PERIODO));
    });
  }

  function buscar(id) {
    for (var i = 0; i < dados.clientes.length; i++) if (dados.clientes[i].id === id) return dados.clientes[i];
    return null;
  }

  $("busca").addEventListener("input", desenharLista);

  $("lista").addEventListener("click", function (e) {
    var b = e.target.closest("[data-acao]");
    if (!b) return;
    var c = buscar(b.closest(".token").getAttribute("data-id"));
    if (!c) return;
    if (b.getAttribute("data-acao") === "qr") abrirQr(c);
    if (b.getAttribute("data-acao") === "excluir") {
      if (confirm("Excluir o vínculo de " + c.nome + "? O código deixa de existir neste aparelho e o cliente precisará de um novo vínculo.")) {
        dados.clientes = dados.clientes.filter(function (x) { return x.id !== c.id; });
        gravar();
        desenharLista();
      }
    }
  });

  // ------------------------------------------------ novo cliente

  $("b-novo").addEventListener("click", function () {
    $("n-nome").value = "";
    $("d-novo").showModal();
    $("n-nome").focus();
  });

  $("form-novo").addEventListener("submit", function (e) {
    e.preventDefault();
    var nome = $("n-nome").value.trim();
    if (!nome) return;
    var c = { id: T.id(), nome: nome, segredo: T.novoSegredo(), criado: new Date().toISOString() };
    dados.clientes.push(c);
    gravar();
    $("d-novo").close();
    $("busca").value = "";
    desenharLista();
    abrirQr(c);
  });

  Array.prototype.forEach.call(document.querySelectorAll("[data-fechar]"), function (b) {
    b.addEventListener("click", function () { b.closest("dialog").close(); });
  });

  // ------------------------------------------------ QR e entrega

  function abrirQr(c) {
    atual = c;
    abaAtual = "link";
    $("qr-titulo").textContent = "Entregar a " + c.nome;
    desenharQr();
    $("d-qr").showModal();
  }

  function desenharQr() {
    var link = abaAtual === "link";
    $("aba-link").className = "botao" + (link ? "" : " secundario");
    $("aba-app").className = "botao" + (link ? " secundario" : "");
    $("qr-explica").textContent = link
      ? "Peça ao cliente para apontar a câmera do celular, abrir o link e tocar em Confirmar vínculo. Depois confiram juntos se o código é o mesmo nas duas telas."
      : "Para quem usa Google Authenticator ou Microsoft Authenticator: no aplicativo, toque em adicionar conta e escaneie este QR Code.";
    var conteudo = link ? T.linkVinculo(dados.perfil, atual) : T.uriAutenticador(dados.perfil, atual);
    $("qr-img").innerHTML = T.qrSvg(conteudo, 5);
    $("b-copiar").classList.toggle("oculto", !link);
  }

  $("aba-link").addEventListener("click", function () { abaAtual = "link"; desenharQr(); });
  $("aba-app").addEventListener("click", function () { abaAtual = "app"; desenharQr(); });

  $("b-copiar").addEventListener("click", function () {
    var link = T.linkVinculo(dados.perfil, atual);
    if (!confirm("O link dá acesso ao código deste cliente. Copie apenas para enviar a quem você confirmou ser o cliente. Continuar?")) return;
    (navigator.clipboard ? navigator.clipboard.writeText(link) : Promise.reject())
      .then(function () { alert("Link copiado."); })
      .catch(function () { prompt("Copie o link:", link); });
  });

  $("b-imprimir").addEventListener("click", function () {
    var p = dados.perfil;
    $("folha").innerHTML =
      '<h1>Token Anti-Golpe</h1>' +
      '<p>Iniciativa do Colégio de Presidentes da Capital, OAB SP</p>' +
      '<div class="caixa"><b>Seu advogado:</b> ' + T.esc(p.nome) + ' (' + T.esc(p.oab) + ')<br><b>Cliente:</b> ' + T.esc(atual.nome) + '</div>' +
      '<div class="qr">' + T.qrSvg(T.linkVinculo(p, atual), 4) + '</div>' +
      '<p class="centro"><b>Válido até ' + T.esc(T.validadeAte(Math.floor(Date.now() / 1000)).toLocaleString("pt-BR")) + '.</b> Depois disso, peça um novo ao advogado.</p>' +
      '<p class="centro">Aponte a câmera do celular para o código acima e toque em <b>Confirmar vínculo</b>.</p>' +
      '<h2>Como se proteger</h2>' +
      '<ol class="passos">' +
      '<li>Sempre que alguém falar em seu nome sobre pagamento, valores, documentos ou conta bancária, abra o token no celular.</li>' +
      '<li>Peça: "qual é o código?". Quem informa o código é o advogado.</li>' +
      '<li>Compare com o número da sua tela. Igual: pode seguir. Diferente: encerre o contato.</li>' +
      '<li>Nunca leia o seu código para ninguém, nem aceite novo QR Code ou link enviado por mensagem.</li>' +
      '<li>Na dúvida, ligue para o escritório pelo número que você já conhecia.</li>' +
      '</ol>' +
      '<div class="caixa"><b>Guarde esta folha em local seguro.</b> Quem tiver o QR Code consegue gerar o seu código. Depois de vincular o celular, você pode rasgá-la.</div>';
    window.print();
  });

  // ------------------------------------------------ cópia de segurança

  $("b-backup").addEventListener("click", function () {
    var blob = new Blob([JSON.stringify({ tipo: "token-anti-golpe-colegio-capital", versao: 1, gerado: new Date().toISOString(), dados: dados }, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "token-anti-golpe-copia-" + new Date().toISOString().slice(0, 10) + ".json";
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
    alert("Cópia baixada. Este arquivo contém as chaves dos seus clientes: guarde com o mesmo cuidado de uma senha.");
  });

  $("b-restaurar").addEventListener("click", function () { $("arquivo").click(); });

  $("arquivo").addEventListener("change", function () {
    var f = this.files && this.files[0];
    this.value = "";
    if (!f) return;
    f.text().then(function (txt) {
      var j = JSON.parse(txt);
      if (!j || ["token-anti-golpe-colegio-capital", "token-anti-golpe-oab-tatuape"].indexOf(j.tipo) === -1 || !j.dados || !Array.isArray(j.dados.clientes)) throw new Error();
      var novos = j.dados.clientes.filter(function (c) {
        return c && T.idValido(c.id) && typeof c.nome === "string" && c.nome.trim() &&
          T.segredoValido(c.segredo) && !buscar(c.id);
      }).map(function (c) {
        return { id: c.id, nome: c.nome.trim().slice(0, 80), segredo: c.segredo.toUpperCase().replace(/\s/g, ""),
                 criado: String(c.criado || "").slice(0, 40) };
      });
      if (!confirm("Restaurar " + novos.length + " cliente(s) desta cópia? Os clientes já existentes neste aparelho são mantidos.")) return;
      dados.clientes = dados.clientes.concat(novos);
      var p = j.dados.perfil;
      if (!dados.perfil && p && typeof p.nome === "string" && typeof p.oab === "string") {
        dados.perfil = { nome: p.nome.trim().slice(0, 80), oab: p.oab.trim().slice(0, 30) };
      }
      gravar();
      mostrar();
    }).catch(function () {
      alert("Arquivo inválido. Escolha uma cópia de segurança gerada por este painel.");
    });
  });

  // ------------------------------------------------ início

  mostrar();
  T.relogio(atualizarCodigos);
})();
