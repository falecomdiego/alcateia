# Nota metodologica - rodada inicial

## 1. Origem dos dados
Os dados derivam de comentarios extraidos do Instagram por extensao do Chrome e organizados originalmente em arquivos XLSX brutos.

## 2. Divisao por lotes
A rodada inicial considerou apenas `lote_01`, `lote_02` e `lote_03`. `lote_04` e `lote_05` nao fazem parte deste ciclo.

## 3. Etapas do pipeline
O pipeline aplicado separou diagnostico tecnico, padronizacao, limpeza, classificacao, Camada 3, Matriz Resolutiva, consolidacao e painel final.

## 4. Limpeza com log
Remocoes tecnicas ocorreram apenas na etapa de limpeza, com registro obrigatorio em log e preservacao das bases anteriores.

## 5. Classificacao Pilar 2
A classificacao Pilar 2 estruturou comentarios conforme regras tecnicas e preservou comentario, origem, lote e justificativa de vinculo.

## 6. Camada 3
A Camada 3 separou dimensoes operacionais e experienciais, mantendo natureza_principal, polaridade_textual, evidencias e campos de rastreabilidade.

## 7. Matriz Resolutiva
A Matriz Resolutiva consolidou problemas, impactos, recomendacoes, responsaveis e indicadores, sempre com evidencia_textual e ids_linhas_relacionadas.

## 8. Consolidacao da rodada inicial
As matrizes oficiais dos lotes 01, 02 e 03 foram consolidadas em uma matriz auditavel unica.

## 9. Painel final
O painel final agrupou problemas semelhantes em macroproblemas executivos sem substituir a matriz auditavel consolidada.

## 10. Limitacoes da amostra
A rodada inicial e uma amostra inicial. Ela nao representa ainda a ampliacao futura para 50 perfis ou 10.000 comentarios.

## 11. Criterios de rastreabilidade
Foram preservados lotes_relacionados, arquivos_origem_relacionados, ids_linhas_relacionadas, evidencias_representativas e indicadores de monitoramento.

## 12. Confirmacao de ciclo
`lote_04` e `lote_05` nao fazem parte deste ciclo e nao foram usados nesta leitura executiva final.
