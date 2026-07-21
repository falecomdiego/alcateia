# MDN-RPP01-MAN-001-V0.3 — Manifesto anterior à coleta

## Controle

- Rodada: `MDN-RPP01`
- Versão: `0.3`
- Data de atualização: 16/07/2026
- Substitui: `MDN-RPP01-MAN-001-V0.2`
- Status: preenchido parcialmente; pendências bloqueantes registradas
- Gate G0: **não aprovado**
- Natureza prospectiva: anterior à extração e à análise, embora o período de referência já tenha encerrado

## Problema observado

Há manifestações públicas dispersas sobre a vida noturna, mas a primeira aplicação não nasceu com registros contemporâneos suficientes para demonstrar seleção, completude da coleta, validação humana, rastreabilidade integral e governança de publicação.

## Objetivo principal

Executar uma nova observação exploratória com protocolo anterior à extração, dados protegidos, processamento reproduzível por lote, validação humana documentada e pacote de reaplicação.

## Pergunta central operacional

Como comentários públicos relacionados ao Tribal House em São Paulo, datados de 1 a 30 de junho de 2026, articulam percepções e tensões entre comercialização da experiência e ética do cuidado, considerando governança das pistas, códigos culturais, precificação, operação, tipos de ambiente, infraestrutura, segurança, redução de danos e relações mencionadas com políticas públicas e equipamentos urbanos?

## Subperguntas orientadoras

1. Quais manifestações fazem referência à governança das pistas, aos códigos culturais, às gírias e aos rituais, e em quais contextos?
2. Quais sinais descritivos aparecem sobre preço, valor percebido, infraestrutura e operação, sem converter recorrência em diagnóstico de eficácia?
3. Como diferem os sinais observados em contextos identificados previamente como clube fechado ou `open air`, quando essa informação estiver documentada na fonte?
4. Quais referências aparecem sobre segurança, redução de danos e ética do cuidado, e quais casos exigem revisão humana obrigatória?
5. Quais menções relacionam a experiência noturna a políticas públicas, mobilidade ou equipamentos urbanos?
6. Quais resultados podem ser tratados como evidência observada, inferência, recomendação ou decisão humana?

## Ampliação temporal registrada

- Janela inicial: 01/06/2026 a 15/06/2026.
- Janela confirmada: 01/06/2026 a 30/06/2026.
- Motivo: incorporar comentários e repercussões posteriores ao dia 15 relacionados às festas do período de Corpus Christi.
- Regra preventiva: a janela ampliada será aplicada integralmente a todas as fontes aprovadas.
- Proibição: não selecionar somente comentários posteriores já conhecidos como relevantes.
- Consequência: toda comparação temporal deverá declarar a janela completa e, se houver divisão por fase, usar cortes definidos antes da análise.

## Blindagem interpretativa da pergunta

- Ausência de menção não prova ausência de política, serviço, equipamento, cuidado ou problema.
- Comentário não equivale a pessoa única, experiência independente ou posição representativa da comunidade.
- Recorrência não prova causalidade, eficácia, intenção, culpa ou negociação comunitária consolidada.
- Comparação entre clube fechado e `open air` somente será realizada quando o contexto da publicação estiver classificado antes da análise dos comentários.
- Precificação e operação serão tratadas como percepções observadas, não como auditoria financeira ou operacional.
- A inclusão do período posterior a 15/06 não poderá ser apresentada como descoberta prospectivamente prevista.

## Campo e público relacionados

- Campo: cena Tribal House de São Paulo.
- Contextos comparáveis previstos: clubes fechados e eventos `open air`.
- Público relacionado: pessoas que publicaram comentários nas fontes escolhidas.
- Plataforma: Instagram.
- Período de referência dos comentários: 01/06/2026 a 30/06/2026.
- Fuso de referência: `America/Sao_Paulo`.
- Data de execução da coleta: posterior à aprovação de G0, a registrar em cada tentativa.
- Fontes previstas: **pendentes; a planilha recebida contém perfis de comentaristas e não as publicações ou contas-fonte exigidas**.

## Unidade observada

Uma linha exportada como comentário, com `Comment Date` dentro do período de referência. Ela não equivale automaticamente a pessoa, evento, organização, experiência independente ou opinião representativa.

## Unidade de fonte

Uma publicação pública do Instagram, vinculada a uma conta pertinente ao recorte e identificada antes da extração. Cada publicação receberá um `fonte_id`; perfis de comentaristas não podem ser usados como fonte de coleta.

## Critérios prévios de inclusão da fonte

- pertinência demonstrável ao Tribal House em São Paulo;
- publicação pública e acessível no momento da tentativa;
- contexto previamente classificado como clube fechado, `open air` ou não determinado;
- publicação relacionada a atividade ocorrida, anunciada ou discutida no recorte de interesse;
- justificativa registrada no inventário antes da extração;
- possibilidade técnica de coleta com ferramenta e configuração documentadas;
- ausência de bloqueio de risco identificado no momento da seleção.

