# Conferência de citações com IA antes de protocolar

*O método em 4 passos para nenhuma jurisprudência inventada chegar ao processo*

Base: CPC, arts. 77, 80 e 81 · Estatuto da OAB, arts. 32 e 34, XIV · CNJ, pauta do Plenário Virtual (DJe 277/2026) · TJPR, 9ª Câmara Cível

## Por que agora

> **Fundamento:** é dever de partes e procuradores não formular pretensão ou defesa sabidamente sem fundamento (CPC, art. 77, II). Deturpar o teor de dispositivo de lei ou de julgado para iludir o juiz é infração disciplinar (Estatuto da OAB, art. 34, XIV).

| Fato | Onde |
|---|---|
| O CNJ pautou recurso que pede recomendação sobre a apuração individualizada da responsabilidade de advogados que apresentam jurisprudência inexistente gerada por IA, sem caracterizar automaticamente má-fé | 18ª Sessão do Plenário Virtual (27/11 a 04/12/2026), DJe 277/2026 |
| O TJPR aplicou multa por litigância de má-fé "pelo uso de inteligência artificial sem o devido zelo e cautela" e oficiou a OAB/PR | 9ª Câmara Cível, 0108267-74.2025.8.16.0000, julgado em 16/05/2026 |
| A multa por má-fé vai de mais de 1% a menos de 10% do valor corrigido da causa, além de indenização | CPC, art. 81 |

## Passo 1 · Anonimize

Antes de colar, retire nome das partes, CPF, CNPJ, endereço, número do processo e qualquer dado do cliente. O sigilo profissional vale também na janela do chat.

## Passo 2 · Ligue a pesquisa na web

No Claude, a pesquisa na web fica no menu de ferramentas da conversa; em planos Team e Enterprise, o administrador precisa liberar o recurso. Sem pesquisa, a IA só "lembra" e pode inventar.

## Passo 3 · Cole o prompt revisor

```
Atue como revisor de citações de uma peça jurídica brasileira.
1. Liste em tabela TODAS as referências do texto: leis e artigos,
   súmulas, temas repetitivos, julgados e doutrina.
2. Colunas: trecho citado | tipo | identificação informada
   (tribunal, classe, número, relator, data) | link em site OFICIAL
   (planalto.gov.br, stf.jus.br, stj.jus.br, site do tribunal) |
   situação.
3. Situação, só uma destas: LOCALIZADO NA FONTE OFICIAL,
   NÃO LOCALIZADO ou DIVERGENTE (número, relator, data ou conteúdo
   diferentes do citado).
4. Blog, site de curso e agregador não provam existência: nesses
   casos marque NÃO LOCALIZADO.
5. Nunca complete dados que faltam: diga o que falta.
6. Ao final, liste por prioridade o que devo abrir pessoalmente.
Texto:
[cole aqui a peça já anonimizada]
```

## Passo 4 · Você confere (a parte que não se delega)

- [ ] Abri cada link LOCALIZADO e li a ementa no site do tribunal.
- [ ] Número, relator e data batem com o que está na peça.
- [ ] O trecho entre aspas está de fato na ementa ou no voto.
- [ ] Retirei ou substituí todo item NÃO LOCALIZADO ou DIVERGENTE.
- [ ] Artigos de lei conferidos no texto compilado do Planalto.
- [ ] Súmulas e temas conferidos como vigentes (não cancelados nem superados).

> **Atenção:** a IA também erra na conferência. Um "LOCALIZADO" só vale depois que você abriu o link e leu.

## Como ler a tabela que a IA devolve

| Situação | O que fazer |
|---|---|
| LOCALIZADO NA FONTE OFICIAL | Abrir, ler e confirmar o trecho citado |
| DIVERGENTE | Corrigir o dado na peça ou trocar o precedente |
| NÃO LOCALIZADO | Procurar você mesmo no site do tribunal; não achou, retira |

> **Resumo:** a IA mostra onde procurar. Quem assina é quem responde (Estatuto da OAB, art. 32).

## Fontes

- CNJ, pauta da 18ª Sessão do Plenário Virtual de 2026 (DJe 277/2026, 19/11/2026): https://www.cnj.jus.br/pauta-de-julgamentos-18a-sessao-do-plenario-virtual-de-2026-27-11-2026-a-04-12-2026/
- TJPR, 9ª Câmara Cível, rel. Luis Sergio Swiech, 0108267-74.2025.8.16.0000, j. 16/05/2026: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035214151/Ac%C3%B3rd%C3%A3o-0108267-74.2025.8.16.0000
- Lei 13.105/2015 (CPC), arts. 77, 80 e 81: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm
- Lei 8.906/1994 (Estatuto da OAB), arts. 32 e 34: https://www.planalto.gov.br/ccivil_03/leis/l8906.htm
- Central de Ajuda da Anthropic, pesquisa na web: https://support.claude.com/en/articles/10684626-enable-and-use-web-search

*Material informativo, sem caráter de consultoria.*
