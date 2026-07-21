# Caderno Metodológico Externo — Mapa da Noite

## Status de circulação

**Documento de trabalho para avaliação crítica externa. Não aprovado para circulação pública.**

Este caderno sistematiza o percurso metodológico preservado no repositório do projeto Mapa da Noite. Seu propósito é permitir exame independente do desenho exploratório, das operações computacionais, das decisões humanas, das lacunas documentais e dos riscos de interpretação e exposição.

O texto não afirma representatividade estatística, validação científica, conformidade jurídica definitiva, causalidade ou generalização para a população da vida noturna. A liberação para circulação externa depende de leitura final do responsável e, para matérias de proteção de dados e ética, de avaliação humana especializada.

## 1. Como as afirmações deste caderno devem ser lidas

Foram adotadas três qualificações de fonte ao longo do documento:

- **Os arquivos demonstram**: afirmação verificável em bases, regras, scripts, relatórios, logs, matrizes ou painéis preservados no repositório.
- **Segundo declaração retrospectiva do responsável**: informação fornecida depois da execução, baseada na memória e na explicação do autor do processo. Ela contextualiza decisões, mas não substitui um registro contemporâneo à execução.
- **Não foi possível determinar**: aspecto sem documentação suficiente para uma conclusão segura. Nesses casos, não se formulam hipóteses compensatórias.

O repositório foi examinado como fonte primária. A declaração retrospectiva foi integrada somente nos pontos em que esclarece autoria, intenção ou contexto não preservado pelos arquivos.

## 2. Natureza e origem do projeto

Segundo declaração retrospectiva do responsável, o Mapa da Noite nasceu de interesse investigativo próprio e foi conduzido por uma única pessoa, em processo de experimentação progressiva e pesquisa pessoal. Não houve supervisão institucional, protocolo acadêmico formal prévio, busca bibliográfica sistemática anterior ao início, equipe multidisciplinar formalizada ou formação especializada declarada em ciência de dados, métodos digitais ou processamento de linguagem natural.

Essa condição não torna o trabalho irrelevante, mas define seu estatuto: trata-se de uma **aplicação autoral exploratória, posteriormente sistematizada de modo retrospectivo**. O repositório registra esforço consistente de organização, rastreabilidade e separação entre etapas, porém não oferece base para apresentar o projeto como pesquisa probabilística, estudo acadêmico controlado ou procedimento reconhecido por avaliação científica externa.

Segundo declaração retrospectiva do responsável, a procura de laboratórios e avaliadores externos tem justamente a finalidade de submeter o percurso a crítica técnica, identificar fragilidades e orientar uma eventual formalização futura.

## 3. Construção intencional do recorte

Segundo declaração retrospectiva do responsável, a seleção das publicações foi:

- intencional;
- exploratória;
- não probabilística;
- baseada em julgamento de relevância, notoriedade, presença social, engajamento, amplitude e reconhecimento no universo observado.

Não existiram, antes da seleção, marco amostral, pontuação formal, protocolo escrito de inclusão e exclusão, comparação documentada entre candidatos ou referência metodológica adotada para amostragem. Portanto, o corpus não deve ser descrito como amostra representativa da vida noturna, do público de uma plataforma ou de qualquer população mais ampla.

Os arquivos demonstram a existência de 19 endereços de publicações em uma lista de entrada e de 15 exportações em planilha, depois distribuídas em três lotes de cinco arquivos. Não foi possível determinar a relação individual entre cada endereço e cada exportação nem explicar documentalmente a diferença de quatro unidades. O responsável declarou não possuir memória segura para preencher essa lacuna. Assim, o caderno preserva a divergência sem sugerir falha, descarte, duplicação ou qualquer outra hipótese.

## 4. Procedimento de coleta e seus limites

Segundo declaração retrospectiva do responsável, a coleta foi realizada exclusivamente por ele, em computador pessoal. O procedimento consistiu em copiar endereços de publicações e usar uma extensão do navegador Chrome para exportar comentários; os arquivos resultantes foram então organizados no repositório.

