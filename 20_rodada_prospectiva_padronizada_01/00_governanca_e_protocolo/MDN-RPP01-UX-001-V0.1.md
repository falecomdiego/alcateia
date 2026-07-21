# MDN-RPP01-UX-001-V0.1 — Estratégia controlada de UX/UI do painel público

## Controle do documento

- Rodada: `MDN-RPP01`
- Tipo: especificação de UX/UI
- Data: 16/07/2026
- Status: vigente interno; implementação e circulação bloqueadas
- Gate relacionado: `G4 — Publicação`
- Produto definido: protótipo do painel público, separado do painel interno e do material promocional
- Pré-condição: nenhuma tela com resultado real pode ser publicada antes da aprovação formal de `G4`

## Decisão de produto

O painel público será uma **interface de exploração descritiva de evidências coletivas aprovadas**, construída para explicar contexto, recorrência e limitações sem expor pessoas e sem simular previsão.

Enquanto a nova rodada não for coletada e validada, a interface só poderá existir como protótipo interno com dados sintéticos claramente marcados ou, se autorizado para demonstração controlada, com resultados históricos explicitamente rotulados como exploratórios e não comparáveis à MDN-RPP01.

## Posicionamento na interface

### Definição controlada

`Infraestrutura metodológica em validação para organizar manifestações públicas em sinais descritivos, evidências rastreáveis e perguntas úteis ao ecossistema da música eletrônica.`

### Promessa permitida

O Mapa da Noite organiza registros públicos, preserva contexto e documenta a passagem do dado para a leitura coletiva. Recomendações e decisões continuam humanas.

### Promessas proibidas

- prever comportamento, demanda, permanência, risco ou resultado;
- afirmar representatividade da comunidade ou da cidade;
- tratar comentário como pessoa única;
- apresentar recorrência como causalidade;
- chamar consolidação de conclusão;
- afirmar anonimização ou privacidade garantida;
- divulgar precisão, auditabilidade ou impacto sem evidência aprovada;
- sugerir parceria, certificação ou validação institucional inexistente.

## Princípio visual

### Dark-first, não all-dark

A interface usará grafite e navy como moldura estrutural, com amarelo como assinatura. Blocos analíticos alternarão fundos claros/frios e fundos escuros/quentes para reduzir fadiga, separar funções e respeitar a identidade já consolidada.

### Papéis cromáticos

| Papel | Uso |
|---|---|
| Base estrutural escura | cabeçalho, navegação, rodapé, contexto e blocos de método |
| Base analítica clara | tabelas, definições, limitações e leitura comparativa |
| Amarelo assinatura | foco, ação principal, destaque de número aprovado e estado ativo |
| Verde técnico mínimo | confirmação ou controle concluído; nunca como prova autônoma |
| Tons de alerta | pendência, bloqueio ou risco; sempre acompanhados de texto e ícone |

Os códigos exatos, a paleta funcional de gráficos e os estados de contraste permanecem pendentes de fechamento no Manual de Identidade Visual. A implementação não deve inventar valores cromáticos oficiais.

### Linguagem formal

- Google Sans permanece como escolha tipográfica da identidade; a implementação web deve registrar disponibilidade, licença e fallback.
- Hierarquia editorial, espaço negativo, grid e leitura mobile são obrigatórios.
- Neon excessivo, transparência, glassmorphism, cyberpunk, cartoon, gradientes decorativos e efeitos sem função permanecem proibidos.
- Fotografia, cartografia e microelementos urbanos só entram quando ajudam a explicar contexto.
- Gráficos não podem ser usados como decoração nem para ampliar artificialmente diferenças pequenas.

## Arquitetura de informação

### 1. Cabeçalho de estado

Deve mostrar de forma persistente:

- nome do produto;
- camada: `painel público`;
- estado: `protótipo interno`, `histórico exploratório` ou `publicado`;
- versão;
- período de referência;
- data de atualização;
- aviso quando `G4` não estiver aprovado.

### 2. Abertura e contexto

**Título recomendado:**

> O que começa a aparecer quando comentários públicos são organizados com contexto?

**Subtítulo recomendado enquanto a rodada estiver bloqueada:**

> Protótipo metodológico interno. A nova rodada MDN-RPP01 ainda não possui coleta autorizada nem resultados públicos.

**Definição curta:**

> Não é um guia de festas. É uma infraestrutura metodológica em validação para tornar sinais coletivos legíveis sem individualizar pessoas.

O CTA não será `Ver evidências` enquanto não houver pacote público aprovado. O CTA permitido nesta fase é `Entender o método`.

### 3. Escopo e denominadores