## Critérios prévios de inclusão do registro

- linha exportada pela tentativa vinculada à fonte aprovada;
- `Comment Date` interpretável e entre 01/06/2026 e 30/06/2026, inclusive;
- preservação integral das oito colunas originais esperadas;
- vínculo recuperável com arquivo, aba e linha de origem.

## Critérios prévios de exclusão

- publicação fora do campo definido;
- ausência de justificativa de inclusão;
- duplicação da mesma publicação no inventário;
- perfil de comentarista apresentado como se fosse conta ou publicação-fonte;
- comentário fora do período de referência;
- coleta incompatível com os controles técnicos e de proteção definidos;
- determinação de suspensão pelo responsável de risco ou publicação.

Toda exclusão posterior à exportação deverá permanecer no balanço e possuir log específico.

## Ferramenta registrada

- Nome: `Exportar Comentários - Extrator de Comentários Instagram`.
- Versão observada: `1.10.3`.
- Identificador observado: `nilbploiciiajeklaogbonjaejdjhfao`.
- Evidência: registro protegido com hash SHA-256.
- Situação: ferramenta identificada; configuração operacional ainda não documentada.

### Minimização obrigatória

A descrição da extensão indica capacidade de extrair e-mail e telefone. A MDN-RPP01 não possui finalidade para esses campos. Portanto:

- coleta de e-mail e telefone fica proibida;
- campos adicionais fora das oito colunas originais não devem ser selecionados ou incorporados;
- uma exportação sintética de configuração deverá comprovar cabeçalho, paginação, respostas, ordenação e formato antes de qualquer fonte real;
- qualquer campo inesperado suspende a tentativa e exige nova decisão.

## Papéis registrados

- Responsável da rodada e operador de coleta: identificado em registro interno protegido.
- Revisora independente para G4: indicada em registro interno; aceite direto ainda pendente.
- Responsável metodológico: pendente de atribuição nominal.
- Responsável por proteção de dados: pendente de atribuição nominal.
- Responsável por publicação: pendente de atribuição nominal.

Uma pessoa pode acumular funções internas, mas a revisão independente de G4 não pode ser substituída.

## Retenção e destinação

- Dados brutos protegidos, mapeamento de pseudônimos e base de trabalho identificável: 12 meses após o encerramento de G1.
- Ao final: exclusão segura com registro ou renovação justificada por nova decisão datada.
- Hashes, manifestos de execução, contagens agregadas e logs sem conteúdo identificável: permanentes para auditoria.
- Lista nominal de acesso, local da cópia protegida e método de exclusão: ainda pendentes.

## Produtos esperados

- base interna rastreável e pseudonimizada;
- logs completos de coleta, tratamento e decisões;
- classificação orientada pela Taxonomia Mestre V1.1, com abstenção explícita;
- consolidação relacional reversível;
- relatório interno de qualidade e limitações;
- pacote público apenas se G4 for aprovado;
- pacote de reaplicação testável por terceiro.

## Perdas aceitáveis

Nenhuma perda invisível. Falhas de coleta, arquivos ausentes, registros inválidos, exclusões técnicas e itens fora da classificação textual devem permanecer contabilizados e justificados.

## Condições de suspensão

- inventário formado por perfis de comentaristas em vez de publicações-fonte;
- fonte selecionada após inspeção de resultados sem justificativa anterior à extração;
- comentário selecionado apenas por ser conhecido como relevante após 15/06;
- divergência de colunas originais;
- presença de e-mail, telefone ou campo não autorizado;
- ferramenta ou configuração de coleta não documentada;
- alteração de bruto ou divergência de hash;
- quebra de unicidade ou linhagem;
- ausência de log de exclusão;
- mudança da taxonomia durante a rodada;
- tentativa de consolidar lotes não aprovados;
- risco de exposição não mitigado;
- ausência de decisão humana em item sensível;
- tentativa de publicação sem gate formal.

## Pendências bloqueantes de G0

1. Receber inventário correto de publicações ou contas-fonte, com justificativa e contexto.
2. Registrar a configuração completa da extensão e aprovar uma exportação sintética de teste.
3. Registrar responsáveis metodológico, proteção de dados e publicação.
4. Registrar aceite direto da revisora independente indicada.
5. Definir lista nominal de acesso, local da cópia protegida e método de exclusão ao fim da retenção.

## Aprovação G0

| Função | Identificação | Decisão | Data | Observação |
|---|---|---|---|---|
| Responsável da rodada | registrada em arquivo protegido | preenchimento parcial | 16/07/2026 | G0 não aprovado |
| Responsável metodológico | pendente | pendente |  |  |
| Responsável por proteção de dados | pendente | pendente |  |  |
| Revisora independente | indicada; aceite pendente | pendente |  | necessária para G4 |