Os arquivos demonstram que as exportações têm estrutura XLSX e oito colunas originais, relacionadas a numeração, índice, identificação do usuário, endereços de avatar e perfil, nome de usuário, texto e data do comentário. Os 15 arquivos guardados na pasta bruta são idênticos, por nome e hash, às 15 cópias organizadas nos três lotes. Isso confirma a preservação dos arquivos recebidos pelo pipeline, mas não demonstra completude da captura na plataforma.

Não foi possível determinar:

- o nome ou a edição da extensão;
- sua configuração;
- o modo de autenticação;
- a paginação ou o carregamento dinâmico;
- o tratamento de respostas;
- limites impostos pela ferramenta ou pela plataforma;
- a função interna da extensão;
- a existência de tentativas malsucedidas;
- a completude dos comentários disponíveis no momento da coleta.

Segundo declaração retrospectiva do responsável, essas informações não foram preservadas e não devem ser inferidas ou reconstruídas. Em consequência, a coleta não é integralmente reproduzível apenas com o repositório.

## 5. Corpus preservado e unidade de análise

Os arquivos demonstram 3.720 linhas nos 15 XLSX organizados em três lotes:

| Lote | Arquivos | Linhas de entrada |
|---|---:|---:|
| 01 | 5 | 810 |
| 02 | 5 | 2.124 |
| 03 | 5 | 786 |
| **Total** | **15** | **3.720** |

A unidade operacional é uma linha exportada como comentário. Essa unidade não equivale necessariamente a uma pessoa, publicação, festa, evento ou experiência independente. Um mesmo usuário pode contribuir mais de uma vez; uma publicação pode reunir vários contextos; e campos necessários para identificar postagem, evento ou tipo de conteúdo foram criados na padronização, mas permaneceram sem informação útil.

Os arquivos demonstram que os dados brutos incluem elementos diretamente identificadores ou vinculáveis a perfis. Esse material é necessário à auditoria interna de origem, mas não é adequado à circulação externa sem minimização, generalização e avaliação do risco de reidentificação.

## 6. Arquitetura operacional do pipeline

O processo preservado pode ser resumido assim:

1. diagnóstico técnico separado por lote;
2. ingestão e padronização estrutural;
3. consolidação parcial dos lotes;
4. limpeza técnica com log de exclusões;
5. classificação por regras textuais;
6. refinamento lexical e organização de tópicos;
7. formação de matrizes resolutivas por lote;
8. consolidação dos agrupamentos;
9. agrupamento executivo;
10. preparação de camadas interna e pública;
11. testes controlados de apoio analítico e validação humana pontual;
12. produção de exemplos derivados e filtros documentais específicos.

As cinco primeiras operações computacionais principais — da ingestão à matriz por lote — têm scripts Python preservados. As etapas seguintes possuem resultados e relatórios, mas não os scripts de geração correspondentes.

### 6.1 Ingestão e padronização

Os arquivos demonstram que o script de ingestão lê internamente os XLSX, valida o cabeçalho esperado, preserva as oito colunas originais e acrescenta campos de controle, entre eles lote, arquivo, aba, linha de origem e identificador composto.

O processo gerou 3.720 linhas padronizadas, sem exclusão. Campos derivados sem fonte nos XLSX — como endereço da postagem, tipo de conteúdo, data da postagem, curtidas e respostas — receberam marcador de informação não disponível. Portanto, sua existência no esquema não significa que o dado tenha sido coletado.

Duas representações tratadas foram mantidas por lote: uma com estrutura próxima às colunas originais e outra com esquema ampliado. A base parcial de 3.720 linhas foi formada pela concatenação da primeira representação; a limpeza posterior usou a representação ampliada. A duplicidade de ramos não causou diferença de contagem, mas aumenta a necessidade de documentar qual ramo alimenta cada etapa.

### 6.2 Limpeza com registro de exclusões

