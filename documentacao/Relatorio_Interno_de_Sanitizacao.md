# Relatório Interno de Sanitização — Caderno Metodológico Externo

## 1. Status

**Controle interno. Não aprovado para circulação externa.**

Este relatório registra as fontes usadas, as decisões de sanitização e os riscos remanescentes do caderno metodológico. Nenhuma base, planilha, matriz, regra, script, log, taxonomia ou painel foi alterado. Somente os dois documentos da pasta `documentacao` foram substituídos.

## 2. Escopo documental examinado

O inventário, excluídos os dois documentos substituídos e o arquivo temporário de auditoria, contém 258 arquivos originais, com aproximadamente 108,5 milhões de bytes.

Foram examinadas as seguintes classes:

- instruções do projeto e contexto metodológico;
- lista de entrada;
- diagnósticos técnicos;
- planilhas brutas e cópias por lote;
- bases padronizadas, tratadas, consolidadas e limpas;
- logs de exclusão;
- regras YAML e scripts Python;
- classificações, frequências, tópicos e amostras;
- matrizes por lote, consolidação e agrupamento executivo;
- documentos de entrega e validação;
- dados, código e registros do painel interno;
- dados, código, decisões e registros do painel público;
- testes com agentes de apoio e validação humana pontual;
- artefatos de exemplos e filtro nominal específico.

O caderno anterior não foi adotado como base textual, editorial ou probatória. As afirmações foram confrontadas com artefatos originais e, quando não documentadas, atribuídas à declaração retrospectiva fornecida pelo responsável.

## 3. Declarações retrospectivas incorporadas

Foram integradas, nas seções correspondentes do caderno:

1. seleção intencional, exploratória, não probabilística e por julgamento;
2. critérios informais de relevância, notoriedade, presença social, engajamento, amplitude e reconhecimento;
3. inexistência de protocolo, pontuação, marco amostral ou referência formal prévia;
4. coleta integralmente realizada pelo responsável em computador pessoal;
5. cópia dos endereços e exportação por extensão do Chrome;
6. ausência de memória e registros sobre nome, edição, configuração, paginação, autenticação, respostas, limites e falhas da extensão;
7. ausência de explicação segura para 19 endereços e 15 exportações;
8. criação posterior e progressiva da Taxonomia Mestre diante da insuficiência percebida da estrutura inicial;
9. razão para exclusão de comentários somente com emoji e reconhecimento da possível perda de sinais;
10. autoria individual, experimentação progressiva, pesquisa pessoal e ausência de formação ou protocolo especializado declarado;
11. uso do Codex como apoio organizacional, computacional, analítico e documental, sem autonomia ou decisão final;
12. intenção de submeter o trabalho a avaliação crítica externa.

Nenhuma declaração retrospectiva foi convertida em prova documental. O caderno usa qualificação explícita de fonte.

## 4. Confronto de afirmações centrais

| Afirmação | Evidência | Resultado de sanitização |
|---|---|---|
| 19 endereços na lista | Arquivo de entrada | Mantida apenas a contagem |
| 15 exportações em três lotes | Pastas bruta e de lotes | Mantidas contagens; nomes removidos |
| Arquivos brutos e cópias são idênticos | Comparação por nome e hash | Mantida conclusão agregada; hashes não expostos |
| 3.720 linhas de entrada | Relatórios e bases tratadas | Mantida contagem agregada |
| 3.325 preservadas e 395 excluídas | Bases limpas e logs | Mantidas contagens e motivos agregados |
| 366 exclusões por emoji | Logs | Mantida contagem; nenhum conteúdo reproduzido |
| 30 categorias nas regras iniciais | Arquivos YAML | Mantidas contagens agregadas |
| 1.533 grupos por lote, 1.000 consolidados e 39 executivos | Matrizes e relatórios | Mantida cadeia quantitativa |
| 14 rótulos e 13 proxies | Base padronizada e painel | Mantida divergência sem nomes |
| 3.325 linhas e 3.032 linhas do painel | Base limpa e painel | Mantida divergência sem inferência |
| Rastreabilidade degradada após matrizes por lote | Campos de origem nas matrizes | Explicada sem reproduzir chaves ou arquivos |
| Ausência de scripts posteriores | Inventário de scripts | Mantida lacuna de reprodução |
| Impedimento seguido de implementação pública | Registros de governança | Mantida transição sem pessoas ou datas |

## 5. Exposição identificável nas fontes

### 5.1 Camadas brutas e tratadas

As 3.720 linhas tratadas preservam campos de identificação, nome de usuário e endereços de perfil e avatar. Foram observados, em contagem agregada:

- 2.553 identificadores de usuário distintos;
- 2.553 nomes de usuário distintos;
- 2.553 endereços de perfil distintos;
- 3.191 endereços de avatar distintos.

Esses valores não aparecem no caderno externo. Os nomes das 15 exportações também foram omitidos porque incorporam rótulos de perfis ou recortes.

### 5.2 Logs, classificações e matrizes

Os logs de exclusão preservam usuário, comentário, arquivo e linha. As classificações e matrizes mantêm texto literal, origem e identificadores compostos. Os exemplos derivados incluem fragmentos e combinações de lote, arquivo, data e tema. Por isso, esses materiais devem permanecer internos.

### 5.3 Painel interno

O JSON interno contém 1.039 objetos com campo de evidência textual. Uma varredura simples encontrou 1.623 ocorrências com sintaxe de menção por arroba. A contagem é um indicador de exposição técnica, não uma contagem validada de pessoas únicas.

### 5.4 Painel público existente

No JSON público, a varredura sintática simples encontrou:

- menções por arroba: 0;
- endereços web: 0;
- endereços de e-mail: 0;
- padrões de telefone: 0.

Essa ausência não equivale a anonimização robusta. O mesmo arquivo contém 40 entidades, rankings, temas associados, evidências e contagens potencialmente pequenas. Também existem nomes de artistas ou recortes em estruturas de consulta. A combinação pode permitir pesquisa reversa ou reidentificação contextual.

## 6. Decisões de sanitização do caderno

Foram aplicadas as seguintes regras:

- nenhuma pessoa, usuário, perfil, artista, evento ou entidade rara foi nomeada;
- nenhum endereço de publicação, perfil, avatar ou página foi reproduzido;
- nenhum identificador, hash ou chave de origem foi exposto;
- nenhum comentário ou fragmento pesquisável foi citado;
- nenhum nome de arquivo de exportação foi reproduzido;
- nenhum caminho absoluto, nome de usuário do computador ou estrutura privada foi incluído;
- nenhuma data ou hora precisa foi incluída;
- exemplos reais foram substituídos por descrição abstrata;
- quantidades foram mantidas somente quando necessárias à auditoria metodológica;
- a Taxonomia Mestre foi descrita por frentes gerais, sem afirmar aplicação retroativa;
- as declarações do responsável foram qualificadas como retrospectivas;
- lacunas foram marcadas como indeterminações, sem hipóteses;
- automação, apoio computacional, apoio analítico e decisão humana foram separados;
- não se afirmou validação científica ou conformidade jurídica definitiva.

## 7. Termos e enquadramentos bloqueados

O caderno evita:

- representatividade estatística;
- generalização populacional;
- causalidade comprovada;
- responsabilização de pessoas ou organizações;
- desempenho individual;
- prova, laudo ou diagnóstico;
- autonomia decisória do Codex;
- conformidade definitiva com a legislação de proteção de dados;
- equivalência entre dado público e autorização de republicação;
- equivalência entre neutralidade lexical e ausência de sentimento;
- descrição da Taxonomia Mestre como regra aplicada desde o início.

## 8. Lacunas preservadas

Permanecem explicitamente não resolvidas:

- ausência de protocolo contemporâneo de seleção;
- ausência dos metadados e logs da ferramenta de coleta;
- ausência de explicação para a diferença entre 19 e 15;
- impossibilidade de medir perdas da coleta;
- perda potencial decorrente da exclusão de 366 comentários somente com emoji;
- ausência da regra de transformação de 14 rótulos em 13 proxies;
- ausência da correspondência entre 3.325 e 3.032;
- degradação dos identificadores compostos depois das matrizes por lote;
- ausência dos scripts de consolidação, agrupamento executivo e geração dos painéis;
- documentação insuficiente do processo geral de validação humana;
- configuração não preservada dos testes com agentes de apoio;
- ausência do registro que autoriza a passagem do impedimento à implementação pública.

## 9. Risco remanescente

O caderno externo foi generalizado, mas qualquer circulação deve considerar:

- possibilidade de associação do projeto ao universo social estudado;
- sensibilidade dos temas abordados pela Taxonomia Mestre;
- risco de que contagens raras sejam combinadas com conhecimento externo;
- risco de interpretação promocional de resultados exploratórios;
- risco de confundir recomendações automáticas com decisão implementada;
- risco jurídico e ético ainda não avaliado por especialista.

O documento não deve ser anexado a uma base, painel ou pacote que exponha os elementos omitidos, pois a combinação entre materiais pode desfazer a sanitização.

## 10. Critério de liberação

A circulação externa só deve ocorrer após confirmação humana de que:

1. a finalidade da circulação está definida;
2. o público destinatário está delimitado;
3. não serão anexados dados identificáveis;
4. entidades, rankings e células pequenas foram retirados ou avaliados;
5. as lacunas metodológicas permanecem visíveis;
6. não há alegação de representatividade, causalidade ou validação científica;
7. a proteção de dados recebeu avaliação adequada ao contexto;
8. o responsável aprovou o texto final.

## 11. Varredura quantitativa dos documentos gerados

Foi executado confronto automatizado dos dois documentos com nomes de usuário, identificadores, endereços de perfil e avatar, nomes das exportações, entidades nomeadas no JSON público e comentários das bases tratadas. Também foram testados comentários integrais e janelas de dez palavras com extensão mínima suficiente para pesquisa reversa.

| Categoria verificada | Caderno externo | Relatório interno |
|---|---:|---:|
| Nomes, perfis, identificadores, nomes de exportação ou entidades específicas | 0 | 0 |
| Comentários integrais coincidentes | 0 | 0 |
| Fragmentos coincidentes de dez palavras | 0 | 0 |
| Menções por arroba | 0 | 0 |
| Endereços web | 0 | 0 |
| Endereços de e-mail | 0 | 0 |
| Padrões de telefone | 0 | 0 |
| Caminhos absolutos locais ou de rede | 0 | 0 |
| Datas precisas | 0 | 0 |
| Horas precisas | 0 | 0 |
| Identificadores numéricos longos | 0 | 0 |
| Marcadores editoriais proibidos | 0 | 0 |
| Alegações afirmativas de validação científica | 0 | 0 |

A busca por entidades excluiu somente o nome do próprio projeto, necessário ao título e ao objeto documental. Ocorrências genéricas de termos como “identificador”, “endereço” e “perfil” descrevem classes de risco e não reproduzem valores de origem.

## 12. Resultado

O caderno foi produzido em linguagem técnica e não promocional, com separação contínua entre evidência documental, declaração retrospectiva e indeterminação. Ele contém somente números agregados e descrições abstratas.

**Situação:** sanitização documental concluída; circulação externa ainda não autorizada.
