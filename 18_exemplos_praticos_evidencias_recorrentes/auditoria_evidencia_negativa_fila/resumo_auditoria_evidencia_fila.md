# Resumo da auditoria — evidência fila

## Concentração da evidência

### A evidência está concentrada em uma única festa?

Não é possível afirmar. Campo literal de festa/evento não disponível na base atual.

### A evidência está concentrada em um único post?

Não é possível afirmar concentração por post. A coluna `url_postagem` existe, mas está sem informação útil nos 40 registros da evidência.

### A evidência está concentrada em um único lote?

Não. Distribuição por lote:

- lote_01: 10
- lote_02: 29
- lote_03: 1

### A evidência está distribuída em múltiplas fontes?

Sim. Distribuição por arquivo de origem:

- IGComment-All_20260615192942_oimperfeitinho.xlsx: 10
- IGComment-All_20260615194141_oimperfeitinho_guapo.xlsx: 29
- IGComment-All_20260616033837_kiki_klub_BIGGER.xlsx: 1

### O dado permite direcionamento para um responsável específico?

Não de forma pública ou automática. O campo `responsavel_sugerido` da matriz indica operação, mas a responsabilização específica exige validação interna.

### O dado exige validação interna antes de qualquer responsabilização?

Sim. A evidência exige validação interna antes de qualquer responsabilização por festa, produção, espaço, equipe ou operação específica.

## Classificação da robustez

Nível: Média robustez contextual.

Justificativa: Há recorrência quantitativa, vínculo por id_registro, lote, arquivo de origem, perfil_monitorado e data_comentario. Parte dos campos de origem está ausente ou sem valor útil nos registros desta evidência: url_postagem, data_postagem, festa_evento e data_evento. Por isso a robustez é média: suficiente para afirmar recorrência no universo analisado, mas insuficiente para atribuir o problema a uma festa, postagem ou data específica sem validação interna.

## Campos disponíveis

- id_registro: 1
- lote: 1
- arquivo_origem: 1
- linha_origem: 1
- comentario_anonimizado: 1
- tema: 1
- categoria: 1
- natureza: 1
- polaridade: 1
- agrupamento: 1
- impacto: 1
- recomendacao: 1
- perfil_monitorado: 1
- conta_identificada: 1
- data_comentario: 1
- entidade_associada/entidade_monitorada: 1

## Campos não disponíveis

- festa_evento literal: 1
- data_evento: 1
- url_postagem com valor útil para estes 40 registros: 1
- data_postagem com valor útil para estes 40 registros: 1
- causa operacional exata: 1
- responsável específico validado: 1