Os arquivos demonstram que a limpeza produziu 3.325 linhas preservadas e 395 exclusões, todas acompanhadas por log. O balanço fecha exatamente em 3.720 linhas.

| Motivo técnico registrado | Quantidade |
|---|---:|
| Conteúdo apenas com emoji | 366 |
| Comentário vazio | 19 |
| Duplicidade exata no mesmo arquivo, usuário e texto | 7 |
| Sinal textual mínimo insuficiente | 3 |
| **Total** | **395** |

A regra de duplicidade é restrita à combinação de arquivo, usuário e texto. Ela não remove automaticamente repetições entre arquivos diferentes. Essa opção preserva ocorrências potencialmente distintas, mas também significa que a base não foi deduplicada por pessoa ou conteúdo em todo o corpus.

Segundo declaração retrospectiva do responsável, comentários somente com emoji foram excluídos porque se priorizou um sinal textual mínimo. O responsável informou não ter conhecimento, protocolo ou referência para interpretar emojis, códigos visuais, reações afetivas, ironia ou outros sinais não textuais. A decisão é operacionalmente clara e foi registrada, mas pode ter removido manifestações de afeto, pertencimento, reprovação, humor ou contexto cultural. Não houve medição dessa perda nem reintegração ou reclassificação posterior.

### 6.3 Classificação inicial por regras

Os arquivos demonstram que a classificação inicial usou dois arquivos YAML: um com 17 categorias operacionais e outro com 13 categorias experienciais. Em conjunto, eles contêm 30 categorias, 279 palavras-chave e 120 expressões equivalentes.

O script normaliza caixa e acentuação e procura correspondência literal de palavras ou expressões. Ele não executa compreensão contextual ampla. As regras determinam eixo, justificativa, relevância e confiança a partir do número e do tipo de correspondências. Mais de quatro categorias encontradas produzem marcação de ambiguidade e baixa confiança; uma expressão equivalente ou categoria de peso elevado pode produzir confiança alta.

O arquivo previsto para entidades monitoradas não existe no repositório. Por isso, as 3.325 linhas receberam marcação de entidade não identificada nessa etapa.

| Resultado da classificação por regras | Quantidade |
|---|---:|
| Relevante | 977 |
| Ambígua | 62 |
| Baixa relevância | 2.286 |
| **Total** | **3.325** |

| Grau de confiança atribuído pelo script | Quantidade |
|---|---:|
| Alto | 891 |
| Médio | 86 |
| Baixo | 2.348 |
| **Total** | **3.325** |

Esses graus são indicadores internos produzidos por regras; não são probabilidades calibradas nem medidas de acurácia. A elevada quantidade de linhas não classificadas ou de baixa confiança mostra que o vocabulário inicial cobriu apenas parte do corpus.

### 6.4 Camada lexical e polaridade textual

Os arquivos demonstram que a etapa seguinte reutiliza as categorias anteriores, tokeniza o texto, organiza frequências e aplica pequenos léxicos positivos e negativos definidos no próprio script.

| Natureza atribuída | Quantidade |
|---|---:|
| Operação tangível | 326 |
| Experiência intangível | 518 |
| Mista | 195 |
| Indefinida | 2.286 |
| **Total** | **3.325** |

| Polaridade textual | Quantidade |
|---|---:|
| Positiva | 201 |
| Negativa | 257 |
| Ambivalente | 24 |
| Neutra | 2.843 |
| **Total** | **3.325** |

“Neutra” significa, no código, que nenhum termo dos léxicos positivo ou negativo foi encontrado em um texto não vazio. Não equivale a uma avaliação sem sentimento nem a uma interpretação semântica contextual. Ironia, gíria, ambivalência cultural e sinais não textuais não são resolvidos por esse procedimento.

Os scripts preservados não fazem chamadas documentadas a modelos de linguagem, serviços externos ou classificadores estatísticos. Nessa parte do pipeline, trata-se de automação determinística baseada em regras, listas e limiares.

### 6.5 Matrizes por lote

