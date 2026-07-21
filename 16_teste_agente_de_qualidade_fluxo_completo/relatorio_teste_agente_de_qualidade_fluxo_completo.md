# Teste controlado do Agente de Qualidade - fluxo completo

## Escopo

Teste executado exclusivamente na pasta derivada `16_teste_agente_de_qualidade_fluxo_completo`, sem alteracao de arquivos oficiais, bases aprovadas, matrizes, paineis ou arquivos brutos.

## Fontes autorizadas utilizadas

- `06_bases_limpas_por_lote`
- `07_classificacao_pilar2_por_lote`
- `08_pln_pilar3_por_lote`
- `09_matriz_resolutiva_por_lote`
- `10_consolidacao_rodada_inicial\matriz_resolutiva_rodada_inicial.xlsx`

## Quantidade avaliada

- Registros avaliados: 30
- Distribuicao por lote: {'lote_01': 10, 'lote_02': 10, 'lote_03': 10}
- Todos os registros possuem vinculo com resolucao aprovada por lote e com a matriz consolidada aprovada: sim

## Cobertura da amostra

- Prioridade original: {'media': 8, 'baixa': 11, 'monitorar': 11}
- Natureza original: {'experiencia_intangivel': 10, 'mista': 8, 'operacao_tangivel': 11, 'indefinida': 1}
- Polaridade original: {'neutra': 8, 'negativa': 13, 'positiva': 6, 'ambivalente': 3}
- Prioridade no teste: {'media': 8, 'baixa': 18, 'monitorar': 4}
- Natureza no teste: {'experiencia_intangivel': 13, 'mista': 10, 'indefinida': 5, 'operacao_tangivel': 2}
- Grau de mudanca no comparativo: {'mudanca_moderada': 10, 'mudanca_relevante': 20}

Observacao metodologica: nao foram encontrados casos com prioridade original `alta` nas matrizes aprovadas usadas como fonte; por isso, o teste preservou apenas as prioridades existentes na rodada.

## Arquivos gerados

1. `amostra_base_teste_agente_de_qualidade.xlsx`
2. `reclassificacao_teste_agente_de_qualidade.xlsx`
3. `resolucoes_teste_agente_de_qualidade.xlsx`
4. `comparativo_fluxo_original_vs_agente_de_qualidade.xlsx`
5. `relatorio_teste_agente_de_qualidade_fluxo_completo.md`

## Campos para avaliacao humana

O arquivo comparativo contem os campos em branco:

- `avaliacao_humana`
- `decisao_humana`
- `observacao_humana`

## Blindagem

- Ambiente de teste: sim
- Efeito oficial sobre arquivos aprovados: nao
- Alteracao de dados, evidencias, recomendacoes ou conclusoes oficiais: nao
- Escopo valido mantido: `lote_01`, `lote_02`, `lote_03`
