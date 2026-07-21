# MDN-RPP01-PRO-COL-001-V0.1 — Protocolo de seleção e coleta

## Estado

Coleta bloqueada até aprovação G0. Este documento não autoriza acessar, exportar ou processar nenhuma fonte.

## Antes de cada tentativa

1. Confirmar que a fonte está aprovada no inventário.
2. Atribuir `coleta_id` único.
3. Registrar ferramenta, versão, configuração, autenticação, paginação e captura de respostas.
4. Registrar data, horário, fuso e operador.
5. Confirmar pasta protegida de destino.

## Depois de cada tentativa

1. Registrar sucesso, falha ou cancelamento.
2. Se houver arquivo, calcular SHA-256 sem alterar o XLSX.
3. Registrar número de linhas observado tecnicamente.
4. Vincular exatamente um arquivo ao resultado correspondente ou explicar a ausência.
5. Nunca substituir um arquivo anterior; nova tentativa recebe novo `coleta_id`.

## Formação de lotes

- Os lotes serão definidos somente depois do inventário de coletas concluídas.
- Cada arquivo terá uma única associação ativa de lote.
- O manifesto de lote listará `fonte_id`, `coleta_id`, arquivo e hash.
- Cada lote será autorizado e processado separadamente.

## Divergências bloqueantes

- ferramenta ou versão desconhecida;
- arquivo sem fonte e tentativa correspondentes;
- hash ausente ou divergente;
- cabeçalho diferente das oito colunas originais esperadas;
- quantidade de arquivos incompatível com o log sem justificativa;
- tentativa de completar lacuna por memória não registrada.