Os arquivos demonstram que o script de matriz agrupa linhas por natureza, categoria principal, polaridade e eixo, desde que exista evidência textual recuperável. Ele preserva até cinco trechos representativos, relaciona identificadores de origem e gera, por fórmulas fixas, descrição do problema, impactos, prioridade, área sugerida, indicador e recomendação.

| Lote | Grupos gerados | Soma das ocorrências |
|---|---:|---:|
| 01 | 396 | 743 |
| 02 | 739 | 1.938 |
| 03 | 398 | 644 |
| **Total** | **1.533** | **3.325** |

As recomendações são formulações padronizadas condicionadas à presença de evidência e identificadores. Elas não registram verificação de causa, viabilidade, custo, responsabilidade real ou implementação. Por isso, devem ser lidas como encaminhamentos analíticos preliminares, não como soluções comprovadas.

### 6.6 Consolidação e agrupamento executivo

Os arquivos demonstram a redução de 1.533 grupos por lote para 1.000 registros consolidados e, depois, para 39 macroagrupamentos executivos. A soma de ocorrências permanece 3.325 nas duas camadas.

Na matriz por lote não há prioridade alta: aparecem 38 grupos de prioridade baixa, 13 média e 1.482 em monitoramento. Na matriz consolidada aparecem 22 registros de prioridade alta, 249 média e 729 em monitoramento. No agrupamento executivo aparecem 18 macroagrupamentos de prioridade alta, 18 média e 3 baixa.

Não foi possível determinar computacionalmente como foram produzidas essas mudanças, porque os scripts de consolidação e agrupamento executivo não estão no repositório. Os relatórios descrevem os resultados, mas não substituem o código, os parâmetros e os testes necessários à reprodução.

## 7. Maturação taxonômica posterior

Os arquivos demonstram que a Taxonomia Mestre foi criada depois da rodada inicial e organiza dez frentes: sociocultural e linguística; saúde, segurança e redução de danos; histórico-musical e curatorial; operação e infraestrutura; experiência e percepção; reputação e decisão; governança, ética e proteção de dados; território e dinâmica urbana; economia da experiência e valor percebido; trabalho, bastidores e cadeia produtiva.

Segundo declaração retrospectiva do responsável, essa taxonomia surgiu quando a estrutura inicial foi percebida como insuficiente. Seu desenvolvimento foi progressivo e pretende servir como referência para trabalhos futuros.

Os próprios registros da taxonomia determinam que ela oriente novas etapas, mas também afirmam que a rodada inicial não foi reprocessada automaticamente. Assim, devem ser mantidas duas camadas distintas:

- **camada efetivamente usada na rodada inicial**: categorias e critérios dos dois arquivos YAML, léxicos e funções dos scripts preservados;
- **camada metodológica posterior**: Taxonomia Mestre, criada como ampliação conceitual e referência prospectiva.

Não é correto apresentar a Taxonomia Mestre como fundamento prévio da seleção, coleta, limpeza ou classificação já executadas.

## 8. Papel do Codex e divisão de responsabilidades

Segundo declaração retrospectiva do responsável e conforme os artefatos preservados, o Codex funcionou como ambiente de apoio para organização, execução de regras, produção de scripts, rastreabilidade documental, análise e geração de artefatos.

Esse papel deve ser decomposto em quatro níveis:

| Nível | Função observada | Limite |
|---|---|---|
| Automação determinística | Leitura, padronização, limpeza, correspondência de termos, contagens e agrupamentos programados | Executa regras codificadas; não compreende por si só o contexto social |
| Apoio computacional | Geração de CSV, XLSX, logs, relatórios, matrizes e estruturas para painéis | Depende da qualidade dos dados, regras e comandos fornecidos |
| Apoio analítico | Organização de impactos, prioridades, recomendações, testes e linguagem de apresentação | Pode introduzir simplificações, inconsistências ou extrapolações e requer validação humana |
| Decisão humana | Definição de escopo, aceitação ou rejeição de alterações, interpretação contextual e autorização de uso | Permanece com o responsável; não é delegada ao sistema |

