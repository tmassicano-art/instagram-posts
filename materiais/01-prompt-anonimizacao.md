# Anonimize antes de colar a peça na IA

*Prompt pronto, checklist e a base legal para usar IA sem expor o cliente*

Base: LGPD, arts. 5º e 6º · Estatuto da OAB, art. 34, VII · Código de Ética da OAB, art. 35 · Recomendação CFOAB 001/2024

## Por que anonimizar

> **Fundamento:** o advogado tem o dever de guardar sigilo dos fatos que conhece no exercício da profissão (Código de Ética e Disciplina da OAB, art. 35), e violar sigilo profissional sem justa causa é infração disciplinar (Estatuto da OAB, art. 34, VII).

A LGPD reforça o mesmo caminho:

| Conceito | O que a LGPD diz | Na prática |
|---|---|---|
| Dado pessoal | Informação de pessoa natural identificada ou identificável (art. 5º, I) | Nome, CPF, endereço, e-mail, telefone |
| Dado sensível | Saúde, vida sexual, religião, biometria, entre outros (art. 5º, II) | Laudos, atestados, prontuários: cuidado redobrado |
| Anonimização | Meios técnicos razoáveis que tiram a possibilidade de associar o dado ao titular (art. 5º, XI) | Trocar por marcadores e generalizar valores e datas |
| Necessidade | Tratar só o mínimo necessário para a finalidade (art. 6º, III) | A IA recebe só o que a tarefa exige |

> **Atenção:** trocar só o nome não basta. Número do processo, valor exato da causa e endereço permitem identificar o cliente com uma busca simples.

## O prompt de anonimização

Use numa ferramenta aprovada pelo escritório e confira o resultado antes de levar o texto a outra IA.

```
Você vai anonimizar um texto jurídico antes do uso em ferramentas de IA.
Substitua, de forma consistente em todo o texto:
- nomes de pessoas físicas por [PARTE 1], [PARTE 2], [TESTEMUNHA 1]...
- nomes de empresas por [EMPRESA 1], [EMPRESA 2]...
- CPF, CNPJ, RG, OAB, e-mail e telefone por [DOCUMENTO] ou [CONTATO]
- endereços por [ENDEREÇO] e cidades por [CIDADE] (se a cidade não
  for relevante para a tese)
- número do processo por [PROCESSO]
- valores exatos por faixas ("cerca de R$ 50 mil")
- datas exatas por referências relativas ("três meses depois"),
  salvo prazos relevantes para a tese
- dados de saúde, religião ou vida sexual por [DADO SENSÍVEL]
Não altere fundamentos jurídicos, artigos de lei nem a narrativa.
Entregue: (1) o texto anonimizado; (2) a tabela
[marcador -> dado original] para eu guardar fora da IA.
```

> **Na prática:** a tabela de correspondência fica no sistema do escritório, nunca na conversa com a IA. Depois de usar a resposta, você troca os marcadores de volta.

## Exemplo fictício

> **Exemplo:** "Maria Souza, CPF 123..., moradora da Rua X, 100, ajuizou em 03/02/2025 a ação 1000123-45.2025... cobrando R$ 48.317,22" vira "[PARTE 1], [DOCUMENTO], moradora de [ENDEREÇO], ajuizou a ação [PROCESSO] no início de 2025, cobrando cerca de R$ 50 mil".

## Checklist antes de colar

- [ ] Nomes, documentos e endereços trocados por marcadores.
- [ ] Número do processo, valores exatos e datas generalizados.
- [ ] Dados sensíveis (saúde, religião, biometria) retirados ou marcados.
- [ ] Anexos conferidos: metadados, assinaturas e cabeçalhos também identificam.
- [ ] Termos da ferramenta lidos: os dados são usados para treinamento? Dá para desativar?
- [ ] Tabela de correspondência guardada fora da IA.

## Erros comuns

> **Erro comum:** colar o PDF inteiro dos autos "só para resumir". Recorte o trecho necessário e anonimize; a IA quase nunca precisa do processo todo.

- Esquecer o nome do cliente no nome do arquivo enviado.
- Deixar o número da OAB do colega ou o e-mail do cliente na assinatura.
- Usar conta pessoal gratuita para trabalho do escritório sem verificar a política de dados.

## Fontes

- Lei 13.709/2018 (LGPD), arts. 5º e 6º: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Lei 8.906/1994 (Estatuto da OAB), art. 34: https://www.planalto.gov.br/ccivil_03/leis/l8906.htm
- Código de Ética e Disciplina da OAB (Resolução CFOAB 02/2015), art. 35.
- CFOAB, Recomendação 001/2024 sobre IA generativa na prática jurídica, pilar de confidencialidade e privacidade: https://www.oab.org.br/noticia/62711/confira-versao-final-da-recomendacao-do-cfoab-sobre-o-uso-de-ia-na-pratica-juridica

*Material informativo, sem caráter de consultoria.*
