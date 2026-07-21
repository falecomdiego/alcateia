# MDN-RPP01-PRO-COL-001-V0.2 — Protocolo de seleção e coleta

## Estado

Coleta bloqueada até aprovação G0. Este documento não autoriza acessar, exportar ou processar nenhuma fonte.

## Unidade de fonte

Cada `fonte_id` representará uma publicação pública do Instagram aprovada antes da extração. Uma conta do circuito poderá entrar como candidata, mas suas publicações deverão ser selecionadas e identificadas antes da coleta. Perfil de comentarista não é fonte.

## Período

- Período de referência do comentário: 01/06/2026 a 15/06/2026, inclusive.
- Fuso: `America/Sao_Paulo`.
- Data de extração: posterior a G0 e registrada em cada tentativa.
- Registros fora do período não serão apagados do bruto; serão contabilizados e encaminhados ao log de tratamento.

## Ferramenta

- Nome: `Exportar Comentários - Extrator de Comentários Instagram`.
- Versão observada: `1.10.3`.
- Código observado: `nilbploiciiajeklaogbonjaejdjhfao`.
- Situação: identificada, mas sem configuração aprovada.
- Registro detalhado: `MDN-RPP01-FER-001-V0.1.md`.

## Minimização prévia

1. Selecionar exclusivamente as oito colunas originais previstas.
2. Desativar e-mail, telefone e qualquer campo adicional.
3. Não coletar um campo desnecessário para removê-lo depois.
4. Executar primeiro uma exportação sintética ou controlada, sem fonte real.
5. Suspender se o cabeçalho ou a configuração divergir.

## Antes de cada tentativa

1. Confirmar `G0 = true` na configuração vigente.
2. Confirmar que a publicação possui `fonte_id` aprovado no inventário.
3. Atribuir `coleta_id` único.
4. Registrar ferramenta, versão, origem de instalação e hash da evidência de configuração.
5. Registrar seleção de campos, autenticação sem credenciais, paginação, respostas, ordenação e filtro temporal.
6. Registrar data, horário, fuso e operador.
7. Confirmar pasta protegida de destino e cópia protegida.
8. Confirmar que e-mail, telefone e campos não autorizados estão desativados.

## Durante a tentativa

1. Não modificar a publicação ou interagir com usuários.
2. Não alterar manualmente o arquivo exportado.
3. Registrar interrupções, mensagens de erro e retomadas.
4. Não repetir tentativa silenciosamente.

## Depois de cada tentativa

1. Registrar sucesso, falha ou cancelamento.
2. Se houver arquivo, calcular SHA-256 sem alterar o XLSX.
3. Registrar número de linhas observado tecnicamente.
4. Vincular exatamente um arquivo ao resultado correspondente ou explicar a ausência.
5. Verificar somente o cabeçalho e a integridade técnica antes de qualquer leitura analítica.
6. Nunca substituir um arquivo anterior; nova tentativa recebe novo `coleta_id`.

## Formação de lotes

- Os lotes serão definidos somente depois do inventário de coletas concluídas.
- Cada arquivo terá uma única associação ativa de lote.
- O manifesto de lote listará `fonte_id`, `coleta_id`, arquivo e hash.
- Cada lote será autorizado e processado separadamente.

## Divergências bloqueantes

- planilha de usuários ou comentaristas apresentada como inventário de fontes;
- ferramenta, versão, origem de instalação ou configuração desconhecida;
- e-mail, telefone ou campo não autorizado presente na exportação;
- arquivo sem fonte e tentativa correspondentes;
- hash ausente ou divergente;
- cabeçalho diferente das oito colunas originais esperadas;
- quantidade de arquivos incompatível com o log sem justificativa;
- paginação ou respostas sem regra registrada;
- tentativa de completar lacuna por memória não registrada.

