# Lista de blindagem de linguagem

Escopo: mapear formulacoes que podem gerar atribuicao indevida ou leitura acusatoria. Nenhuma correcao foi aplicada no painel.

| texto atual | risco de interpretacao | formulacao segura proposta | nivel |
|---|---|---|---|
| `Perfil/Festa monitorada` | Sugere que ha campo literal de festa/evento, embora o proprio painel use proxy tecnico. | `Recorte monitorado (proxy técnico)` | Erro critico |
| `Perfis/Festas monitoradas` | Pode parecer atribuicao direta a uma festa ou perfil. | `Recortes monitorados por proxy técnico` | Erro critico |
| `Ranking de Perfis/Festas` | Pode transformar proxy tecnico em ranking reputacional direto. | `Ranking de recortes monitorados por proxy técnico` | Erro critico |
| `Mais bem avaliados por sinais positivos identificados` | Pode soar como avaliacao positiva direta de perfil, festa ou organizacao. | `Sinais positivos agregados por recorte técnico` | Erro critico |
| `Maior criticidade identificada` | Pode soar como acusacao ou julgamento direto. | `Pontos de atenção agregados por recorte técnico` | Erro critico |
| `DJs e entidades textuais` | Pode sugerir cadastro ou avaliacao direta de artistas/entidades. | `Menções textuais agregadas, sem cadastro externo` | Erro medio |
| `responsável` / `sem responsável` | Pode sugerir responsabilizacao validada. | `área sugerida para validação interna` / `sem área sugerida` | Erro critico |
| `Revisar o ponto operacional associado a fila/bar/preço/segurança/som` | Pode parecer causa operacional ja confirmada. | `No universo analisado, a recorrência observada em [tema] indica ponto de atenção para validação interna.` | Erro medio |
| `Macroproblema operacional: fila` | Pode soar como diagnostico conclusivo sem nota de contexto. | `Recorrência operacional observada: fila` | Erro medio |
| `Macroproblema experiencial: rejeição` | Pode soar como leitura reputacional direta. | `Sinal de percepção em experiência: rejeição` | Erro medio |
| Menções `@...` em filtros e rankings | Exposicao direta de perfis ou entidades em tela. | `Menções textuais agregadas`; manter handles apenas quando a validacao interna exigir rastreabilidade. | Erro medio |
| Caminhos locais completos em `Fontes oficiais usadas` | Exposicao de bastidor tecnico e estrutura local. | `Fonte oficial interna validada: [nome do arquivo]` + hash curto. | Erro critico |

## Frases de seguranca recomendadas

- `no universo analisado`
- `comentários públicos analisados`
- `recorrência observada`
- `sinal de percepção`
- `ponto de atenção`
- `evidência agregada`
- `leitura contextual`
- `sem atribuição pública de causa`
- `validação interna necessária`

## Regra de aplicacao

As correcoes devem atuar apenas na camada textual de exibicao. Elas nao exigem alterar base oficial, matriz, taxonomia, lote ou dado analitico.

