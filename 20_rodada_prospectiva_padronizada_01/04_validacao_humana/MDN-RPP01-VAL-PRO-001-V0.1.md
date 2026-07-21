# MDN-RPP01-VAL-PRO-001-V0.1 — Protocolo de validação humana

## População elegível

Registros mantidos para classificação textual. Itens fora da classificação textual permanecem no balanço, mas não recebem frente automática.

## Amostra geral

Para `N` registros elegíveis:

`n = min(N, max(200, teto(0,10 × N)))`

A seleção deve ser determinística e estratificada por lote, fonte, frente sugerida, `nao_determinado`, grau de evidência e marcador sensível.

## Dupla revisão

Pelo menos 20% da amostra geral será revisada independentemente por duas pessoas. A divergência não será apagada; receberá decisão de adjudicação própria.

## Revisão integral obrigatória

- vocabulário sociocultural, ironia, deboche ou gíria ambígua;
- saúde, substâncias, chemsex ou redução de danos;
- acusação, violência ou risco reputacional;
- comparação externa;
- alteração de polaridade, natureza, categoria ou prioridade;
- criação de recomendação ou resolução;
- qualquer evidência proposta para circulação pública.

## Estados permitidos

- `pendente`;
- `validada`;
- `rejeitada`;
- `ajustada`;
- `nao_determinado`.

## Regra pública

Uma frente somente pode sustentar afirmação externa se alcançar precisão mínima de 85% no conjunto humano de referência e se todos os itens sensíveis relacionados estiverem aprovados. A aprovação de uma frente não autoriza comentário literal, identificação, causalidade ou representatividade.

## Limite

Sem segundo revisor, a rodada pode encerrar produto interno, mas G4 permanece bloqueado.

