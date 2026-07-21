# Processamento por lote — MDN-RPP01

## Status

Sem lotes registrados. Execução bloqueada por G0 e G1.

## Estrutura criada automaticamente para cada lote autorizado

```text
lotes/lote_NN/
├── 00_manifesto_lote
├── 01_diagnostico
├── 02_base_tratada_protegida
├── 03_base_trabalho_pseudonimizada
├── 04_limpeza_e_logs
├── 05_classificacao_taxonomica
├── 06_fila_validacao_humana
└── 07_matriz_por_lote
```

Cada etapa recebe uma execução própria e grava resultados novos. O pipeline não sobrescreve saídas existentes.

## Balanço obrigatório

`entrada = mantidos + excluidos_tecnicos + fora_classificacao_textual`

Comentários apenas com emojis permanecem contabilizados em `fora_classificacao_textual`. Itens sem evidência suficiente recebem `nao_determinado`.

## Segredo de pseudonimização

O pipeline exige uma variável de ambiente `MDN_PSEUDONYM_KEY`. O valor não pode aparecer em arquivos, logs, manifestos ou commits. A mesma chave deve ser preservada em ambiente protegido durante toda a rodada para manter pseudônimos estáveis.

