# Pipeline MDN V2

Pipeline configurável da rodada `MDN-RPP01`. A implementação usa apenas a biblioteca padrão do Python e não altera os cinco scripts históricos.

## Princípios implementados

- gates bloqueiam execução prematura;
- cada lote é processado isoladamente;
- XLSX é apenas lido e conferido por hash;
- oito colunas originais são exigidas sem divergência;
- pseudonimização usa HMAC com segredo externo ao Git;
- nenhum registro desaparece da base de tratamento;
- emoji isolado fica fora da classificação textual, não é apagado;
- classificação lexical é somente sugestão e permite `nao_determinado`;
- casos sensíveis entram em fila humana;
- consolidação usa relação `grupo_registro`;
- publicação exige G4, registro de liberação, métricas e autorização por grupo;
- toda execução gera manifesto com entradas, saídas, hashes e contagens.

## Comandos seguros disponíveis antes de G0

```powershell
python -m pipeline_mdn_v2.mdn_pipeline.cli validate-config
python -m pipeline_mdn_v2.mdn_pipeline.cli verify-taxonomy
```

Os demais comandos recusam execução enquanto seus gates estiverem bloqueados.

