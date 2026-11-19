# Identidade visual | OAB Tatuapé

Padrão extraído da arte de referência da Subseção ("The Veredict Experience | Júri Simulado"). Vale para carrosséis, posts, páginas web e materiais impressos da OAB Tatuapé.

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

1. **Logo** "OAB São Paulo | Subseção Tatuapé" centralizado no topo (`img/`, versões azul e branca).
2. **Canto curvo** azul-marinho no alto à esquerda, com filete dourado acompanhando a curva.
3. **Filete dourado com "×" central** separando o título do conteúdo.
4. **Caixa azul com borda dourada e cantos arredondados** para as informações. Em listas, cada faixa traz um número dourado, uma divisória branca e o texto, separadas por filetes dourados.
5. **Rodapé:** filete dourado com setas apontando para a balança central, "OAB TATUAPÉ" e "JUNTOS, SOMOS MAIS FORTES!". Na capa e no card final entra também "Presidente OAB Tatuapé: Thiago Massicano".

## Gerar um carrossel

```bash
python3 identidade-oab-tatuape/render_oab_tatuape.py roteiro.json -o 2026-WXX/NN --jpg
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

O logo foi recortado da arte de referência (493 px de largura) e serve bem para os posts. Para impressão em formato grande, substitua os arquivos de `img/` pela versão vetorial oficial, mantendo os mesmos nomes.
