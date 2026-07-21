# MDN-RPP01-FON-DIAG-001-V0.1 — Diagnóstico da planilha apresentada como fontes

## Controle

- Data da leitura: 16/07/2026
- Operação: leitura somente; nenhuma célula editada
- Artefato: Google Sheets fornecido pelo responsável do projeto
- Título observado: `Perfis Instagram`
- Aba observada: `Sheet1`, `sheetId 1387839138`
- Intervalo inspecionado: `E1:F1949`
- Cabeçalhos: `Profile URL` e `User Name`
- Circulação: interna; este diagnóstico não reproduz URLs ou nomes de usuário

## Resultado estrutural

| Medida | Resultado |
|---|---:|
| Linhas de dados | 1.948 |
| URLs de perfil únicas | 1.544 |
| Ocorrências duplicadas | 404 |
| URLs distintas que aparecem mais de uma vez | 244 |
| URLs com formato divergente do padrão Instagram observado | 0 |
| Divergências entre slug da URL e `User Name` | 0 |

## Classificação metodológica

O conteúdo é compatível com uma lista de perfis de usuários ou comentaristas extraídos. Não é compatível com o inventário prévio de fontes da MDN-RPP01, que exige uma linha por publicação pública — ou, antes de sua seleção final, por conta-fonte do circuito — com justificativa, período, contexto e situação de aprovação.

A repetição de perfis é esperada em uma lista derivada de comentários, mas confirma que a unidade registrada é o usuário que comentou, não a publicação onde os comentários serão coletados.

## Decisão

- A planilha não será importada para `MDN-RPP01-FON-001`.
- Nenhum perfil nela contido será presumido como fonte de observação.
- Nenhum URL individual será copiado para arquivo versionado.
- A planilha poderá ser preservada apenas como referência protegida de origem, sem uso para selecionar fontes.
- O item `Fontes previstas preenchidas` permanece pendente em G0.

## Estrutura exigida para substituição

A nova lista deverá conter, para cada publicação ou conta-fonte candidata:

- URL protegida da publicação ou conta;
- tipo de fonte: publicação ou conta candidata;
- pertinência ao Tribal House em São Paulo;
- contexto: clube fechado, `open air` ou não determinado;
- período ou data relevante;
- justificativa de inclusão;
- regra de exclusão aplicável;
- situação: candidata, aprovada, rejeitada ou cancelada;
- responsável e data da decisão.

Até esse recebimento, nenhuma tentativa de coleta está autorizada.

