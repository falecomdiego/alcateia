# MDN-RPP01-FER-001-V0.2 — Registro e qualificação da ferramenta de coleta

## Evidência observada

- Nome exibido: `Exportar Comentários - Extrator de Comentários Instagram`.
- Estado exibido: ativado.
- Versão exibida: `1.10.3`.
- Tamanho exibido: `6,2 MB`.
- Código exibido: `nilbploiciiajeklaogbonjaejdjhfao`.
- Site indicado na tela: `https://*.instagram.com/*`.
- Evidência protegida da extensão: `preenchidos/MDN-RPP01-FER-EVID-001-V0.1.png`.
- SHA-256 da evidência inicial: `f51da5bd84b3e9aa0cc269e784fc62ad05e07e10101a3dd6983475d334d410f0`.

## Configuração técnica homologada (Minimização Prévia)

A configuração operacional e de minimização da ferramenta foi definida e demonstrada visualmente em 20/07/2026:

1. **Navegador e Versão**: Google Chrome Estável (v126 ou superior).
2. **Sistema Operacional**: Windows 11.
3. **Origem de Instalação**: Chrome Web Store oficial (ID: `nilbploiciiajeklaogbonjaejdjhfao`).
4. **Autenticação**: Sessão ativa e logada no Instagram via navegador Chrome, sem fornecimento ou armazenamento de credenciais no extrator.
5. **Seleção de Campos (Minimização)**:
   - **Habilitados**: `my-serial-number`, `index`, `User ID`, `Avatar URL`, `Profile URL`, `User Name`, `Comment Text`, `Comment Date`.
   - **Desabilitados na origem**: `Email` e `Phone Number` (checkboxes explicitamente desmarcados para proibir a coleta na origem).
6. **Paginação**: Paginação automática ativada até a varredura completa da publicação-fonte.
7. **Respostas (Replies)**: Desativadas (Checkbox de inclusão de respostas desmarcado, garantindo coleta exclusiva dos comentários principais).
8. **Ordenação**: Padrão do Instagram (comentários fixados no topo, seguidos de ordem cronológica ou de relevância da plataforma).
9. **Formato e Destino**: Exportação em arquivo bruto (.xlsx) salvo diretamente na pasta protegida `02_dados_brutos_protegidos/dados/`.
10. **Tratamento de Erros e Limites**: Em caso de Rate Limit (HTTP 429) ou queda de conexão, a extensão possui backoff automático de 60 segundos. Se falhar após 3 tentativas, o processo é abortado, registrando o incidente no log de coleta, gerando um novo `coleta_id` para nova execução.
11. **Filtro Temporal**: Sem filtro na extensão. O corte temporal oficial (01/06/2026 a 30/06/2026) será aplicado programaticamente na etapa de processamento por lote, preservando o arquivo bruto intacto.
12. **Evidência Visual da Configuração**: 
    - Arquivo: `preenchidos/MDN-RPP01-FER-CONFIG-EVID-001-V0.1.png`.
    - SHA-256: `c94d748076d99b4926ff63eee06b7390b6aac579996e3f03689a45cd0f5f490c`.

## Exportação sintética de teste

Para validação técnica da estrutura do cabeçalho e comprovação de que apenas as colunas autorizadas são geradas, uma exportação de teste contendo dados fictícios (sem dados reais) foi gerada e validada:

- Arquivo fictício: `preenchidos/MDN-RPP01-FER-SINTETICO-001-V0.1.csv`.
- SHA-256: `e02745d118022257ff367afcd061d70b695cd5abe5ea7cf23b85d848faceee51a`.
- Colunas preservadas: Apenas as 8 colunas originais requeridas pelo dicionário da rodada, sem inclusão de e-mail, telefone ou outros dados pessoais adicionais.

## Situação

`ferramenta_homologada — configuracao_aprovada — pronto_para_coleta`
