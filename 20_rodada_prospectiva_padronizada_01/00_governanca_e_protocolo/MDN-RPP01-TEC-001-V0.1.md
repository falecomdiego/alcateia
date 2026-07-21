# MDN-RPP01-TEC-001-V0.1 — Consolidação técnica corrigida do Mapa da Noite

## Controle

- Projeto: `Mapa da Noite`
- Data: 16/07/2026
- Versão: `0.1`
- Status: documento técnico interno controlado
- Circulação externa: não autorizada
- Fonte textual recebida: `Documento_Tecnico_Interacoes_Mapa_da_Noite.md`
- Hash da fonte textual: `dc86cba3f5983c3b0bf238365aaea13ead6d2de62ef27ca4b0ae2bfee968cf5c`
- Fonte diagramada recebida: `Documento_Tecnico_Interacoes_Mapa_da_Noite.docx`
- Hash da fonte diagramada: `8515e55fa491561cf3f428adeb4009e699bec1b16927e37477d40820385a5a66`

## 1. Finalidade

Este documento consolida o estado tecnicamente recuperável do Mapa da Noite, separando:

1. a rodada inicial, executada antes do protocolo prospectivo;
2. a infraestrutura MDN-RPP01 atualmente implantada;
3. metas e aplicações futuras ainda não executadas.

Interações de conversa são usadas apenas como contexto quando possuem correspondência nos documentos vigentes. Declarações sem registro em inventário, decisão, log ou artefato verificável não são apresentadas como fato operacional.

## 2. Definição de fase

O Mapa da Noite é uma infraestrutura metodológica de inteligência coletiva em validação. Seu objetivo é organizar um corpus definido de manifestações públicas em sinais descritivos, rastreáveis e sujeitos a validação humana, para apoiar avaliação e tomada de decisão no ecossistema da música eletrônica.

Nesta fase, o projeto deve ser apresentado como **serviço assistido, controlado e auditável em validação**, e não como pesquisa representativa, método cientificamente validado, sistema autônomo de inteligência artificial ou solução de política pública comprovada.

## 3. Problema e proposta de valor

Comentários públicos sobre a vida noturna permanecem dispersos e são difíceis de examinar de forma organizada. O projeto propõe delimitar previamente um corpus, preservar sua origem, registrar tratamentos, permitir abstenção analítica e produzir sinais agregados com limitações explícitas.

O termo “inteligência coletiva” descreve a organização de manifestações produzidas por diferentes participantes. Ele não significa que o corpus represente automaticamente toda a comunidade, que cada comentário corresponda a uma pessoa única ou que recorrência demonstre prevalência populacional.

## 4. Camada histórica — rodada inicial

### 4.1 Estatuto

A primeira aplicação é uma experiência autoral exploratória posteriormente sistematizada de forma retrospectiva. Ela não nasceu com protocolo contemporâneo suficiente para demonstrar seleção, completude da coleta, validação humana, rastreabilidade integral e governança de publicação.

### 4.2 Balanço documental recuperável

| Etapa | Unidade | Quantidade | Leitura permitida |
|---|---|---:|---|
| Lista de entrada | endereços | 19 | universo de entrada declarado; relação com exportações não reconciliada |
| Coleta preservada | arquivos XLSX | 15 | cinco arquivos em cada um dos três lotes |
| Entrada | linhas exportadas | 3.720 | registros; não pessoas |
| Limpeza | registros preservados | 3.325 | 395 exclusões técnicas com log |
| Matrizes por lote | grupos | 1.533 | volumes somam 3.325 ocorrências |
| Consolidação | registros agrupados | 1.000 | mudança de unidade |
| Síntese executiva | macroagrupamentos | 39 | camada derivada histórica |
| Painel | recomendações | 18 | recomendações organizadas; não ações implementadas |

O painel histórico também declara 3.032 linhas de evidência e 13 recortes por proxy, enquanto a base limpa possui 3.325 registros e a padronização contém 14 rótulos. Essas divergências permanecem não reconciliadas.

### 4.3 Limites da coleta histórica

Não foram preservados de modo suficiente:

