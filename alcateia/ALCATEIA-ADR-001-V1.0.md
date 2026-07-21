# ALCATEIA — Architecture Decision Records (ADR) v1.0

**Status**: FROZEN (Architecture Freeze v1.0)  
**Objetivo**: Registro das decisões de projeto críticas e suas justificativas técnicas.  
**Data**: 21/07/2026  

Este documento reúne os registros oficiais de decisão técnica (*Architecture Decision Records*) que fundamentam a arquitetura ALCATEIA v1.0, servindo como suporte explicativo para revisões técnicas e bancas examinadoras.

---

## [ADR-0001] Separação Estrita de Raciocínio (Probabilístico) e Execução (Determinístico)

### Contexto e Problema
Sistemas baseados exclusivamente em LLMs enfrentam o problema de "alucinação" e inconsistência de processamento de dados (ex.: cálculo de hashes, remoção de registros, filtros de LGPD, contagem de dados). Por outro lado, sistemas estritamente determinísticos carecem de flexibilidade cognitiva para compreender gírias de nicho, nuances culturais e gerar recomendações contextuais complexas.

### Decisão de Projeto
Dividir rigidamente a inteligência do sistema entre dois agentes com papéis mutuamente exclusivos:
1. **GPT-5.6 (Reasoning Service)**: Exclusivamente probabilístico. Atua apenas sobre textos pré-normalizados, interpretando sentimentos, aplicando eixos taxonômicos cognitivos e sintetizando hipóteses analíticas. É expressamente proibido de realizar operações aritméticas, integrações ou filtros diretos em arquivos.
2. **Codex (Execution Service)**: Exclusivamente determinístico. Planeja e executa tarefas lógicas de baixo nível por meio de código programático fixo em Python/SQL (saneamento, hashing, isolamento de caracteres, remoção física de duplicados e indexação relacional). Não gera juízo de valor ou interpretações subjetivas.

### Consequências e Impacto
- **Positivas**: Eliminação completa de alucinações matemáticas ou estruturais nas bases consolidadas; rastreabilidade de código imutável.
- **Negativas**: Exige interfaces de troca de mensagens claras e estritas entre a camada lógica e cognitiva (Módulo de Domínio de Interfaces).

---

## [ADR-0002] Armazenamento Desacoplado via Evidence Chains Relacionais

### Contexto e Problema
A publicação de resultados analíticos com base em inteligência artificial costuma sofrer com a falta de fundamentação. Se uma recomendação final diz "Aumentar a segurança da pista no espaço X", a banca técnica exige saber: *De qual linha/comentário isso veio? Qual arquivo originou? Qual o hash desse arquivo? Qual o nível de incerteza dessa classificação?*

### Decisão de Projeto
Implementar o **Modelo Único de Evidência** (MUE). Toda recomendação ou classificação analítica final gerada pelo *Reasoning Service* deve ser materializada e persistida como uma linha em uma tabela relacional de Evidências. Essa tabela vincula a conclusão de inteligência diretamente aos metadados estáveis fornecidos pelo *Evidence Service* e processados pelo *Execution Service*.

```
Recomendação (ID) ➔ Raciocínio (Grau de Incerteza) ➔ Evidência Limpa (ID + Hash) ➔ Arquivo Bruto de Origem (Hash SHA-256)
```

### Consequências e Impacto
- **Positivas**: Auditoria cega e bidirecional instantânea (é possível clicar em uma recomendação e puxar todas as linhas originais por trás dela em menos de um segundo).
- **Negativas**: Custo computacional adicional para estruturar e persistir os esquemas de metadados relacionais a cada execução do pipeline.

---

## [ADR-0003] Customização por Context Packages Isolados

### Contexto e Problema
Como demonstrar que a ALCATEIA é uma arquitetura corporativa generalizável de inteligência e não um software construído exclusivamente para o caso específico do "Mapa da Noite"?

### Decisão de Projeto
O núcleo da ALCATEIA (os seis serviços e os esquemas de banco de dados e auditoria) é totalmente agnóstico de domínio. Qualquer domínio de entrada deve ser embarcado através de um **Context Package** padronizado, que atua como um "plugin" de regras que se conecta à ALCATEIA. 
O Context Package injeta:
- O dicionário taxonômico de eixos.
- As regras específicas de conformidade de privacidade (ex.: palavras-chave a expurgar).
- A lista de mapeamento de fontes de evidência oficiais autorizadas.
- Os critérios específicos de corte (fuso horário, datas de referência).

### Consequências e Impacto
- **Positivas**: Comprovamos a independência de domínio apresentando o Mapa da Noite como *Context Package 1* (caso principal demonstrável) e Inteligência Territorial em Saúde como *Context Package 2* (caso de generalização).
- **Negativas**: Requer a criação de adaptadores formais que limitem as ontologias para que o motor da ALCATEIA consiga interpretá-las de maneira uniforme.
