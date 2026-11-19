# Token Anti-Golpe | Colégio de Presidentes da Capital

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
- Tudo fica no `localStorage` de cada aparelho. Não há servidor, banco de dados nem coleta de dados pessoais.
- A conferência aceita a janela atual e as vizinhas (até 30 segundos de diferença), porque o código é dito em voz alta e os relógios variam.

## Proteções contra o golpe do falso advogado

| Ataque | Proteção |
|---|---|
| Golpista conhece nome, foto e processo do advogado | O código depende de uma chave que só existe nos aparelhos do advogado e do cliente |
| Golpista pede ao cliente que leia o código e o repete | Regra de ouro em todas as telas: quem diz o código é o advogado, o cliente só confere |
| Golpista cria um token com o nome do advogado e manda o link por mensagem | Aviso forte quando o cliente já tem token daquela OAB (compara o número normalizado); o botão vira "substituir" e pede confirmação; a tela de vínculo orienta a cancelar link recebido por mensagem |
| Foto ou encaminhamento do QR Code depois da entrega | O link de vínculo expira em 72 horas |
| Chave esquecida na barra de endereço ou no histórico | O link é apagado do endereço assim que a página abre |
| Script de terceiro (analytics, pixel) lendo a chave | Política de segurança (CSP) que só aceita scripts do próprio site e bloqueia qualquer conexão de rede (`connect-src 'none'`) |
| Arquivo de cópia de segurança adulterado | Validação de cada campo na restauração; nomes sempre exibidos como texto |
| Página embutida em site falso (clickjacking) | `frame-ancestors 'none'` e `X-Frame-Options: DENY` no `.htaccess` |

O que o token **não** resolve sozinho: se o cliente ignorar os avisos e aceitar um QR Code enviado pelo golpista, ou se o aparelho do advogado for invadido. Por isso a entrega deve ser presencial ou por videochamada, e o painel deve ficar em computador protegido por senha.

## Testes

Os cenários abaixo foram verificados num navegador Chromium automatizado:
- os códigos são iguais no advogado e no cliente, e o código certo confere e o errado não;
- o cálculo bate com os vetores oficiais da RFC 6238;
- o link expirado é recusado, e o link some da barra de endereço antes da confirmação;
- o alerta de duplicidade aparece para a mesma OAB escrita de outro jeito, e o token original continua igual após cancelar;
- a restauração descarta registro adulterado e mostra HTML como texto;
- a CSP bloqueia conexões de rede;
- não há rolagem horizontal no celular.

## Publicar

São arquivos estáticos e não exigem servidor de aplicação. Qualquer hospedagem com HTTPS serve: GitHub Pages, Netlify, Cloudflare Pages ou o site institucional. HTTPS é obrigatório, porque o navegador só libera a criptografia (`crypto.subtle`) em conexão segura.

Passo a passo completo em `INSTALACAO.md`.

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

## Antes de divulgar como serviço do Colégio

- Aprovação do Colégio de Presidentes e, se for o caso, ciência da Seccional (OAB SP).
- Domínio institucional para hospedar as páginas.
- Revisão de LGPD (a ferramenta não coleta dados, mas a política de privacidade deve dizer isso).
- Um contato oficial do Colégio para dúvidas, a incluir no rodapé de `index.html`.

## Licenças

`assets/qrcode.js`: QR Code Generator for JavaScript, Kazuhiko Arase, licença MIT.

## Identidade visual

As páginas seguem a identidade do Colégio de Presidentes da Capital descrita em `../identidade-colegio-capital/README.md`: fundo claro, azul-marinho `#0B2B49`, dourado `#D9A354`, Playfair Display nos títulos e Montserrat no texto. Fontes e logo ficam em `assets/` para as páginas funcionarem sem depender de serviços externos.
