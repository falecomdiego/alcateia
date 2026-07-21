# Roteiro de Apresentação (Pitch de 3 Minutos) — ALCATEIA

**Projeto:** ALCATEIA — Evidence-Oriented Multi-Agent Architecture
**Desenvolvedor:** Diego da Silva
**Evento:** OpenAI Build Week

---

## 🕒 0:00 - 0:30 | O Problema (O "Por quê")

"A adoção de agentes autônomos no setor público e em ambientes corporativos de alto risco esbarra em uma barreira crítica: **a falta de rastreabilidade e governança das decisões tomadas pela IA**.
Quando pedimos para um modelo analisar milhares de comentários ou documentos, recebemos uma resposta sintética. Se essa resposta contiver uma alucinação ou omissão, não há como rastrear de qual documento exato a IA tirou aquela conclusão. 
Como tomar uma decisão estratégica se não temos a prova factual do que a fundamentou?"

## 🕒 0:30 - 1:15 | A Solução (O "Como")

"Para resolver isso, criei a **ALCATEIA**, uma arquitetura multiagente orientada a evidências. Em vez de construir prompts genéricos, a ALCATEIA quebra o processo em **microsserviços isolados** e constrói uma cadeia criptográfica do início ao fim.
Nós não trabalhamos com respostas opacas. Nós trabalhamos com a **MUE - Matriz Única de Evidência**. Cada insight gerado, cada diagnóstico, está ancorado no dado original, com assinatura SHA-256 da fonte e trilha de auditoria completa, protegendo a linhagem da informação desde o momento da coleta até a recomendação final."

## 🕒 1:15 - 2:00 | Diferenciais Competitivos e Stack OpenAI

"A ALCATEIA foi construída para escalar, mas projetada para ser **independente de domínio**. Hoje ela analisa percepção de cidadãos, amanhã pode auditar contratos.
O grande diferencial é nossa profunda integração com os novos recursos da **OpenAI Dev News**:
1. Utilizamos a **Responses API** para orquestrar de forma estruturada as interações cognitivas com o **GPT-5.6**.
2. Garantimos que toda saída seja amplamente auditável através do **Structured Outputs**, gerando a MUE no formato JSON-LD determinístico.
3. Além disso, separamos o Reasoning (inferência probabilística com GPT) do Execution (automação determinística através de código e ferramentas, utilizando Codex). 
4. Implementamos também telemetria nativa, registrando o `x-request-id` de ponta a ponta para rastreabilidade de requisições e resiliência via backoff em erros 429."

## 🕒 2:00 - 3:00 | Demonstração Prática (O "Wow")

*(Na tela, rodar o terminal CLI da ALCATEIA em tempo real)*

"Vamos ver na prática. Rodarei o sistema perguntando sobre a infraestrutura de um evento, o Mapa da Noite, consumindo milhares de comentários já anonimizados.
`(python -m alcateia.main --context mapa_da_noite --question "Como está a infraestrutura do bar ou pista open air?" --live)`

*(O script roda rapidamente na tela)*

De forma ágil o orquestrador coordena: o *Discovery Agent* analisa a pergunta, o *Execution Agent* limpa os dados pessoais (LGPD), o *Reasoning Agent* utiliza o **GPT-5.6** e formula uma hipótese fundamentada. E o mais importante, o *Audit Agent* fecha o ciclo garantindo que a MUE gerada passe por validação criptográfica.
Minimizando alucinações. Com rastreabilidade integral. Pronto para a escala da administração pública ou uso corporativo de missão crítica.
Essa é a ALCATEIA. Muito obrigado."
