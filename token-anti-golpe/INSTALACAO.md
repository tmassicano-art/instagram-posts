# Token Anti-Golpe | Guia de instalação no site

Colégio de Presidentes da Capital (OAB SP)

Este guia é para quem administra o site. A instalação leva cerca de 15 minutos e não exige programação, banco de dados nem servidor de aplicação.

## 1. O que vai no pacote

Pasta `token-anti-golpe/`, que deve ser publicada inteira, sem alterar a estrutura:

| Arquivo | Função |
|---|---|
| `index.html` | Página de apresentação, passo a passo e perguntas frequentes |
| `advogado.html` | Painel do advogado (cadastro de clientes, QR Code, códigos) |
| `cliente.html` | Token do cliente (código e conferência) |
| `manifest.webmanifest`, `sw.js` | Permitem instalar o token na tela do celular e abrir sem internet |
| `.htaccess` | Cabeçalhos de segurança para servidores Apache (arquivo oculto: confira se foi enviado) |
| `assets/` | Estilos, scripts, fontes, logo e ícones |
| `README.md` | Como o sistema funciona por dentro |

## 2. Requisitos

- **HTTPS obrigatório.** Sem HTTPS o navegador bloqueia a criptografia e o código não aparece.
- Hospedagem de arquivos estáticos (qualquer hospedagem de site serve: Apache, Nginx, IIS, Netlify, Cloudflare Pages, GitHub Pages).
- Nenhum banco de dados, PHP ou cadastro de usuários.

## 3. Passo a passo

1. Descompacte `token-anti-golpe.zip`.
2. Envie a pasta `token-anti-golpe` para o servidor do site (FTP, painel da hospedagem ou gerenciador de arquivos), por exemplo em `https://SEU-SITE/token/`.
   - Pode renomear a pasta. Não renomeie os arquivos internos.
   - Ative "mostrar arquivos ocultos" no programa de FTP para enviar o `.htaccess`.
3. Abra `https://SEU-SITE/token/` no navegador e confira se aparece a página com o logo do Colégio.
4. Faça o teste da seção 6.
5. Divulgue o endereço: no link da bio do Instagram, no site e na comunicação com a advocacia.

**Use um endereço próprio do Colégio ou da OAB SP.** Divulgue sempre o mesmo endereço oficial, para que golpistas não consigam se passar pela ferramenta com um site parecido.

## 4. Regras que não podem ser quebradas

- **Não inclua nessas páginas** Google Analytics, Tag Manager, pixel do Facebook, chat, banner de cookies de terceiros ou qualquer outro script externo. O link de vínculo carrega a chave do cliente, e um script de terceiro poderia lê-la. As páginas já trazem uma política de segurança (CSP) que bloqueia esses scripts. Não a remova.
- **Não coloque as páginas dentro de um iframe** do site principal. Linke para elas diretamente.
- **Não edite** `assets/token.js`, que contém o cálculo do código.

## 5. Cabeçalhos de segurança no servidor

As páginas já trazem as proteções principais por conta própria. Os cabeçalhos abaixo reforçam essa proteção.

**Apache:** o arquivo `.htaccess` do pacote já faz tudo. Basta que ele esteja na pasta.

**Nginx:** peça ao responsável pelo servidor para incluir no bloco `location` da pasta:

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; font-src 'self'; connect-src 'none'; worker-src 'self'; manifest-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer" always;
add_header X-Frame-Options "DENY" always;
location ~ (sw\.js|\.html|\.webmanifest)$ { add_header Cache-Control "no-cache"; }
types { application/manifest+json webmanifest; }
```

**Netlify / Cloudflare Pages:** crie um arquivo `_headers` na pasta com as mesmas linhas do `.htaccess`, no formato da plataforma.

## 6. Teste antes de divulgar

Use dois aparelhos (um computador e um celular, por exemplo).

1. No computador, abra `advogado.html`, cadastre um nome e uma OAB de teste e crie um cliente "Teste".
2. No celular, escaneie o QR Code com a câmera e toque em **Confirmar vínculo**.
3. Confira se o código de 6 dígitos é igual nas duas telas e muda a cada 30 segundos.
4. No celular, digite o código no campo **Conferir**: deve aparecer "Código confere".
5. Digite 000000: deve aparecer "Código NÃO confere".
6. No celular, use "Adicionar à tela inicial" e abra o ícone com o modo avião ligado: o código deve continuar aparecendo.
7. Ao terminar, exclua o cliente de teste no painel e remova o token do celular.

## 7. Atualizações futuras

Ao publicar uma versão nova dos arquivos, abra `sw.js` e troque `token-anti-golpe-v1` por `token-anti-golpe-v2` (e assim por diante). Isso faz os celulares baixarem a versão nova.

## 8. O que comunicar à advocacia

- O token é gratuito e não coleta dados: tudo fica no aparelho do advogado e no do cliente.
- O advogado deve fazer a **cópia de segurança** do painel com frequência e guardá-la como uma senha.
- O QR Code deve ser entregue **pessoalmente ou em videochamada** e vale por 72 horas.
- **Regra de ouro:** quem diz o código é o advogado. O cliente só confere e nunca lê o próprio código para ninguém.
- Se o cliente receber "do advogado" um novo QR Code por mensagem, não deve confirmar. O sistema avisa quando ele já tem token daquela OAB.

## 9. Antes de divulgar oficialmente

- Aprovação do Colégio de Presidentes e ciência da OAB SP.
- Endereço oficial definido (seção 3).
- Política de privacidade mencionando que a ferramenta não coleta dados.
- Contato oficial para dúvidas, a incluir no rodapé de `index.html`.
