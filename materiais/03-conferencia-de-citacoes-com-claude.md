# Conferência de citações com o Claude antes de protocolar

*Material do Reels de 27/11/2026 · @thiago.massicano*

## Por que agora
- A pauta da 18ª Sessão do Plenário Virtual do CNJ (27/11 a 04/12/2026) traz um recurso que pede recomendação sobre a apuração individualizada da responsabilidade de advogados que apresentam jurisprudência inexistente gerada por IA generativa, sem caracterização automática de litigância de má-fé. Fonte: CNJ, pauta publicada no DJe nº 277/2026, de 19/11/2026.
- Os tribunais já aplicam sanção: a 9ª Câmara Cível do TJPR, em acórdão de 16/05/2026, aplicou multa por litigância de má-fé "pelo uso de inteligência artificial sem o devido zelo e cautela" e determinou ofício à OAB/PR (TJPR, 0108267-74.2025.8.16.0000).

## Passo 1 · Anonimize
Antes de colar, apague nome das partes, CPF, CNPJ, endereço, número do processo e qualquer dado do cliente. Sigilo profissional vale também na tela do chat.

## Passo 2 · Ative a pesquisa na web
No Claude, a pesquisa na web fica no menu "+" da conversa (na interface nova, o Claude pesquisa sozinho quando precisa). Em planos Team e Enterprise, o administrador precisa liberar o recurso antes.

## Passo 3 · Cole este prompt

```
Atue como revisor de citações de uma peça jurídica brasileira.

1. Liste em tabela TODAS as referências do texto abaixo: leis e artigos,
   súmulas, temas repetitivos, julgados e doutrina.
2. Colunas: trecho citado | tipo | identificação informada (tribunal,
   classe, número, relator, data) | link encontrado em site OFICIAL
   (planalto.gov.br, stf.jus.br, stj.jus.br, site do tribunal) |
   situação.
3. Na coluna "situação", use só: LOCALIZADO NA FONTE OFICIAL,
   NÃO LOCALIZADO ou DIVERGENTE (número, relator, data ou conteúdo
   diferentes do citado).
4. Não use blogs, sites de cursos nem agregadores como prova de
   existência. Se só achar a citação nesses sites, marque NÃO LOCALIZADO.
5. Nunca complete dados que faltam. Se faltar número ou relator, diga
   o que falta.
6. Ao final, liste em ordem de prioridade o que devo abrir pessoalmente
   antes de protocolar.

Texto:
[cole aqui a peça já anonimizada]
```

## Passo 4 · Você confere (a parte que não se delega)
- [ ] Abri cada link marcado como LOCALIZADO e li a ementa no site do tribunal
- [ ] O número, o relator e a data batem com o que está na peça
- [ ] O trecho entre aspas está de fato na ementa ou no voto
- [ ] Removi ou substituí todo item NÃO LOCALIZADO ou DIVERGENTE
- [ ] Artigos de lei conferidos no texto compilado do Planalto
- [ ] Súmulas e temas conferidos como vigentes (não cancelados nem superados)

## Cuidados
- A IA ajuda a achar onde procurar. A responsabilidade pela citação continua sendo de quem assina a peça.
- Repita a conferência sempre que a peça mudar depois da revisão.

**Fontes:** CNJ, pauta de julgamentos da 18ª Sessão do Plenário Virtual de 2026 (DJe nº 277/2026, 19/11/2026): https://www.cnj.jus.br/pauta-de-julgamentos-18a-sessao-do-plenario-virtual-de-2026-27-11-2026-a-04-12-2026/ · TJPR, 9ª Câmara Cível, rel. Luis Sergio Swiech, julgado em 16/05/2026: https://portal.tjpr.jus.br/jurisprudencia/j/4100000035214151/Ac%C3%B3rd%C3%A3o-0108267-74.2025.8.16.0000 · Central de Ajuda da Anthropic, "Enable and use web search": https://support.claude.com/en/articles/10684626-enable-and-use-web-search

*Material informativo, sem caráter de consultoria.*