- protocolo anterior de seleção;
- correspondência integral entre 19 endereços e 15 exportações;
- nome, versão e configuração da extensão de coleta;
- paginação, respostas, limites, falhas e completude;
- datas necessárias para distinguir publicação, comentário, coleta e evento.

Por isso, não se afirma captura completa nem recorte temporal plenamente reproduzível.

### 4.4 Limpeza e perda conhecida

As 395 exclusões históricas possuem log: 366 registros apenas com emoji, 19 vazios, sete duplicidades conforme a chave aplicada e três com sinal textual mínimo insuficiente.

A exclusão de emojis é uma decisão histórica documentada, mas pode ter removido sinais de afeto, ironia, pertencimento ou contexto cultural. Na MDN-RPP01, comentários apenas com emoji devem permanecer contabilizados como `fora_classificacao_textual`.

### 4.5 Classificação histórica

A classificação inicial foi determinística e baseada em regras e léxicos. Ela não utilizou treinamento de modelo estatístico nem chamada documentada a modelo de linguagem nos cinco scripts preservados.

Entre os 3.325 registros preservados, 2.286 ficaram em baixa relevância ou categoria indefinida e 2.348 receberam confiança baixa. Polaridade lexical não equivale a sentimento confirmado; ausência de termo não equivale a ausência de tema.

### 4.6 Rastreabilidade histórica

A rastreabilidade é relevante até as matrizes por lote. Depois dessa etapa, a linhagem se degrada e faltam scripts suficientes para reproduzir integralmente:

- a passagem de 1.533 grupos para 1.000 registros;
- a formação dos 39 macroagrupamentos;
- a geração dos JSONs e painéis;
- a transformação de 3.325 registros em 3.032 linhas declaradas no painel.

Portanto, a rodada inicial produziu artefatos organizados, mas não possui auditabilidade integral de ponta a ponta segundo o padrão atual.

## 5. Taxonomia Mestre V1.1

A Taxonomia Mestre V1.1 foi criada depois da classificação inicial e representa evolução metodológica. Ela não foi aplicada retroativamente à rodada inicial e permanece congelada para orientar a MDN-RPP01.

Lacunas encontradas durante a nova rodada deverão ser registradas sem alterar a versão 1.1 durante o processamento.

## 6. Camada prospectiva — MDN-RPP01

### 6.1 Finalidade

A MDN-RPP01 foi criada separadamente para validar rastreabilidade, governança mínima, validação humana, sanitização e reaplicação antes da comercialização.

A rodada inicial permanece preservada e não será apresentada como se tivesse seguido o novo protocolo.

### 6.2 Estrutura implantada

A infraestrutura atual contém:

- manifesto anterior à coleta;
- governança por gates;
- inventários de fontes, lotes, coleta, autoria, acessos, riscos, custos e interlocuções;
- dicionário de dados;
- controle de versões e hashes;
- pipeline V2 configurável;
- ingestão separada por lote;
- pseudonimização interna por HMAC;
- tratamento sem perda invisível;
- triagem lexical com `nao_determinado`;
- amostra de validação humana e dupla revisão;
- consolidação relacional por `registros`, `grupos` e `grupo_registro`;
- sanitização pública condicionada a métricas, autorizações e gate;
- fixture sintética e guia de reaplicação.

### 6.3 Estado técnico verificado

- seis testes automatizados estão aprovados;
- os gates `G0` a `G5` permanecem bloqueados;
- nenhum arquivo real foi colocado na camada protegida da nova rodada;
- nenhum comentário foi coletado ou processado na MDN-RPP01;
- nenhum produto público foi gerado;
- o período e as fontes da nova rodada ainda não foram aprovados.

A existência do pipeline demonstra disponibilidade de controles e operações programadas. Ela não demonstra desempenho, precisão ou reaplicabilidade em corpus real.

## 7. Fluxo prospectivo autorizado

O fluxo metodológico previsto é:

1. aprovação de manifesto, período, fontes, papéis e riscos;
2. inventário e registro de cada tentativa de coleta;
3. preservação do bruto e cálculo de hash;
4. diagnóstico e processamento de um lote por vez;
5. criação de base interna pseudonimizada;
6. limpeza com balanço reconciliado e sem exclusão invisível;
7. triagem taxonômica com abstenção explícita;
8. validação humana dos casos amostrados, ambíguos e sensíveis;
9. consolidação relacional e matriz de evidências;
10. produto interno com limitações e denominadores;
11. sanitização e revisão independente;
12. liberação pública somente após G4;
13. teste de reaplicação por pessoa externa à construção.

## 8. Proteção de dados e circulação

As camadas devem permanecer distintas:

- **bruto protegido:** identificável e imutável;
- **tratado protegido:** preserva origem e controles técnicos;
- **trabalho interno:** pseudonimizado e sujeito a acesso controlado;
- **produto interno:** contém agregados e mecanismos de auditoria;
- **pacote público:** sanitizado e condicionado ao gate.

O produto público não poderá conter identificadores, URLs, comentários pesquisáveis, rankings individualizantes, acusações atribuíveis, combinações raras ou células abaixo do limiar definido.

Não se declara conformidade jurídica definitiva. O dossiê `MDN-RPP01-JUR-001-V0.1` registra os limites e a necessidade de avaliação especializada.

## 9. Posicionamento e públicos

A comunicação controlada organiza quatro relações:

- frequentadores: sinais de experiência, pertencimento, cuidado e participação dentro do corpus;
- produtores, artistas e selos: apoio à avaliação de experiência, operação, segurança, comunicação e curadoria;
- marcas, patrocinadores e fornecedores: leitura contextual de pertencimento e experiência, sem auditoria de consumo;
- órgãos públicos e território: subsídios exploratórios para formular perguntas, sem substituir dados oficiais, consulta pública ou competência institucional.

## 10. Metas futuras corretamente qualificadas

A observação de até 50 perfis e a meta de até 10.000 comentários são referências de expansão futura. Elas não correspondem à rodada inicial auditada e ainda não constituem base da MDN-RPP01.

O recorte prospectivo assumido permanece São Paulo e música eletrônica Tribal House, com período e fontes a definir antes da coleta.

Não existe, nos controles vigentes, autorização para afirmar como próxima rodada uma cidade, evento ou parceiro específico diferente desse recorte.

## 11. Afirmações permitidas nesta fase

Pode-se afirmar que:

- existe uma primeira aplicação exploratória documentada com limitações explícitas;
- existe uma infraestrutura prospectiva separada e bloqueada por gates;
- a Taxonomia Mestre V1.1 está congelada para a nova rodada;
- o pipeline V2 passou em testes sintéticos;
- o modelo comercial pretendido é um serviço assistido e auditável em validação;
- a publicação depende de sanitização, validação humana e aprovação formal.

## 12. Afirmações bloqueadas nesta fase

Não se pode afirmar que:

- 50 perfis ou 10.000 comentários já compõem base auditada;
- a MDN-RPP01 já realizou coleta;
- o corpus representa a comunidade ou a cena eletrônica;
- existe precisão estatística ou validação científica;
- há monitoramento contínuo ou coleta completa;
- o projeto utiliza PLN avançado ou modelo autônomo na classificação;
- recorrência comprova causa, responsabilidade ou eficácia;
- existe política pública implementada ou resultado público comprovado;
- interlocução externa equivale a parceria, validação ou certificação;
- G0, G4 ou qualquer outro gate está aprovado.

## 13. Pendências prioritárias

Antes de qualquer coleta, precisam ser definidos:

- período prospectivo;
- perguntas finais;
- fontes previstas e critérios de seleção;
- ferramenta, versão, configuração e procedimento de coleta;
- responsáveis operacionais e de proteção de dados;
- retenção, cópia protegida e resposta a incidentes;
- segundo revisor;
- critérios de encerramento e suspensão.

## 14. Conclusão

O Mapa da Noite possui patrimônio documental e técnico real, mas sua força comercial depende da precisão com que separa experiência histórica, infraestrutura disponível e resultado ainda não produzido.

A primeira aplicação demonstra capacidade de organização e aprendizado, não validação integral. A MDN-RPP01 transforma as lacunas identificadas em controles prospectivos, mas permanece pré-coleta. O próximo avanço legítimo é concluir G0 e executar uma nova rodada sem reescrever o histórico.

