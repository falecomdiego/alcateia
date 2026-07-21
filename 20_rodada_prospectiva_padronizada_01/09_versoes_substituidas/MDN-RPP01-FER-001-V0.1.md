# MDN-RPP01-FER-001-V0.1 — Registro e qualificação da ferramenta de coleta

## Evidência observada

- Nome exibido: `Exportar Comentários - Extrator de Comentários Instagram`.
- Estado exibido: ativado.
- Versão exibida: `1.10.3`.
- Tamanho exibido: `6,2 MB`.
- Código exibido: `nilbploiciiajeklaogbonjaejdjhfao`.
- Site indicado na tela: `https://*.instagram.com/*`.
- Evidência protegida: `preenchidos/MDN-RPP01-FER-EVID-001-V0.1.png`.
- SHA-256: `f51da5bd84b3e9aa0cc269e784fc62ad05e07e10101a3dd6983475d334d410f0`.

## Limite da evidência

A imagem comprova apenas identificação, versão e elementos visíveis de acesso da extensão. Ela não comprova:

- origem ou integridade do código da extensão;
- configuração aplicada à exportação;
- completude da paginação;
- captura ou não de respostas;
- ordem dos comentários;
- comportamento diante de falhas;
- campos efetivamente exportados;
- filtro temporal;
- autenticação utilizada;
- aderência jurídica ou às regras da plataforma.

## Risco de minimização

A descrição visível informa capacidade de extrair e-mail, telefone e outros dados. Esses campos não são necessários à pergunta da MDN-RPP01, não pertencem ao dicionário e ficam proibidos.

## Configuração mínima ainda exigida

Antes de G0, registrar:

1. navegador e versão;
2. sistema operacional;
3. origem de instalação da extensão;
4. conta ou tipo de autenticação, sem registrar credenciais;
5. seleção exata de campos;
6. regra de paginação e limite por tentativa;
7. inclusão ou exclusão de respostas;
8. ordenação e comportamento com comentários fixados;
9. formato, nome e local protegido do arquivo;
10. tratamento de erro, interrupção e repetição;
11. capacidade ou procedimento de filtro por `Comment Date`;
12. evidência de uma exportação sintética sem dados reais.

## Cabeçalho permitido

A exportação aceita pela rodada deverá conter exatamente as oito colunas originais esperadas:

- `my-serial-number`;
- `index`;
- `User ID`;
- `Avatar URL`;
- `Profile URL`;
- `User Name`;
- `Comment Text`;
- `Comment Date`.

Qualquer campo adicional suspende a tentativa antes da ingestão. E-mail, telefone, endereço ou outro dado não necessário não pode ser coletado para posterior remoção; deve ser desativado na origem.

## Situação

`ferramenta_identificada — configuração_pendente — coleta_bloqueada`

