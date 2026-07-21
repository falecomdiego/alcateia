# MDN-RPP01-GATE-001-V0.1 — Checklist mestre de gates

Marcar um item não altera automaticamente a configuração. A alteração do gate deve possuir decisão registrada e aprovação nominal.

## G0 — Protocolo

- [ ] Período definido.
- [ ] Perguntas orientadoras aprovadas.
- [ ] Fontes previstas preenchidas.
- [ ] Critérios de inclusão e exclusão aprovados.
- [ ] Ferramenta e procedimento de coleta definidos.
- [ ] Responsáveis identificados.
- [ ] Acessos e retenção definidos.
- [x] Taxonomia Mestre V1.1 congelada e hash registrado.
- [x] Matriz de riscos criada.
- [x] Dicionário de dados iniciado.
- [ ] Decisão formal `G0 = aprovado` registrada.

## G1 — Coleta

- [ ] G0 aprovado.
- [ ] Toda fonte possui `fonte_id`.
- [ ] Toda tentativa possui `coleta_id` e resultado.
- [ ] Todo XLSX possui hash e vínculo com a fonte.
- [ ] Diferenças entre previsto e coletado estão explicadas.
- [ ] Decisão formal `G1 = aprovado` registrada.

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
- [ ] Volumes dos grupos reconciliados.
- [ ] Matriz de evidências preenchida.
- [ ] Decisão formal `G3 = aprovado` registrada.

## G4 — Publicação

- [ ] Segundo revisor identificado.
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

