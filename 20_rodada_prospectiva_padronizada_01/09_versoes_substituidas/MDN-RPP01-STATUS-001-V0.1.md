# MDN-RPP01-STATUS-001-V0.1 — Status de implantação

## Data

16/07/2026

## Implantado

- estrutura exclusiva da rodada `MDN-RPP01`;
- manifesto anterior à coleta e governança por gates;
- inventários, logs, dicionário, riscos, decisões, autoria, acessos, cópias e custos;
- configuração com Taxonomia Mestre V1.1 congelada por hash;
- Git 2.55.0 funcional e repositório inicializado;
- pipeline V2 sem dependências Python externas;
- ingestão XLSX protegida e pseudonimização por HMAC;
- tratamento sem perda invisível;
- classificação lexical de triagem com `nao_determinado`;
- amostragem e dupla revisão;
- consolidação relacional de registros, grupos e decisões;
- sanitizador público bloqueado por gate, métricas e autorizações;
- fixture sintética e guia de reaplicação.

## Verificações realizadas

- 6 testes automatizados aprovados;
- compilação Python aprovada;
- 57 arquivos da estrutura e do pipeline validados quanto a JSON, CSV e conteúdo não vazio;
- 15 XLSX brutos da rodada inicial continuam correspondendo por hash às 15 cópias organizadas em lotes;
- nenhum arquivo real existe na área protegida da nova rodada;
- nenhuma execução real ou saída pública foi criada;
- pipeline identificado pelo hash `d35c62ef775b0a3be8e4a8c2ca2c2df929e8a2987ade73e50266e706e8fcb760`.

## Estado dos gates

| Gate | Estado |
|---|---|
| G0 — Protocolo | bloqueado |
| G1 — Coleta | bloqueado |
| G2 — Análise | bloqueado |
| G3 — Consolidação | bloqueado |
| G4 — Publicação | bloqueado |
| G5 — Reaplicação externa | bloqueado |

## Pendências para G0

Definir período, perguntas finais, fontes, critérios, ferramenta e configuração de coleta, responsáveis, acessos, retenção, cópia protegida e segundo revisor. Nenhum lote pode ser processado antes dessas decisões.

