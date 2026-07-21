# Relatorio de revisao do painel interno V1

Escopo revisado: `C:\Users\Diego\Documents\Codex\2026-06-15\analise_comentarios_evento\14_dashboard_visual_rodada_inicial`

Modo de revisao: validacao minima V1, sem reprocessamento, sem alteracao de dados e sem correcao automatica dos arquivos do painel.

Observacao operacional: a tentativa de abertura do painel em navegador local foi bloqueada pela politica do ambiente. A validacao visual minima foi feita por revisao estatica objetiva de `index.html`, `app.js`, `styles.css` e `data/dashboard_data.json`, sem criar rota alternativa e sem servir o painel por outro caminho.

| tela ou secao | texto atual | problema identificado | correcao proposta | tipo de problema | nivel do problema | bloqueia validacao interna |
|---|---|---|---|---|---|---|
| Metodologia > Fontes oficiais usadas | `C:\Users\Diego\Documents\Codex\...\matriz_resolutiva_rodada_inicial.xlsx` e demais caminhos completos | Exposicao de caminho local completo, usuario, estrutura interna do projeto e arquivos de bastidor dentro da interface. | Exibir apenas nome do arquivo, tipo de fonte e hash curto; ocultar o caminho local completo. | Blindagem de linguagem / validacao visual minima | Erro critico | sim |
| Filtros | `Perfil/Festa monitorada` | O painel informa que o campo literal de festa nao existe, mas o filtro usa `Festa`, o que pode induzir leitura de atribuicao direta. | `Recorte monitorado (proxy tecnico)` | Padronizacao / blindagem de linguagem | Erro critico | sim |
| Indicadores e detalhe da matriz | `Perfis/Festas monitoradas` | Mesmo problema de atribuicao: mistura perfil e festa sem campo literal validado de festa/evento. | `Recortes monitorados por proxy tecnico` | Padronizacao / blindagem de linguagem | Erro critico | sim |
| Rankings | `Ranking de Perfis/Festas` | O titulo pode parecer ranking publico de festas ou perfis, embora a base use proxy tecnico. | `Ranking de recortes monitorados por proxy tecnico` | Blindagem de linguagem | Erro critico | sim |
| Rankings | `Mais bem avaliados por sinais positivos identificados` / `Maior criticidade identificada` | A formulacao pode soar como avaliacao reputacional direta de perfil, festa ou organizacao. | `Sinais positivos agregados por recorte tecnico` / `Pontos de atencao agregados por recorte tecnico` | Blindagem de linguagem | Erro critico | sim |
| Cartoes de recomendacao e detalhe da matriz | `responsavel`, `sem responsavel`, `bar`, `producao`, `operacao`, `seguranca`, `gestao_do_evento` | Pode sugerir responsabilizacao direta antes de validacao interna. | `area sugerida para validacao interna`; `sem area sugerida`; manter areas como encaminhamento preliminar. | Blindagem de linguagem | Erro critico | sim |
| Indicadores oficiais e tabela | `Linhas de evidencia rastreadas`, `Volume`, `Recomendacoes sem evidencia` | Numeros aparecem sem contexto suficiente e podem ser confundidos com total de comentarios ou universo analisado. | Usar `linhas de evidencia rastreadas (proxy tecnico)`, `ocorrencias no universo analisado` e nota `nao representa total de comentarios analisados`. | Validacao visual minima / padronizacao | Erro critico | sim |
| Textos fixos e dinamicos | `Nao`, `Proxima`, `Recomendacao`, `Evidencias`, `ocorrencias`, `unicas`, `Mencao`, `extraida`, `tecnico`, `navegavel`, `metodologica` | Erros visiveis de acentuacao e ortografia em botoes, cabecalhos, tabelas, rankings e estados vazios. | Aplicar acentuacao correta apenas na camada de exibicao: `Não`, `Próxima`, `Recomendação`, `Evidências`, `ocorrências`, `únicas`, `Menção`, `extraída`, `técnico`, `navegável`, `metodológica`. | Ortografia | Erro critico | sim |
| Hero / texto de abertura | `Camada visual de apresentacao dos resultados validados` | Pode confundir resultado validado com painel validado; o status atual informa que o painel ainda esta em revisao. | `Camada visual em revisao dos resultados da rodada inicial validada`. | Padronizacao | Erro medio | nao |
| Status strip | `Fonte: 5 arquivos oficiais validados` | A expressao pode parecer validacao do painel, quando o que existe sao fontes oficiais usadas. | `Fontes oficiais consultadas: 5 arquivos internos da rodada inicial validada`. | Padronizacao | Erro medio | nao |
| Status strip | `Nao pertencem a esta rodada: lote_04 | lote_05` | A informacao e correta, mas no topo pode distrair e gerar duvida sobre o recorte do painel. | `Fora do recorte V1: lote_04 e lote_05 nao usados`, preferencialmente na metodologia. | Validacao visual minima | Erro medio | nao |
| Filtro de entidade textual | Lista com `@...` de perfis e entidades | Exibe mencoes diretas; para uso interno pode ser util, mas exige aviso claro de evidencia agregada e validacao interna antes de atribuicao publica. | `Menções textuais agregadas`; incluir aviso `sem atribuição pública de causa`. | Blindagem de linguagem | Erro medio | nao |
| Busca textual | `Buscar em problemas, evidencias e recomendacoes` | Alem da falta de acentos, a busca reforca `problemas` como unica chave de leitura. | `Buscar em recorrencias, evidencias e recomendacoes`. | Padronizacao / ortografia | Erro medio | nao |
| Matriz Resolutiva | Colunas `Recomendacao` e `Evidencias` com textos longos | Excesso de informacao em celula pode reduzir legibilidade e hierarquia, principalmente em tela menor. | Manter texto completo no painel de detalhe e usar pre-visualizacao curta na tabela. | Validacao visual minima | Erro medio | nao |
| Graficos e filtros | `experiencia`, `operacao`, `preco`, `seguranca`, `intencao_de_retorno`, `recomendacao_espontanea` | Identificadores internos aparecem como texto final, sem acento ou com underscore. | Aplicar mapa de exibicao: `experiência`, `operação`, `preço`, `segurança`, `intenção de retorno`, `recomendação espontânea`. | Ortografia / padronizacao | Erro medio | nao |
| Paginacao | `Anterior` / `Proxima` | Botoes desabilitados nao possuem estado visual proprio em CSS, podendo parecer clicaveis. | Adicionar estado visual para `disabled` e corrigir `Próxima`. | Validacao visual minima | Erro leve | nao |
| Navegacao mobile | `Geral`, `Evidencias` | `Geral` e pouco especifico; `Evidencias` esta sem acento. | `Visão geral` e `Evidências`, mantendo tamanho legivel. | Ortografia / validacao visual minima | Erro leve | nao |

## Totais

- Erros criticos: 8
- Erros medios: 7
- Erros leves: 2

