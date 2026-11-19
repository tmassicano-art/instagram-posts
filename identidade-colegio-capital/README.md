# Identidade visual | Colégio de Presidentes da Capital

Padrão visual extraído da arte "The Veredict Experience | Júri Simulado", com o logo do Colégio de Presidentes da Capital (OAB SP). Vale para carrosséis, posts, páginas web e materiais impressos do Colégio.

## Cores

| Nome | Hex | Uso |
|---|---|---|
| Fundo | `#F2F2F2` | Fundo de todas as peças |
| Azul-marinho | `#0B2B49` | Títulos, caixas de informação, canto curvo |
| Azul profundo | `#0B2038` | Logo e textos longos |
| Dourado | `#D9A354` | Filetes, bordas das caixas, números, ícones, etiquetas |
| Branco | `#FAFAFA` | Texto dentro das caixas azuis |

## Tipografia

- **Títulos:** Playfair Display Black, sempre em caixa alta.
- **Subtítulos serifados:** Playfair Display Bold.
- **Texto e dados:** Montserrat Medium, Bold e ExtraBold.

As fontes estão em `fonts/` (licença SIL Open Font License).

## Elementos fixos

1. **Logo** "OAB São Paulo | Colégio de Presidentes da Capital" centralizado no topo, recolorido em azul-marinho (`img/logo-colegio-presidentes-navy.png`; versão branca para fundos escuros).
2. **Canto curvo** azul-marinho no alto à esquerda, com filete dourado acompanhando a curva.
3. **Filete dourado com "×" central** separando o título do conteúdo.
4. **Caixa azul com borda dourada e cantos arredondados** para as informações. Em listas, cada faixa traz um número dourado, uma divisória branca e o texto, separadas por filetes dourados.
5. **Rodapé:** filete dourado com setas apontando para a balança central, "COLÉGIO DE PRESIDENTES DA CAPITAL" e "JUNTOS, SOMOS MAIS FORTES!". Sem nome de pessoa na assinatura.

## Gerar um carrossel

```bash
python3 identidade-colegio-capital/render_colegio_capital.py roteiro.json -o 2026-WXX/NN --jpg
```

Tipos de card e campos:

| Tipo | Campos |
|---|---|
| `capa` | `chamada` (opcional, acima do título), `titulo`, `apoio` |
| `conteudo` | `etiqueta`, `titulo` e `texto` ou `itens` (3 a 4) |
| `destaque` | `numero` (opcional), `titulo`, `texto` |
| `cta` | `titulo`, `acoes` (3 linhas) |

Exemplo completo: `2026-W47/04/roteiro.json`.

## Observação

O logo foi recortado da imagem enviada (cerca de 360 px de largura no original, ampliado para 1074 px) e serve bem para os posts. Para impressão em formato grande, substitua os arquivos de `img/` pela versão vetorial oficial, mantendo os mesmos nomes.
