# Lista de correcoes de ortografia e padronizacao

Escopo: somente mapeamento de correcoes propostas para o painel interno V1. Nenhuma correcao foi aplicada automaticamente.

## Ortografia visivel a corrigir

| texto atual | correcao proposta | observacao |
|---|---|---|
| `Nao` / `nao` | `Não` / `não` | Aparece em status, estados vazios e textos metodologicos. |
| `Proxima` | `Próxima` | Botao de paginacao. |
| `Recomendacao` / `recomendacao` | `Recomendação` / `recomendação` | Cabecalhos, detalhe e estados vazios. |
| `Evidencias` / `evidencias` | `Evidências` / `evidências` | Cabecalhos, mobile nav e textos dinamicos. |
| `ocorrencias` | `ocorrências` | Rankings, matriz e cards. |
| `unicas` | `únicas` | Ranking de recortes. |
| `Mencao` / `mencao` | `Menção` / `menção` | Ranking de entidades textuais. |
| `extraida` | `extraída` | Ranking de entidades textuais. |
| `tecnico` | `técnico` | Eyebrow de ranking e metodologia. |
| `navegavel` | `navegável` | Eyebrow da matriz. |
| `metodologica` | `metodológica` | Eyebrow de metodologia. |
| `possivel` | `possível` | Mensagem de erro de carregamento. |
| `responsavel` | `responsável` | Deve ser substituido por linguagem de validacao interna. |
| `comentarios` | `comentários` | Textos de busca e recomendacoes. |
| `experiencia` | `experiência` | Eixos, filtros, recomendacoes e graficos. |
| `operacao` | `operação` | Eixos, filtros, recomendacoes e graficos. |
| `reducao` | `redução` | Recomendacoes. |
| `recorrencia` | `recorrência` | Recomendacoes e textos metodologicos. |
| `acao` | `ação` | Recomendacoes. |
| `preco` | `preço` | Categorias e macroproblemas. |
| `seguranca` | `segurança` | Categorias, macroproblemas e areas sugeridas. |
| `rejeicao` | `rejeição` | Categoria e macroproblema. |
| `identificacao` | `identificação` | Categoria. |
| `lotacao` | `lotação` | Categoria. |
| `sinalizacao` | `sinalização` | Categoria. |
| `climatizacao` | `climatização` | Categoria. |
| `decepcao` | `decepção` | Categoria. |

## Padronizacao de termos obrigatorios

| termo atual ou risco | forma padronizada proposta |
|---|---|
| `Perfil/Festa monitorada` | `Recorte monitorado (proxy técnico)` |
| `Perfis/Festas monitoradas` | `Recortes monitorados por proxy técnico` |
| `Ranking de Perfis/Festas` | `Ranking de recortes monitorados por proxy técnico` |
| `Mais bem avaliados por sinais positivos identificados` | `Sinais positivos agregados por recorte técnico` |
| `Maior criticidade identificada` | `Pontos de atenção agregados por recorte técnico` |
| `DJs e entidades textuais` | `Menções textuais agregadas` |
| `responsável` | `área sugerida para validação interna` |
| `sem responsável` | `sem área sugerida` |
| `Volume` | `Ocorrências no universo analisado` |
| `Linhas de evidência rastreadas` | `Linhas de evidência rastreadas (proxy técnico)` |
| `resultados validados` | `resultados da rodada inicial validada` |
| `comentarios analisados` quando o numero for proxy | Usar somente se for total real de comentários; caso contrário, manter `linhas de evidência rastreadas`. |
| `universo analisado` ausente nos KPIs | Incluir como contexto de leitura quando houver numero consolidado. |
| `reputacional` como rótulo solto | Usar `reputação` em texto de interface quando o objetivo for leitura pública ou executiva. |
| `lote_01`, `lote_02`, `lote_03` | Manter exatamente assim. |
| `Codex` | Caso apareça em tela futura, manter exatamente `Codex`. |

## Termos sem inconsistencias bloqueantes

- `lote_01`, `lote_02` e `lote_03` aparecem de forma consistente no recorte da rodada inicial.
- `polaridade` aparece como filtro e campo de matriz; a correcao necessaria e contextual, nao estrutural.
- `evidência` e `recorrência` precisam ser usados com acento e, quando possivel, acompanhados de `agregada`, `observada` ou `no universo analisado`.

