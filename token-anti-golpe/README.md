# Token Anti-Golpe | OAB Tatuapé

Ferramenta gratuita para o cliente confirmar que um contato vem mesmo do seu advogado, por meio de um código de 6 dígitos que muda a cada 30 segundos.

## Páginas

| Arquivo | Para quem | O que faz |
|---|---|---|
| `index.html` | Público | Apresentação, como funciona, passo a passo para advogados e clientes, perguntas frequentes |
| `advogado.html` | Advogado | Cadastro do perfil, criação de vínculo por cliente, QR Code de entrega, folha impressa de instruções, códigos ao vivo, cópia de segurança |
| `cliente.html` | Cliente | Confirmação do vínculo, código ao vivo e campo "Conferir código" |

## Como funciona por dentro

- Cada vínculo advogado–cliente tem uma chave secreta aleatória de 160 bits, gerada no navegador do advogado.
- O código segue o padrão TOTP (RFC 6238: HMAC-SHA1, 6 dígitos, 30 segundos), o mesmo do Google Authenticator e do Microsoft Authenticator. Por isso o cliente pode usar a página `cliente.html` ou um desses aplicativos.
- A chave chega ao cliente pelo QR Code. No link, ela fica depois do `#`, parte que o navegador não envia ao servidor de hospedagem.
- Tudo fica no `localStorage` de cada aparelho. Não há servidor, banco de dados nem coleta de dados pessoais. O código é calculado no próprio aparelho.
- A conferência aceita a janela atual e as vizinhas (até 30 segundos de diferença), porque o código é dito em voz alta e os relógios variam.

## Publicar

São arquivos estáticos e não exigem servidor de aplicação. Qualquer hospedagem com HTTPS serve: GitHub Pages, Netlify, Cloudflare Pages ou o próprio site da Subseção. HTTPS é obrigatório, porque o navegador só libera a criptografia (`crypto.subtle`) em conexão segura.

Para testar no computador:

```bash
cd token-anti-golpe
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Limites que precisam ser comunicados

- Se o cliente trocar de celular ou apagar os dados do navegador, o vínculo se perde e precisa ser refeito com o advogado.
- O advogado deve fazer a cópia de segurança do painel. O arquivo contém as chaves dos clientes e deve ser guardado como uma senha.
- A proteção depende da regra de ouro: quem diz o código é o advogado, e o cliente nunca lê o próprio código para ninguém. Sem isso, um golpista pode pedir o código ao cliente e repeti-lo.

## Antes de divulgar como serviço da Subseção

- Aprovação da diretoria da Subseção e, se for o caso, ciência da Seccional (OAB SP).
- Domínio institucional para hospedar as páginas.
- Revisão de LGPD (a ferramenta não coleta dados, mas a política de privacidade deve dizer isso).
- Um contato oficial da Subseção para dúvidas, a incluir no rodapé de `index.html`.

## Licenças

`assets/qrcode.js`: QR Code Generator for JavaScript, Kazuhiko Arase, licença MIT.

## Identidade visual

As páginas seguem a identidade da OAB Tatuapé descrita em `../identidade-oab-tatuape/README.md`: fundo claro, azul-marinho `#0B2B49`, dourado `#D9A354`, Playfair Display nos títulos e Montserrat no texto. Fontes e logo ficam em `assets/` para as páginas funcionarem sem depender de serviços externos.
