# Consolidação e linhagem — MDN-RPP01

A consolidação somente poderá ler lotes encerrados e aprovados em G2. O pipeline produzirá saídas em `saidas/`, ignoradas pelo Git por poderem conter material interno.

## Contrato relacional

### `registros.csv`

Uma linha por `registro_id`, com lote, fonte, situação de tratamento, frente validada ou `nao_determinado` e decisão humana relacionada.

### `grupos.csv`

Uma linha por `grupo_id`, com critério de agrupamento, frente, quantidade de registros e status de validação.

### `grupo_registro.csv`

Uma linha por vínculo entre `grupo_id` e `registro_id`. Listas concatenadas de identificadores são proibidas.

### `registro_decisao.csv`

Uma linha por vínculo entre `registro_id` e revisão ou adjudicação humana. A decisão final permanece identificada sem apagar revisões concordantes ou divergentes.

## Invariantes

- `registro_id` é único em `registros`;
- todo vínculo referencia um registro e um grupo existentes;
- a contagem de vínculos por grupo é igual a `volume_registros`;
- nenhum registro excluído tecnicamente integra grupo analítico;
- qualquer recomendação é separada da evidência observada.