Antes de qualquer gráfico, a interface deve responder:

- qual camada está sendo apresentada;
- qual território e período;
- quais fontes foram incluídas;
- o que conta como registro;
- se autores podem se repetir;
- quais exclusões ocorreram;
- o que a base não permite concluir.

### 4. Fluxo metodológico

O fluxo público será exibido como:

`manifestação pública → coleta registrada → preservação → limpeza com log → classificação com abstenção → validação humana → consolidação relacional → evidência aprovada → publicação sanitizada`

Cada etapa deve abrir uma explicação curta, indicar seu estado e apontar o artefato público correspondente, quando houver.

### 5. Evidências aprovadas

Somente afirmações com `afirmacao_id` aprovado poderão entrar. Cada cartão ou gráfico deve exibir:

- título descritivo e não causal;
- unidade e denominador;
- período e território;
- natureza: evidência observada, inferência analítica, recomendação ou decisão humana;
- método de cálculo;
- limitação principal;
- versão da evidência;
- situação de validação;
- acesso a uma tabela ou descrição textual equivalente.

### 6. Limitações

A seção de limitações é parte do conteúdo principal e não rodapé. Deve informar, conforme aplicável:

- comentários não representam toda a comunidade;
- registros não equivalem a pessoas únicas;
- autores podem aparecer mais de uma vez;
- sinais lexicais não comprovam sentimento ou intenção;
- recorrência não comprova causa;
- ausência de menção não comprova ausência de problema;
- o recorte temporal e as fontes limitam generalização.

### 7. Privacidade e governança

A interface explicará controles concretos:

- camada pública separada da camada protegida;
- pseudonimização interna não tratada como anonimização;
- supressão de identificadores, URLs e comentários literais;
- proibição de rankings individualizantes e acusações atribuíveis;
- supressão de combinações raras e células menores que cinco;
- revisão humana e gate formal antes da liberação.

### 8. Versão e contato

O rodapé deve indicar versão do painel, data da liberação, período dos dados, responsável pela publicação, canal para correção e link para nota metodológica pública. Não deve expor caminhos internos, hashes de material protegido ou dados pessoais.

## Contrato para números e gráficos

Nenhum número será renderizado sem os campos abaixo:

| Campo | Regra |
|---|---|
| `afirmacao_id` | obrigatório e único |
| `camada` | histórico, MDN-RPP01 ou sintético |
| `unidade` | registro, grupo, fonte, arquivo, ocorrência ou outra unidade definida |
| `numerador` | valor exibido |
| `denominador` | base de comparação explícita |
| `periodo` | início e fim ou indicação histórica qualificada |
| `territorio` | recorte efetivamente coberto |
| `fonte_calculo` | artefato e versão que permitem reproduzir o número |
| `limitacao` | principal restrição interpretativa |
| `aprovacao` | estado e responsável |
| `publicavel` | verdadeiro somente após `G4` |

### Regras de apresentação

- Eixos devem começar, sempre que aplicável, em zero e informar escalas truncadas.
- Percentuais devem informar `n` e denominador.
- Comparações exigem bases e períodos compatíveis.
- Cores não podem carregar significado sozinhas.
- Valores suprimidos devem aparecer como `não exibido por proteção`, nunca como zero.
- Células com menos de cinco ocorrências não podem ser apresentadas nem derivadas por combinação de filtros.
- Filtros devem impedir dedução de células raras.
- Rankings de pessoas, perfis, marcas, eventos ou locais ficam proibidos no pacote público enquanto puderem individualizar ou atribuir culpa.

## Tratamento dos números históricos

Caso haja autorização específica para uma demonstração interna do histórico, usar exatamente as seguintes definições:

| Valor | Rótulo controlado | Observação obrigatória |
|---:|---|---|
| 19 | endereços listados para coleta | não chamar de perfis efetivamente observados nem de arquivos |
| 15 | arquivos XLSX exportados e preservados | informar que pertencem à rodada inicial |
| 3.720 | linhas históricas de entrada | denominação técnica, não público ou pessoas |
| 395 | exclusões técnicas registradas | apresentar junto do motivo e da reconciliação |
| 3.325 | registros históricos mantidos após limpeza | não chamar de observações independentes nem vozes únicas |
| 1.000 | registros/grupos consolidados no processo histórico | não chamar de conclusões |

Esses valores não pertencem à nova rodada MDN-RPP01 e não comprovam que o protocolo prospectivo foi aplicado no passado.

## Componentes obrigatórios

### Selo de estado

Rótulos fechados:

- `SINTÉTICO — demonstração`
- `HISTÓRICO — exploratório`
- `MDN-RPP01 — validação interna`
- `PUBLICADO — G4 aprovado`

