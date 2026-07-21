# MDN-RPP01-AUD-001-V0.1 — Revisão crítica e validação documental

## Controle

- Rodada de referência: `MDN-RPP01`
- Data: 16/07/2026
- Status: auditoria interna concluída
- Escopo: revisão documental sem coleta, reprocessamento, reclassificação ou publicação
- Gate afetado: nenhum
- Circulação externa: não autorizada

## Documentos recebidos

| Documento | Função declarada | Hash SHA-256 da fonte |
|---|---|---|
| `Relatorio_Interno_de_Sanitizacao.md` | registro interno da sanitização do caderno metodológico histórico | `9d127599090fcc91c65bd621356c99800acb7dce97d10d32380899c23944c842` |
| `Documento_Tecnico_Interacoes_Mapa_da_Noite.md` | consolidação técnica baseada em interações e documentos | `dc86cba3f5983c3b0bf238365aaea13ead6d2de62ef27ca4b0ae2bfee968cf5c` |
| `Documento_Tecnico_Interacoes_Mapa_da_Noite.docx` | representação diagramada do documento técnico | `8515e55fa491561cf3f428adeb4009e699bec1b16927e37477d40820385a5a66` |

O Markdown foi adotado como fonte textual principal do documento técnico. O DOCX foi conferido estruturalmente e possui o mesmo conteúdo essencial, mas não foi sobrescrito.

## Referências de validação

- `documentacao/Caderno_Metodologico_Externo_Mapa_da_Noite.md`;
- `12_leitura_executiva_final/nota_metodologica_rodada_inicial.md`;
- `MDN-RPP01-MAN-001-V0.1.md`;
- `MDN-RPP01-GOV-001-V0.1.md`;
- `MDN-RPP01-JUR-001-V0.1.md`;
- `MDN-RPP01-COM-001-V0.1.md`;
- `MDN-RPP01-STATUS-001-V0.2.md`;
- `MDN-RPP01-CONF-001-V0.1.json`;
- Taxonomia Mestre V1.1 congelada para a rodada.

## Decisão por documento

| Documento | Resultado | Uso permitido |
|---|---|---|
| Relatório Interno de Sanitização | aproveitável após reenquadramento | referência histórica interna; não comprova conformidade da MDN-RPP01 e não autoriza circulação |
| Documento Técnico de Interações | não aprovado na forma recebida | substituído por consolidação corrigida que separa histórico, estado prospectivo e intenção futura |
| DOCX recebido | preservado como fonte | não é a versão canônica corrigida |

## Achados críticos

### 1. Mistura entre histórico e rodada prospectiva

O documento técnico descreve em uma mesma linha narrativa:

- resultados da rodada inicial;
- declarações retrospectivas registradas em conversas;
- controles efetivamente implantados na MDN-RPP01;
- intenções futuras sem aprovação.

Essa mistura permite que um leitor interprete planos como execução e organização retrospectiva como rastreabilidade prospectiva. A versão corrigida separa explicitamente essas camadas.

### 2. Meta futura tratada como expansão observada

A menção a 50 perfis e 10.000 comentários não corresponde a base auditada. Os documentos da rodada inicial classificam esses números como ampliação futura. A MDN-RPP01 também registra 10.000 comentários apenas como meta condicionada. A redação “50 perfis observados” e “mais de 10 mil comentários registrados” foi removida.

### 3. Contextos e agendas sem suporte nos controles vigentes

Foram retiradas da versão corrigida, como afirmações de situação atual:

- associação factual da primeira aplicação à Parada LGBT+ de 2026;
- validações de cofre atribuídas a ChatGPT ou Codex;
- conclusão da denominada Fase III;
- encaminhamento documentado a quatro organizações;
- expansão definida para Brasília ou para evento específico;
- registro de marca, artigo, vídeo e premiação como etapas em andamento.

Esses elementos poderão voltar a um documento futuro somente quando possuírem decisão, fonte, estado e responsável registrados.

### 4. Anonimização afirmada de forma excessiva

As camadas históricas brutas e tratadas preservam dados identificáveis. Portanto, o projeto não pode ser descrito genericamente como “anonimizado”. A formulação adequada distingue:

- bruto protegido e identificável;
- base interna pseudonimizada na rodada prospectiva;
- pacote público sanitizado e sujeito a gate.

### 5. Evidência e auditabilidade superestimadas

A rodada inicial produziu artefatos organizados e possui rastreabilidade relevante nas etapas iniciais, mas a linhagem se degrada depois das matrizes por lote e faltam scripts de consolidação e painéis. Assim, “evidência auditável” não pode ser usada como qualidade uniforme de todo o ciclo histórico.

### 6. Inventário histórico apresentado como estado atual

O relatório de sanitização informa 258 arquivos e aproximadamente 108,5 milhões de bytes. Esse número pertence ao inventário executado na sanitização original. A MDN-RPP01 e o pipeline V2 foram criados depois. A versão corrigida conserva o valor apenas como declaração do snapshot histórico, não como contagem atual do repositório.

### 7. Teste de sanitização sem reexecução independente

O relatório original registra confronto automatizado com identificadores e comentários. Nesta revisão não foram lidas nem reprocessadas as bases dos lotes para repetir o confronto. Foram verificados estrutura, consistência documental e padrões sintáticos nos documentos, preservando a restrição de não reprocessamento.

### 8. Circulação ainda bloqueada

Os documentos reconhecem riscos de células pequenas, pesquisa reversa e entidades. Como `G4_publication` permanece falso, segundo revisor, métricas por frente e registro de liberação continuam pendentes. Nenhum dos documentos pode ser tratado como produto público.

## Matriz de conformidade com a MDN-RPP01

| Critério | Relatório recebido | Documento técnico recebido | Resultado corrigido |
|---|---|---|---|
| Separação da rodada inicial | parcial | parcial | explícita |
| Proibição de reprocessamento retrospectivo | conforme | conforme | mantida |
| Distinção entre declaração e evidência | conforme | parcial | explícita |
| 50 perfis e 10.000 como meta | não aplicável | não conforme | corrigido |
| Taxonomia V1.1 não retroativa | conforme | conforme | mantida |
| Abstenção e `nao_determinado` prospectivos | ausente | insuficiente | incorporado |
| Bruto protegido e base interna pseudonimizada | parcial | não conforme | corrigido |
| Nenhuma exclusão invisível na nova rodada | não aplicável | parcial | incorporado |
| Linhagem relacional prospectiva | ausente | citada apenas como intenção | incorporada como controle implantado e ainda não testado em dados reais |
| Validação humana e segundo revisor | parcial | parcial | pendências explícitas |
| Publicação condicionada a G4 | conforme | conforme | reforçado |
| Ausência de causalidade e representatividade | conforme | conforme | mantida |
| Separação entre produto interno e público | conforme | parcial | corrigido |
| Estado atual dos gates | ausente | desatualizado | incorporado |
| Estado atual da coleta | ausente | ambíguo | corrigido para nenhuma coleta real na MDN-RPP01 |

## Correções produzidas

- `MDN-RPP01-SAN-001-V0.1.md`: versão controlada e reenquadrada do relatório histórico de sanitização;
- `MDN-RPP01-TEC-001-V0.1.md`: consolidação técnica corrigida e alinhada ao estado atual;
- este relatório de auditoria, que preserva as razões das alterações.

## Limite da validação

O resultado é **conformidade documental condicionada**, não aprovação metodológica total. Os documentos corrigidos são coerentes com os controles existentes, mas não preenchem as pendências de G0, não validam resultados da nova rodada e não autorizam G4.

