/* Token Anti-Golpe: guarda as páginas no aparelho para abrir sem internet.
   Ao publicar uma nova versão, aumente VERSAO para renovar o cache. */
var VERSAO = "token-anti-golpe-v1";
var ARQUIVOS = [
  "./", "index.html", "advogado.html", "cliente.html", "manifest.webmanifest",
  "assets/app.css", "assets/token.js", "assets/qrcode.js", "assets/advogado.js", "assets/cliente.js", "assets/pwa.js",
  "assets/img/logo-colegio-presidentes-navy.png", "assets/img/icone-192.png", "assets/img/icone-512.png",
  "assets/fonts/PlayfairDisplay-Black.woff2", "assets/fonts/PlayfairDisplay-Bold.woff2",
  "assets/fonts/Montserrat-Medium.woff2", "assets/fonts/Montserrat-Bold.woff2", "assets/fonts/Montserrat-ExtraBold.woff2"
];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSAO).then(function (c) { return c.addAll(ARQUIVOS); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (nomes) {
    return Promise.all(nomes.filter(function (n) { return n !== VERSAO; }).map(function (n) { return caches.delete(n); }));
  }).then(function () { return self.clients.claim(); }));
});

/* Rede primeiro (para receber atualizações), cache se estiver sem internet.
   O fragmento # do link de vínculo nunca chega aqui. */
self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET" || new URL(e.request.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(e.request).then(function (r) {
      if (r.ok) { var copia = r.clone(); caches.open(VERSAO).then(function (c) { c.put(e.request, copia); }); }
      return r;
    }).catch(function () {
      return caches.match(e.request, { ignoreSearch: true });
    })
  );
});