Nenhuma tela pode omitir o selo.

### Cartão de métrica

Deve conter valor, unidade, denominador, período, estado, limitação e acesso ao método. Um número grande sem esses elementos é proibido.

### Cartão de evidência

Deve separar visualmente:

- `observado`;
- `inferido`;
- `recomendado`;
- `decidido por pessoa`.

Essas categorias não podem compartilhar o mesmo tratamento visual sem rótulo textual.

### Bloco de limitação

Deve permanecer visível perto da evidência e não pode depender exclusivamente de tooltip.

### Gráfico acessível

Todo gráfico terá título, descrição, legenda textual, valores consultáveis por teclado e alternativa tabular ou textual equivalente.

### Estado vazio ou bloqueado

Quando não houver evidência aprovada, mostrar:

> Ainda não há resultado público autorizado para este recorte.

Não preencher o vazio com números históricos, estimativas ou exemplos sem rótulo.

## Interatividade permitida

- filtros descritivos por período, tema e camada, quando a cardinalidade permitir;
- comparação entre categorias compatíveis;
- explicação progressiva do método;
- abertura de definições, limitações e notas de cálculo;
- exportação apenas do pacote público já sanitizado;
- alternância entre gráfico e tabela acessível.

## Interatividade proibida nesta fase

- previsão de fila, permanência, risco, consumo ou comparecimento;
- pontuação de pessoas, perfis, eventos, locais, marcas ou produtores;
- busca por comentário literal, usuário, URL ou fragmento pesquisável;
- filtros que permitam reconstruir células menores que cinco;
- mapa de localização com precisão que individualize ocorrência sensível;
- animações que escondam denominadores, mudem valores ou induzam causalidade;
- recomendação automática apresentada como decisão do sistema.

## Acessibilidade como requisito de aceite

A interface terá como referência a WCAG 2.2 no nível AA. A validação deve incluir avaliação automática e humana.

Requisitos mínimos:

- contraste mínimo de 4,5:1 para texto normal e 3:1 para texto grande;
- contraste não textual adequado para controles e estados;
- navegação integral por teclado, ordem de foco coerente e foco visível não encoberto;
- estrutura semântica com títulos, regiões e rótulos corretos;
- texto redimensionável e reflow sem perda de conteúdo;
- alvos de interação compatíveis com o mínimo da WCAG 2.2;
- alternativa a arrastar, passar o mouse e depender de movimento;
- preferência por movimento reduzido respeitada;
- linguagem da página declarada;
- mensagens de estado anunciadas a tecnologias assistivas;
- gráficos e mapas com equivalência textual;
- teste responsivo a partir de 320 CSS pixels de largura, sem rolagem horizontal de conteúdo textual.

Referência normativa: <https://www.w3.org/TR/WCAG22/>.

## Critérios de aceite antes da implementação

- [ ] Identidade do painel público separada do painel interno e do mockup promocional.
- [ ] Paleta funcional, códigos e contrastes aprovados.
- [ ] Tipografia web, fallback e licenças registrados.
- [ ] Componentes desenhados em estados normal, foco, hover, ativo, desabilitado, erro, vazio e bloqueado.
- [ ] Protótipo responsivo testado em mobile e desktop.
- [ ] Nenhuma linguagem preditiva, causal ou de representatividade.
- [ ] Todos os números de demonstração marcados como sintéticos ou históricos.
- [ ] Nenhum resultado real da MDN-RPP01 enquanto `G0` a `G4` estiverem bloqueados.

## Critérios de aceite para publicação

- [ ] `G4` aprovado e registrado.
- [ ] Matriz de evidências completa para todas as afirmações.
- [ ] Precisão mínima de 85% para classificações que sustentem afirmações externas.
- [ ] Segundo avaliador e adjudicação documentados.
- [ ] Reconciliação dos denominadores sem divergência.
- [ ] Testes de privacidade, células raras e combinações de filtros aprovados.
- [ ] Ausência de identificadores, URLs, comentários literais e rankings individualizantes.
- [ ] Auditoria WCAG 2.2 AA concluída com evidências.
- [ ] Revisão editorial confirma unidade, período, fonte, limitação e estado em cada número.
- [ ] Versão, data, responsável e riscos remanescentes publicados.

## Blindagem de escopo

Esta especificação define somente a camada de UX/UI do painel público do Mapa da Noite. Ela não autoriza coleta, processamento, classificação, consolidação, publicação ou uso comercial de resultados. Não incorpora elementos da ALCATEIA e não altera Taxonomia Mestre, bases, matrizes, scripts ou painéis históricos.

