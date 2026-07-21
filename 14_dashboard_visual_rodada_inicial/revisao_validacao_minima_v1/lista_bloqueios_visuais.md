# Lista de bloqueios visuais

Escopo: validacao visual minima, limitada a problemas objetivos. Nenhum redesenho foi proposto e nenhuma correcao foi aplicada.

## Bloqueios criticos

| secao | bloqueio visual | motivo | correcao minima proposta |
|---|---|---|---|
| Metodologia > Fontes oficiais usadas | Caminhos locais completos aparecem na interface. | Dado sensivel de bastidor exposto. | Exibir apenas nome do arquivo e hash curto. |
| Indicadores oficiais | Numeros aparecem sem contexto suficiente de universo ou proxy. | Numero sem contexto pode induzir interpretacao errada. | Adicionar contexto no rotulo: `proxy tecnico`, `universo analisado`, `rodada inicial validada`. |
| Rankings | Titulos de ranking podem parecer avaliacao direta de perfis/festas. | Risco reputacional e de atribuicao publica. | Substituir por recortes agregados e proxy tecnico. |
| Detalhe e cards | Campo `responsavel` aparece como atribuicao direta. | Pode sugerir responsavel validado sem validacao interna. | Trocar por `area sugerida para validacao interna`. |
| Textos visiveis | Falta de acentos em botoes, headers, tabelas e textos dinamicos. | Ortografia visivel impede validacao minima. | Corrigir acentuacao na camada de exibicao. |

## Problemas medios

| secao | problema visual | motivo | correcao minima proposta |
|---|---|---|---|
| Status strip | `Nao pertencem a esta rodada: lote_04 | lote_05` aparece no topo. | Pode gerar ruido no primeiro contato com o painel. | Mover para metodologia ou reescrever como `fora do recorte V1`. |
| Matriz Resolutiva | Colunas de recomendacao e evidencia podem ficar densas. | Excesso de informacao em celula dificulta varredura visual. | Usar pre-visualizacao curta e manter texto completo no detalhe. |
| Filtro de entidade textual | Lista muitos `@...` diretamente. | Pode causar leitura de exposicao ou atribuicao direta. | Reforcar que sao mencoes textuais agregadas. |
| Graficos e filtros | Identificadores internos aparecem como labels finais. | Labels com underscore ou sem acento reduzem legibilidade. | Aplicar mapa de exibicao sem alterar os dados. |

## Problemas leves

| secao | problema visual | motivo | correcao minima proposta |
|---|---|---|---|
| Paginacao | Botoes desabilitados nao possuem estado visual claro. | Pode parecer que o botao ainda esta disponivel. | Adicionar estado visual `disabled`. |
| Navegacao mobile | `Geral` e `Evidencias`. | Rotulo pouco especifico e sem acento. | Usar `Visão geral` e `Evidências`. |

## Itens nao identificados como bloqueio nesta etapa

- Nao foi identificado problema estrutural de tabela sem rolagem: `.table-shell` possui `overflow: auto`.
- Nao foi identificado risco objetivo de layout por cards sem quebra de texto: labels principais usam `overflow-wrap: anywhere`.
- Nao houve avaliacao estetica, redesenho visual ou aplicacao de manual de identidade visual.