O uso do Codex não constitui validação científica, autonomia metodológica ou decisão final. Para testes posteriores com agentes de apoio, o repositório não preserva de forma suficiente modelo, configuração, instruções completas, parâmetros ou ambiente de execução. Esses testes podem ser auditados pelos resultados gerados, mas não integralmente repetidos.

## 9. Validação humana e testes controlados

Os arquivos demonstram que listas de entrega afirmam validação manual das matrizes, da consolidação, do painel e da leitura executiva. Contudo, não foi localizado protocolo completo com identidade e função dos avaliadores, critérios prévios, amostragem de controle, registro de discordâncias, métricas entre avaliadores ou termo de aprovação detalhado.

Há evidência mais concreta em dois testes derivados, ambos com 30 registros, dez por lote. O primeiro testou um agente de qualidade e deixou campos de decisão humana em branco. O segundo comparou dois agentes de apoio nos mesmos 30 registros: foram registradas diferenças sobretudo em impacto, em 27 casos, e polaridade, em 5.

Os cinco casos de mudança de polaridade receberam decisão humana registrada: três foram aceitos total ou parcialmente e dois rejeitados. Nenhuma dessas decisões alterou as matrizes ou os painéis oficiais. Esse exercício demonstra controle humano pontual, mas sua escala não sustenta uma afirmação de validação geral do pipeline.

## 10. Rastreabilidade: ponto forte inicial e degradação posterior

Até as matrizes por lote, os arquivos demonstram 3.325 identificadores completos e únicos, cada um combinando lote, arquivo e linha de origem. Essa estrutura permite reconectar cada ocorrência à base limpa correspondente.

Na matriz consolidada e no agrupamento executivo, o campo que deveria preservar esses identificadores foi reserializado como listas de componentes separados: nomes de lote, nomes de arquivo e números de linha aparecem sem manter, de modo inequívoco, todas as associações originais. O volume continua disponível, mas a chave composta deixa de ser confiável para reconexão automática em agrupamentos com múltiplas origens.

Um artefato posterior de exemplos recorrentes confirma o efeito: para um tema, o volume consolidado era 62, mas apenas 53 registros puderam ser reconectados pelos identificadores preservados. Outro tema, com estrutura de origem mais simples, teve reconexão integral. Portanto, a rastreabilidade não deve ser descrita como uniforme em todas as camadas.

Para uso futuro, o campo de origem deve permanecer estruturado em uma tabela relacional ou lista de objetos, com uma chave completa por ocorrência, sem decomposição destrutiva.

## 11. Painel interno e camada pública

### 11.1 Painel interno

Os arquivos demonstram que o painel interno foi construído a partir de 1.000 registros consolidados e 39 macroagrupamentos. Ele declara 13 recortes por proxy técnico, 3.032 linhas de evidência rastreadas e 18 recomendações executivas com evidência associada.

A validação do painel interno foi estática, pois a abertura direta em navegador não foi usada no ambiente registrado. A inspeção inicial identificou 8 problemas críticos, 7 médios e 2 leves. As correções críticas alteraram somente a interface e mantiveram os dados. Os registros posteriores marcaram a estrutura interna como validada, embora problemas médios e leves tenham permanecido documentados.

“Proxy técnico” é essencial: os dados não possuem campo literal de festa ou evento. O nome derivado do arquivo foi usado como aproximação de recorte. Esse recurso não autoriza atribuir resultados a uma organização ou experiência específica.

### 11.2 Divergências quantitativas

Três universos distintos aparecem nos artefatos:

- 14 rótulos distintos derivados como perfil-alvo na base padronizada;
- 13 recortes por proxy no painel;
- 3.032 linhas apresentadas como evidência rastreada, diante de 3.325 linhas preservadas após limpeza.

