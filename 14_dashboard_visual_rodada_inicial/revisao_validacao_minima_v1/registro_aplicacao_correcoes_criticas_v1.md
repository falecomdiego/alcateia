# Registro de aplicacao das correcoes criticas V1

Escopo aplicado: somente correcoes minimas classificadas como erro critico na revisao do painel interno V1.

Pasta do painel interno: `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\14_dashboard_visual_rodada_inicial`

## Arquivos do painel alterados

- `index.html`
- `app.js`

## Erros criticos corrigidos

| erro critico | arquivo alterado | texto anterior | texto corrigido |
|---|---|---|---|
| Exposicao de caminhos locais completos em fontes oficiais | `app.js` | `source.caminho` exibido em `Fontes oficiais usadas` | `Fonte oficial interna validada; caminho local ocultado na interface.` + nome do arquivo, bytes e hash curto |
| Uso de `Perfil/Festa monitorada` sem campo literal de festa/evento | `index.html` | `Perfil/Festa monitorada` | `Recorte monitorado (proxy técnico)` |
| Uso de `Perfis/Festas monitoradas` | `index.html`, `app.js` | `Perfis/Festas monitoradas` | `Recortes por proxy técnico` / `Recortes monitorados por proxy técnico` |
| Titulo `Ranking de Perfis/Festas` | `index.html` | `Ranking de Perfis/Festas` | `Ranking de recortes monitorados por proxy técnico` |
| Titulos com avaliacao ou criticidade direta | `index.html` | `Mais bem avaliados por sinais positivos identificados`; `Maior criticidade identificada` | `Sinais positivos agregados por recorte técnico`; `Pontos de atenção agregados por recorte técnico` |
| Campo `responsavel` como atribuicao direta | `app.js` | `sem responsavel` e valor direto de `row.responsavel` em cards | `Área sugerida para validação interna: [area]` / `sem área sugerida` |
| Numeros sem contexto de universo ou proxy | `index.html`, `app.js` | `Linhas de evidência rastreadas`; `Volume`; `ocorrencias` | `Linhas de evidência rastreadas (proxy técnico)`; `Ocorrências no universo analisado`; `ocorrências no universo analisado` |
| Ortografia visivel sem acentos em textos fixos e dinamicos | `index.html`, `app.js` | `Nao`, `Proxima`, `Recomendacao`, `Evidencias`, `ocorrencias`, `unicas`, `Mencao`, `extraida`, `tecnico`, `navegavel`, `metodologica` | `Não`, `Próxima`, `Recomendação`, `Evidências`, `ocorrências`, `únicas`, `Menção`, `extraída`, `técnico`, `navegável`, `metodológica` |
| Mencoes diretas sem blindagem suficiente | `index.html`, `app.js` | `Entidade textual`; `DJs e entidades textuais`; `Mencao textual extraida de evidencias` | `Menções textuais agregadas`; `Menção textual agregada, sem atribuição pública de causa`; aviso de blindagem no detalhe |
| Rotulos internos com underscore ou sem acento aparecendo como texto final | `app.js` | `experiencia`, `operacao`, `preco`, `seguranca`, `intencao_de_retorno`, `recomendacao_espontanea` | Renderizacao de exibicao com `experiência`, `operação`, `preço`, `segurança`, `intenção de retorno`, `recomendação espontânea` |

## Confirmacoes

- Nenhum dado oficial foi alterado.
- Nenhuma matriz foi alterada.
- Nao houve reprocessamento.
- Nenhum painel novo foi criado.
- O painel publico nao foi alterado.
- Os arquivos `data/dashboard_data.json` e `data/dashboard_data.js` nao foram alterados.

