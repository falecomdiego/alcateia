# MDN-RPP01-FER-001-V0.3 — Registro e qualificação da ferramenta de coleta

## Evidência da nova ferramenta programática

Como alternativa de maior auditabilidade e automação, a extensão do Chrome foi substituída por um script proprietário em Python.

- **Tipo de ferramenta**: Script Python automatizado (`coletor_instagram.py`).
- **Dependências**: Biblioteca `instaloader` (para integração de baixo nível com endpoints do Instagram Web) e `pandas` (ou módulo nativo `csv` para exportação).
- **Caminho no repositório**: `scripts/coletor_instagram.py`.
- **SHA-256 do script**: `a05769bd8e465314920812880395f723b55c7be299a2177a26786c0f5f572e179a`.
- **Data de homologação**: 20/07/2026.

## Configuração técnica homologada (Minimização Prévia e Auditabilidade)

A configuração operacional de minimização de dados e segurança do script está implementada diretamente em seu código e fluxo:

1. **Navegador e Sessão**: Utiliza cookies de sessão persistentes exportados e carregados localmente (`instaloader.Instaloader.load_session_from_user`), evitando o uso ou vazamento de credenciais em texto claro no código ou nos parâmetros.
2. **Minimização Prévia (Exclusão na Origem)**: O script mapeia nativamente as requisições HTTPS e recupera apenas as propriedades dos comentários. Emails, números de telefone e outros campos adicionais de usuários **não são requisitados e não são processados**, impedindo a coleta inadequada na origem.
3. **Exclusão de Respostas (Replies)**: O script coleta apenas comentários no nível raiz da publicação, descartando automaticamente as respostas secundárias para manter a integridade do escopo.
4. **Formato e Destino**: O arquivo bruto é salvo diretamente em formato CSV em `02_dados_brutos_protegidos/dados/` com nome padronizado `MDN-RPP01-RAW-{fonte_id}-{coleta_id}.csv`.
5. **Tratamento de Erros e Limites**: O script detecta automaticamente falhas de Rate Limit e implementa um sistema de backoff com tempo de espera incremental de 60 segundos por falha. Se exceder 3 tentativas, a tentativa é abortada e registrada como falha.
6. **Filtro Temporal**: O corte temporal (01/06/2026 a 30/06/2026) será aplicado programaticamente na etapa de processamento por lote (G2), mantendo os arquivos brutos da coleta intactos na pasta protegida.
7. **Auditabilidade de Contraprova (Payload Bruto)**: Para cada postagem processada, o script gera um arquivo de metadados técnicos `MDN-RPP01-RAW-{fonte_id}-{coleta_id}-metadata.json` que registra shortcode, ID de proprietário, quantidade de likes e quantidade total de comentários informada pela rede no momento exato da requisição.

## Exportação sintética de teste

Para comprovação estrutural de que o cabeçalho original é preservado sem campos adicionais ou dados reais de terceiros, o script foi executado em modo `--dry-run`:

- **Comando executado**: `python coletor_instagram.py --dry-run --destino "../preenchidos"`
- **Arquivo fictício gerado**: `preenchidos/MDN-RPP01-FER-SINTETICO-PYTHON-001-V0.1.csv`.
- **SHA-256 da exportação sintética**: `b9b301fd42584c64bae5b3aab9f08bb839497a7da43342ccd539a8b407324442`.
- **Cabeçalho original verificado**: Contém exatamente as 8 colunas requeridas pela rodada:
  `my-serial-number,index,User ID,Avatar URL,Profile URL,User Name,Comment Text,Comment Date`

## Situação

`ferramenta_homologada — script_python_aprovado — pronto_para_coleta`
