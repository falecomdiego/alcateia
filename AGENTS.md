# Regras fixas do projeto

Este arquivo define as regras obrigatorias de execucao do pipeline de analise de comentarios extraidos do Instagram no projeto `analise_comentarios_evento`.

O projeto trabalha com arquivos XLSX brutos exportados por extensao do Chrome e organizados em lotes dentro da pasta:

`analise_comentarios_evento\03_lotes_processamento`

## Regras obrigatorias

1. Nao alterar, sobrescrever, editar ou apagar arquivos brutos XLSX em:
   - `analise_comentarios_evento\02_xlsx_brutos_extensao_chrome`
   - `analise_comentarios_evento\03_lotes_processamento`

2. Todo processamento deve gerar novos arquivos em pastas derivadas, mantendo os arquivos brutos intactos.

3. Antes de qualquer analise qualitativa, estrategica ou interpretativa, o pipeline deve gerar e validar bases intermediarias verificaveis.

4. Cada lote deve ser processado separadamente. O Codex nao deve ler todos os lotes de uma vez sem autorizacao explicita.

5. Cada base tratada por lote deve preservar as colunas originais encontradas nos XLSX:
   - `my-serial-number`
   - `index`
   - `User ID`
   - `Avatar URL`
   - `Profile URL`
   - `User Name`
   - `Comment Text`
   - `Comment Date`

6. Cada base tratada deve adicionar colunas de controle:
   - `lote`
   - `arquivo_origem`
   - `aba_origem`
   - `linha_origem`

7. Nenhuma exclusao de linha, comentario ou registro pode ocorrer sem geracao de log especifico informando o motivo da exclusao.

8. Comentarios duplicados, vazios, ilegiveis ou tecnicamente invalidos devem ser identificados em arquivo de log antes de qualquer remocao.

9. Toda classificacao futura deve preservar o comentario original, o arquivo de origem, o lote de origem e uma justificativa de vinculo com o eixo de classificacao.

10. O projeto deve separar claramente as etapas:
    - diagnostico tecnico dos lotes
    - padronizacao estrutural
    - consolidacao por lote
    - consolidacao parcial ou final
    - validacao tecnica
    - limpeza com log
    - classificacao tematica
    - matriz resolutiva
    - diagnostico estrategico

11. O Codex nao deve gerar diagnostico estrategico, analise reputacional, leitura de percepcao publica ou conclusao interpretativa antes de existir uma base consolidada e auditavel.

12. Todas as saidas devem ser salvas em arquivos verificaveis, preferencialmente CSV, XLSX, MD ou JSON, conforme a natureza da etapa.

13. Sempre que gerar um arquivo novo, o Codex deve informar o caminho completo, o nome do arquivo, a quantidade de linhas processadas e eventuais inconsistencias encontradas.

14. Em caso de duvida estrutural, divergencia de colunas, erro de leitura ou ambiguidade metodologica, o Codex deve parar e pedir confirmacao antes de prosseguir.

## Blindagem operacional

- Nao processar lote sem solicitacao explicita.
- Nao consolidar comentarios sem solicitacao explicita.
- Nao criar CSV tratado sem solicitacao explicita.
- Nao classificar, interpretar, resumir percepcao publica ou gerar diagnostico estrategico antes da etapa tecnicamente autorizada.
- Nao remover linhas ou registros sem log previo e verificavel.
