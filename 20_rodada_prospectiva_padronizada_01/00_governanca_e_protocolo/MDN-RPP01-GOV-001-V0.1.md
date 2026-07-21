# MDN-RPP01-GOV-001-V0.1 — Governança mínima e gates

## Princípio

Planejamento, execução, observação, interpretação, recomendação e publicação são estados distintos. Nenhum estado posterior poderá ser usado para reescrever silenciosamente o anterior.

## Papéis mínimos

| Papel | Responsabilidade | Poder de bloqueio |
|---|---|---|
| Responsável da rodada | autorizar escopo, lotes e encerramento | todos os gates |
| Operador de coleta | executar e registrar cada tentativa | G1 |
| Operador técnico | executar scripts e reconciliar contagens | G2 e G3 |
| Revisor humano | decidir casos sensíveis e discordâncias | G2 e G4 |
| Revisor independente | revisar amostra de sobreposição | G4 |
| Responsável por publicação | verificar sanitização e riscos remanescentes | G4 |

Uma pessoa pode acumular funções internas, mas não pode substituir a revisão independente necessária à circulação pública.

## Gates

### G0 — Protocolo

Exige manifesto, período, critérios, inventário previsto, papéis, matriz de riscos, dicionário e Taxonomia V1.1 congelada.

### G1 — Coleta

Exige G0, ferramenta documentada, fonte identificada, tentativa registrada, arquivo associado e hash preservado.

### G2 — Análise por lote

Exige G1, diagnóstico estrutural aprovado e autorização explícita do lote. Limpeza, classificação e validação permanecem separadas.

### G3 — Consolidação

Exige fechamento técnico de todos os lotes autorizados, balanço quantitativo e ausência de vínculos quebrados.

### G4 — Publicação

Exige produto interno validado, segundo avaliador, precisão mínima por classificação publicada, sanitização aprovada e registro de liberação.

### G5 — Reaplicação

Exige execução independente do pacote de teste, registro das dúvidas e correção das lacunas documentais.

## Diário de decisões

Toda mudança deve registrar data, questão, decisão, justificativa, participantes, documentos utilizados, impacto, artefatos afetados e condição de reversão. Decisões negativas e suspensões são obrigatórias.

## Controle de versões

- Versões publicadas não são sobrescritas.
- Correção editorial sem mudança de decisão incrementa a versão menor.
- Mudança de método, regra, gate ou schema incrementa a versão maior.
- Versões substituídas vão para `09_versoes_substituidas` com registro no índice.
- Logs de coleta, execução e decisão são anexáveis e não devem ter linhas antigas alteradas.

## Cópias e acesso

- manter uma cópia operacional e uma cópia protegida em ambiente distinto;
- restringir dados brutos, mapeamento de pseudônimos e comentários identificáveis;
- nunca versionar segredos, chaves de pseudonimização ou dados protegidos no Git público;
- verificar hashes e acessibilidade das cópias a cada encerramento de gate.

Registros preenchidos que contenham nomes, assinaturas, acessos ou informações internas devem ser gravados em `00_governanca_e_protocolo/preenchidos/`, caminho excluído do Git. Os arquivos versionados nesta pasta são modelos vazios ou registros metodológicos sem dados pessoais.
