# 🐺 ALCATEIA — Evidence-Oriented Multi-Agent Architecture (v1.0)

Este diretório contém o MVP funcional purificado da arquitetura **ALCATEIA**, desenvolvida como um ecossistema desacoplado, performático e genérico para orquestração de inteligência baseada em evidências.

A arquitetura foi implementada em estrita conformidade com os princípios normativos de engenharia estabelecidos em `ALCATEIA-ARC-001-V1.0.md` e validada cientificamente por meio do experimento formal `ALCATEIA-EXP-001-V1.0.md`, garantindo a integridade e linhagem ativa de dados do Marco Zero do projeto.

---

## 🏗️ Estrutura de Módulos e Componentes

O núcleo do sistema foi purificado para rodar **totalmente em memória (livre de bancos de dados locais)** para ganho exponencial de desempenho, garantindo a gravação física dos resultados estruturados no disco:

*   **`core/`**: Serviços centrais de baixo nível.
    *   `discovery.py`: **Discovery Service** (recebe e qualifica a pergunta central da investigação).
    *   `evidence.py`: **Evidence Service** (realiza auditoria criptográfica `SHA-256` recursiva das fontes).
    *   `execution.py`: **Execution Service** (saneamento determinístico e remoção de dados pessoais sob LGPD).
    *   `reasoning.py`: **Reasoning Service** (análise taxonômica cognitiva com suporte opcional e nativo à **API oficial da OpenAI**).
    *   `audit.py`: **Audit Service** (validação lógica cruzada de linhagens, assinatura digital e exportação física de artefatos).
*   **`context_packages/`**: Plugins e adaptadores declarativos de domínios específicos.
    *   `base.py`: Classe abstrata que estabelece as diretrizes de conformidade de pacotes de contexto.
    *   `mapa_da_noite.py`: Conector real do **Mapa da Noite** integrado ao diário oficial de coletas (7.468 comentários brutos).
    *   `saude_territorial.py`: Conector simulado de **Saúde e Proteção Social**, comprovando a total independência de domínio da arquitetura.
*   **`output/`**: Pasta gerada dinamicamente onde são guardados os relatórios consolidados em formato JSON-LD.
*   **`tests/`**: Testes integrados de regressão.
*   **`main.py`**: Orquestrador e CLI de alta performance.

---

## 🚀 Como Executar (Fluxo Completo Ágil)

### 1. Instalar as Dependências (Leves e Seguras)
```bash
pip install -r requirements.txt
```

### 2. Configurar a Chave da API da OpenAI (Opcional - Para Modo Live)
Caso queira que o Reasoning Agent utilize a inteligência real do modelo **GPT-5.6** para formular a hipótese e recomendação:
```bash
# Windows PowerShell:
$env:OPENAI_API_KEY="SUA_CHAVE_AQUI"

# Windows Command Prompt:
set OPENAI_API_KEY=SUA_CHAVE_AQUI
```

### 3. Modo Demonstrativo Offline (Repetibilidade para a Banca)
Caso execute sem chave ou queira demonstrar a repetibilidade impecável off-line de forma ultrarrápida:

*   **Caso 1 (Mapa da Noite)**:
    ```bash
    python -m alcateia.main --context mapa_da_noite --question "Como está a infraestrutura do bar ou pista open air?"
    ```
*   **Caso 2 (Saúde Territorial)**:
    ```bash
    python -m alcateia.main --context saude_territorial --question "Como está o abastecimento de vacinas e remédios de pressão?"
    ```

### 4. Modo Live Real (Conectado à API da OpenAI)
Adicione o flag `--live` para acionar dinamicamente o modelo generativo da OpenAI sob os comentários sanitizados da base mestre:
```bash
python -m alcateia.main --context mapa_da_noite --question "Como está a infraestrutura do bar ou pista open air?" --live
```

---

## 🧪 Validação Técnica & Testes
Para rodar a bateria de testes integrados e unitários da ALCATEIA (que valida desde a higienização de dados pessoais até o travamento imediato do pipeline em caso de violação de hashes):
```bash
python -m unittest alcateia.tests.test_flow
```
*   **Desempenho**: Devido à purificação em memória, a suíte completa de testes executa de forma muito rápida e otimizada, reduzindo drasticamente o overhead de conexões externas.

---

## 📂 Artefatos de Saída (Matriz Única de Evidência)
A cada execução bem-sucedida, o `AuditService` gera e grava fisicamente na pasta `alcateia/output/` dois arquivos:
1.  `mue_latest.json`: O resultado final da última execução realizada.
2.  `mue_ALC-MUE-[ID].json`: Cópia histórica selada digitalmente pela assinatura SHA-256 da cadeia.

### Exemplo de Estrutura de Evidência Rastreável (JSON-LD)
```json
{
  "mue_id": "ALC-MUE-1DC556",
  "demanda_id": "ALC-DEM-45F67E",
  "data_auditoria": "2026-07-21T05:54:27.211668",
  "eixo_central": "infraestrutura_e_operacao",
  "hipotese": "Demonstrado aumento de comentários críticos sobre infraestrutura e operacao.",
  "recomendacao_sugerida": "Aumentar em 30% os caixas móveis e redistribuir pontos de hidratação na pista open air.",
  "nivel_confianca": "alto",
  "origens_verificadas": [
    {
      "fonte_id": "MDN-RPP01-FON-0001",
      "hash_sha256": "b01e73772935ab8dec3e47d906c98b7ab0c57e8e146af60cec7c943f9ffd6c44"
    }
  ],
  "evidencias_factuais": [
    {
      "registro_id": "REG-10",
      "fonte_id": "MDN-RPP01-FON-0001",
      "linha_origem": 11,
      "texto_original": "@felipecesarco agora eles sabem tudo sobre superlotação e qualidade do espaço pro publico 😂",
      "hash_origem": "[ANON_USER_ID]"
    }
  ],
  "versao_arquitetura": "ALCATEIA v1.0",
  "revisor_humano": "Diego da Silva (Aprovação Nominal)",
  "assinatura_mue": "fff8b65357efba30d690d5ed47b4b392b0c3b3a844d59e90fa84b1986e2e8fcb",
  "artefatos_exportados": {
    "diretorio": "C:\\Users\\Diego\\Documents\\Codex\\2026-06-15\\analise_comentarios_evento\\alcateia\\output",
    "latest_file": "mue_latest.json",
    "historical_file": "mue_ALC-MUE-1DC556.json"
  }
}
```
---
## 🤝 Como colaboramos com o Codex e GPT-5.6

Durante o OpenAI Build Week, o **Codex** foi essencial para acelerar e fundamentar decisões arquiteturais chave:
1. **Engenharia e Arquitetura:** O Codex sugeriu o isolamento entre o *Reasoning Service* (inferência probabilística) e o *Execution Service* (automação determinística e remoção de LGPD). 
2. **Qualidade do Código:** Acelerou a construção dos *Context Packages* baseados em interfaces limpas e os testes de regressão automatizados (`unittest`).
3. **Integração GPT-5.6:** Auxiliou na implementação da *Responses API* e dos *Structured Outputs*, assegurando que a MUE (Matriz Única de Evidência) seja gerada como um JSON determinístico e sem alucinações.
4. **Session ID Principal:** `c6da3fb9-faae-4d27-999b-57c869ce3548` (Utilizada para toda a fase de implementação e refinamento técnico do projeto).

---
*Desenvolvido por Diego da Silva como submissão de alta competitividade para a OpenAI Build Week.*
