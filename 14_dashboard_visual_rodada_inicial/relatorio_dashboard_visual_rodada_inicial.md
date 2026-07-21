# Relatorio do dashboard visual - rodada inicial

## Entrega

Dashboard navegavel final da rodada inicial criado com o nome visual:

`Mapa da Noite`

Pasta de saida:

`C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\14_dashboard_visual_rodada_inicial`

## Fontes oficiais utilizadas

1. `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\10_consolidacao_rodada_inicial\matriz_resolutiva_rodada_inicial.xlsx`
2. `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\10_consolidacao_rodada_inicial\painel_resolutivo_rodada_inicial.xlsx`
3. `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\11_painel_final_rodada_inicial\matriz_executiva_agrupada_rodada_inicial.xlsx`
4. `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\11_painel_final_rodada_inicial\painel_final_rodada_inicial.xlsx`
5. `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\11_painel_final_rodada_inicial\relatorio_painel_final_rodada_inicial.md`

## Lotes usados

- Incluidos no painel: `lote_01`, `lote_02`, `lote_03`.
- Nao usados como dados do painel: `lote_04`, `lote_05`.

Observacao tecnica: `lote_04` e `lote_05` aparecem apenas como texto de exclusao em fonte oficial de status da rodada. Eles nao aparecem como lotes filtraveis nem como registros da matriz visual.

## Arquivos gerados

- `index.html`
- `styles.css`
- `app.js`
- `data\dashboard_data.json`
- `data\dashboard_data.js`
- `relatorio_dashboard_visual_rodada_inicial.md`

## Linhas e registros processados

- Problemas resolutivos lidos da matriz detalhada: 1000.
- Macroproblemas lidos da matriz executiva: 39.
- Perfis/arquivos proxy rastreados: 13.
- Linhas de evidencia unicas identificadas como proxy tecnico: 3032.
- Recomendacoes executivas sem evidencia textual associada: 0.

## Campos tratados como proxy tecnico

- Campo literal `festa`: nao identificado; usado `arquivo_origem` / `perfil_proxy` derivado do nome do arquivo.
- Campo literal `perfil_monitorado`: nao identificado; usado `arquivo_origem` / `perfil_proxy` derivado do nome do arquivo.
- Campo literal `DJ`: nao identificado; usadas mencoes textuais `@...` extraidas das evidencias, sem cadastro externo.
- Campo literal `entidade_monitorada`: nao identificado; usadas mencoes textuais `@...` e arquivo de origem como sinais tecnicos.
- Campo literal `categoria_principal`: nao identificado; usado `categorias_relacionadas` como categoria validada quando disponivel.
- Campo literal `categoria_secundaria`: nao identificado; usado `categorias_relacionadas` como categoria validada quando disponivel.
- Campo literal `total_comentarios_considerados`: nao identificado; exibidas linhas de evidencia unicas como proxy tecnico de rastreabilidade.
- Campo literal `total_perfis_monitorados`: nao identificado; exibidos arquivos/perfis proxy rastreados.

## Inconsistencias encontradas

- Nenhuma inconsistencia estrutural bloqueante foi encontrada nos arquivos aprovados.
- Nenhuma recomendacao executiva foi exibida sem evidencia textual associada.
- Nenhum arquivo bruto ou arquivo analitico anterior foi alterado.

## Observacao metodologica

O dashboard e uma camada visual de apresentacao dos resultados ja validados. Ele nao altera definicoes metodologicas, nomenclaturas analiticas, classificacoes, resultados, lotes nem conclusoes previamente aprovadas.
