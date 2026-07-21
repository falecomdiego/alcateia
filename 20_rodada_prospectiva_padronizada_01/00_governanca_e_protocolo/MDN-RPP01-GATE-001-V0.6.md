# MDN-RPP01-GATE-001-V0.6 — Checklist mestre de gates

Marcar um item não altera automaticamente a configuração. A alteração do gate deve possuir decisão registrada e aprovação nominal.

## G0 — Protocolo

- [x] Período de referência definido: 01/06/2026 a 30/06/2026.
- [x] Ampliação temporal justificada, datada e aplicada uniformemente a todas as fontes.
- [x] Pergunta central e subperguntas operacionalizadas no manifesto.
- [x] Fontes previstas preenchidas: 30 publicações específicas registradas em inventário protegido, com URL, conta-fonte, tipo, contexto, justificativa, período e data.
- [x] Critérios de inclusão e exclusão definidos no manifesto.
- [x] Ferramenta identificada, com configuração técnica homologada (script Python + Instaloader) e exportação sintética de teste validada.
- [x] Papéis identificados nominalmente; funções metodológica, proteção de dados e publicação atribuídas a Diego Silva.
- [x] Retenção definida em 12 meses; lista de acesso nominal, local das cópias principal/segurança e política de descarte estruturadas.
- [x] Taxonomia Mestre V1.1 congelada e hash registrado.
- [x] Matriz de riscos criada.
- [x] Dicionário de dados atualizado com retenção e papéis funcionais.
- [x] Aceite direto da revisora independente Kacia Oliveira confirmado e registrado.
- [x] Decisão formal `G0 = aprovado` registrada.

## G1 — Coleta

- [x] G0 aprovado.
- [x] Toda fonte possui `fonte_id`.
- [x] Toda tentativa possui `coleta_id` e resultado.
- [x] Todo XLSX/CSV bruto possui hash e vínculo com a fonte.
- [x] Diferenças entre previsto e coletado estão explicadas (30/30 fontes previstas coletadas integralmente).
- [x] Decisão formal `G1 = aprovado` registrada (MDN-RPP01-DEC-0015).

## G2 — Análise por lote

- [ ] Lote explicitamente autorizado.
- [ ] Diagnóstico estrutural sem divergência bloqueante.
- [ ] Balanço de limpeza fechado.
- [ ] Taxonomia e configuração conferidas por hash.
- [ ] Casos sensíveis enviados à validação humana.
- [ ] Decisão formal `G2 = aprovado` registrada.

## G3 — Consolidação

- [ ] Todos os lotes incluídos estão encerrados.
- [ ] `registro_id` único em toda a rodada.
- [ ] Cada vínculo `grupo_registro` é válido.
- [ ] Volumes dos grupos reuniões.
- [ ] Matriz de evidências preenchida.
- [ ] Decisão formal `G3 = aprovado` registrada.

## G4 — Publicação

- [ ] Segundo revisor identificado e com aceite registrado.
- [ ] Amostra e sobreposição concluídas.
- [ ] Classificações publicadas atingem precisão mínima.
- [ ] Células menores que cinco suprimidas ou agregadas.
- [ ] Não há comentários literais ou identificadores.
- [ ] Riscos remanescentes registrados.
- [ ] Registro nominal e datado de liberação.

## G5 — Reaplicação

- [ ] Terceiro recebeu apenas o pacote autorizado.
- [ ] Fixture executada com resultados esperados.
- [ ] Dúvidas e falhas foram registradas.
- [ ] Lacunas documentais foram corrigidas em nova versão.
- [ ] Decisão formal `G5 = aprovado` registrada.