Não foi possível determinar a regra completa que transforma 14 rótulos em 13 proxies nem quais 293 linhas separam a base limpa do total apresentado pelo painel. O arquivo público denomina 3.032 como comentários considerados, mas o repositório não preserva uma tabela de correspondência que justifique essa equivalência. Os números devem permanecer separados.

### 11.3 Camada pública e governança

Os artefatos públicos apresentam 39 temas, 1.000 pontos de atenção, 18 recomendações, 13 recortes e 3.032 comentários considerados. Uma expansão de consulta criou 221 itens, entre eles 40 entidades, 33 evidências e agrupamentos de ranking.

Os arquivos demonstram uma ruptura de governança: documentos anteriores registram impedimento de codificação, pendências humanas e ausência de autorização explícita; documentos posteriores registram o painel como implementado. Não foi localizado um registro intermediário que mostre a autorização, a aprovação das pendências e a mudança formal de estado. A existência técnica do painel não resolve essa lacuna.

Além disso, a inclusão posterior de rankings e entidades nomeadas entra em tensão com registros anteriores que recomendavam evitar rankings sensíveis, individualização e atribuição pública. Essa tensão exige avaliação humana antes de qualquer exposição.

## 12. Proteção de dados, ética e risco de reidentificação

O fato de comentários terem sido acessíveis publicamente não equivale a autorização irrestrita para reorganizá-los, relacioná-los, ranqueá-los ou republicá-los. O repositório contém identificadores, nomes de usuário, endereços de perfil e avatar, datas, textos literais, nomes de arquivos associados a recortes e evidências que podem ser pesquisáveis.

As camadas derivadas propagam parte desses elementos. Logs de exclusão preservam usuário e comentário; classificações e matrizes preservam textos e origem; o JSON interno mantém evidências literais e numerosas menções com sintaxe de perfil. A base pública remove identificadores diretos detectáveis por padrões simples, mas ainda contém entidades nomeadas, rankings, temas associados e células de baixa frequência. A combinação desses elementos pode permitir reidentificação por contexto.

As medidas apropriadas para uma saída externa incluem:

- minimização de campos;
- generalização de categorias e contagens;
- supressão ou agrupamento de células pequenas;
- remoção de comentários literais e fragmentos pesquisáveis;
- retirada de nomes, perfis, endereços e identificadores;
- eliminação de rankings individualizantes;
- análise de combinações raras;
- separação entre ambiente auditável interno e material de circulação;
- validação humana especializada antes da publicação.

Essas medidas reduzem risco, mas não permitem afirmar conformidade definitiva com a legislação de proteção de dados. Uma conclusão jurídica ou ética depende de avaliação especializada, finalidade, base legal, governança, retenção, segurança, direitos dos titulares e contexto de uso.

## 13. O que é e o que não é reproduzível

### Reproduzível com os arquivos atuais

- conferência dos 15 XLSX preservados e sua organização em três lotes;
- ingestão e padronização, desde que se mantenha ambiente compatível;
- limpeza e reprodução dos 395 logs de exclusão;
- classificação inicial pelos dois arquivos YAML;
- camada lexical e polaridade por léxicos;
- matrizes resolutivas por lote;
- conferência das contagens e resultados tabulares preservados.

### Parcialmente reproduzível ou não reproduzível

- seleção inicial das 19 publicações, por ausência de protocolo contemporâneo;
- coleta pela extensão, por ausência de ferramenta, configuração e logs;
- relação individual entre 19 endereços e 15 exportações;
- consolidação de 1.533 para 1.000 grupos;
- agrupamento de 1.000 registros em 39 macroagrupamentos;
- geração dos dados dos painéis interno e público;
- transformação de 3.325 linhas em 3.032 linhas apresentadas pelo painel;
- configuração dos testes com agentes de apoio;
- processo geral de validação humana;
- transição do impedimento documental para a implementação pública.

## 14. Limites de inferência

Este corpus permite descrever padrões encontrados no conjunto coletado e processado. Ele não permite, sem evidência adicional:

- estimar prevalência na população;
- comparar validamente organizações, eventos ou públicos;
- inferir causas operacionais;
- atribuir responsabilidade;
- medir satisfação geral;
- afirmar tendência temporal;
- avaliar o que não foi capturado pela extensão;
- tratar ausência de correspondência lexical como ausência de tema;
- transformar recomendações automáticas em decisões implementadas;
- considerar neutralidade lexical como neutralidade emocional;
- interpretar emojis ou sinais culturais excluídos.

## 15. Agenda única para avaliação externa

A avaliação por laboratórios ou especialistas deve partir de uma decisão clara: **preservar o núcleo auditável e reconstruir os trechos que hoje impedem validade e circulação segura**.

Devem ser preservados:

- imutabilidade das fontes brutas;
- separação por lotes;
- geração de derivados sem sobrescrita;
- logs integrais de exclusão;
- regras computacionais legíveis;
- distinção entre automação, apoio analítico e decisão humana;
- linguagem prudente contra causalidade e responsabilização indevidas.

Devem ser reconstruídos ou formalizados antes de nova rodada:

- protocolo de seleção com objetivos, unidade de análise e critérios explícitos;
- ficha de coleta por endereço, com ferramenta, configuração, tentativa, resultado e limitação;
- política para comentários não textuais;
- conjunto de validação humana com amostragem, critérios, discordâncias e métricas;
- dicionário de dados e linhagem entre todas as etapas;
- scripts das consolidações, agrupamentos e painéis;
- identificadores compostos preservados sem perda;
- regra documentada para cada mudança de universo quantitativo;
- protocolo de autorização e mudança de estado para produtos públicos;
- avaliação de privacidade e reidentificação antes de qualquer divulgação.

Devem permanecer suspensos para circulação externa até decisão humana:

- comentários ou fragmentos literais;
- nomes, perfis, entidades raras e endereços;
- datas e combinações de origem precisas;
- rankings individualizantes;
- células pequenas ou combinações facilmente pesquisáveis;
- afirmações de representatividade, causalidade, desempenho, culpa ou validação científica.

## 16. Síntese metodológica

O Mapa da Noite produziu uma cadeia documental extensa e um núcleo computacional legível para ingestão, limpeza, classificação lexical e matrizes por lote. A preservação dos brutos, os logs de exclusão e a separação das etapas são qualidades concretas.

Ao mesmo tempo, a seleção foi intencional e não probabilística; a coleta não tem metadados suficientes; a interpretação inicial depende de vocabulário restrito; a Taxonomia Mestre é posterior; a validação humana é apenas parcialmente documentada; a rastreabilidade degrada após as matrizes por lote; scripts decisivos não foram preservados; universos quantitativos divergem; e a governança do painel público apresenta uma transição não registrada.

O estatuto mais preciso é o de uma aplicação autoral exploratória, apoiada por automação e sistematização documental, que pode servir como objeto de avaliação e aprendizagem metodológica. Seu valor externo depende de explicitar esses limites, restaurar a reprodutibilidade das etapas ausentes e aplicar proteção de dados proporcional ao risco.

## 17. Fontes internas consultadas

Foram consultados, sem alteração:

- regras operacionais do projeto e instruções de preservação;
- contexto mestre e documentação da Taxonomia Mestre;
- diagnósticos técnicos dos três lotes;
- 15 XLSX brutos e suas cópias organizadas por lote;
- bases tratadas, base parcial, bases limpas e logs;
- classificações, amostras e relatórios das camadas textuais;
- matrizes por lote, matriz consolidada e agrupamento executivo;
- entregas metodológicas e executivas;
- painel interno, dados, código e registros de validação;
- painel público, dados, código e registros de governança;
- testes controlados de agentes de apoio e decisões humanas pontuais;
- exemplos derivados e filtro documental nominal;
- cinco scripts Python e dois arquivos YAML.

As referências são mantidas em nível de pasta ou classe documental para evitar a reprodução de caminhos locais, nomes de perfis, nomes de arquivos identificáveis e outros elementos que ampliariam o risco de reidentificação.
