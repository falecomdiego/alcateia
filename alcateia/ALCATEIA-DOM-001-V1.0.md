# ALCATEIA — Modelo de Domínio e Contratos de Interfaces v1.0

**Status**: FROZEN (Architecture Freeze v1.0)  
**Objetivo**: Especificar as entidades de domínio e os contratos lógicos (JSON) de entrada e saída das interfaces dos serviços.  
**Data**: 21/07/2026  

---

## 1. Modelo de Domínio

O modelo de domínio da ALCATEIA conceitualiza o fluxo analítico por meio de quatro entidades fundamentais e de suas relações relacionais:

```
+---------------------+         +---------------------+
|   ContextPackage    |1       *|     FonteEvidencia  |
| (Ontologia, Regras) +-------->+  (Publicação, URL)  |
+---------------------+         +----------+----------+
                                           |1
                                           |
                                           |*
+---------------------+         +----------v----------+
|     Recomendacao    |*       1|   RegistroEvidencia |
| (Decisão, Confiança)+-------->+ (Comentário, Hash)  |
+---------------------+         +---------------------+
```

1. **ContextPackage**: O contêiner de regras de negócio específicas para um domínio.
2. **FonteEvidencia**: O ponto de entrada físico ou digital de onde dados são coletados (ex.: URL da publicação, documento PDF).
3. **RegistroEvidencia**: O fragmento elementar de dado limpo extraído, normalizado e imutável (ex.: o comentário isolado).
4. **Recomendacao**: O artefato analítico gerado com base no raciocínio estruturado, que apóia e documenta a decisão humana.

---

## 2. Estrutura do Context Package (Esquema JSON)

Cada domínio de aplicação se conecta ao orquestrador ALCATEIA por meio do seguinte contrato estruturado:

```json
{
  "$schema": "https://alcateia.architecture/schemas/context-package.json",
  "package_id": "mapa_da_noite_v1",
  "name": "Mapa da Noite - Tribal House SP",
  "version": "1.1.0",
  "ontology": {
    "taxonomy_ref": "TAXONOMIA_MESTRE_MAPA_DA_NOITE_V1_1.md",
    "taxonomy_hash": "e6a2c5ef821bc1829da421de72ff91ba27cd7ff2b1a823e20decd2882a17cbde"
  },
  "compliance_rules": {
    "expunge_patterns": [
      "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
      "\\b\\d{2}\\s?\\d{4,5}-?\\d{4}\\b"
    ],
    "strip_urls": true,
    "anonymize_profiles": true
  },
  "operational_window": {
    "start_date": "2026-06-01T00:00:00-03:00",
    "end_date": "2026-06-30T23:59:59-03:00",
    "timezone": "America/Sao_Paulo"
  }
}
```

---

## 3. Contratos de Interfaces dos Seis Serviços Core

As comunicações e os acoplamentos lógicos entre as fronteiras dos seis serviços operacionais são governados pelos seguintes contratos JSON de entrada e saída.

### Interface I-01: Discovery Service ➔ Evidence Service
- **Contrato**: Cadastro e qualificação do tema ou postagem pendente de investigação.

```json
// Input (Postagem mapeada a investigar)
{
  "request_id": "ALC-REQ-2026-001",
  "context_package": "mapa_da_noite_v1",
  "target_source_url": "https://www.instagram.com/p/DZ7sL_pHIgG/",
  "contexto_classificacao": "open air",
  "justificativa_prioridade": "Selo de maior engajamento e repercussão de Corpus Christi.",
  "operador_responsavel": "Diego Silva"
}
```

### Interface I-02: Evidence Service ➔ Execution Service
- **Contrato**: Diário oficial de auditoria técnica das coletas brutas.

```json
// Output (Diário de coleta autenticada com hash do bruto)
{
  "coleta_id": "ALC-COL-0001",
  "fonte_id": "FON-0001",
  "context_package": "mapa_da_noite_v1",
  "resultado_coleta": "sucesso",
  "arquivo_bruto_nome": "MDN-RPP01-RAW-FON-0001-COL-20260720.xlsx",
  "arquivo_bruto_sha256": "b01e73772935ab8dec3e47d906c98b7ab0c57e8e146af60cec7c943f9ffd6c44",
  "total_linhas_brutas": 257,
  "data_hora_execucao": "2026-07-20T23:08:26-03:00"
}
```

### Interface I-03: Execution Service ➔ Reasoning Service
- **Contrato**: Transmissão do lote de comentários sanitizado para análise probabilística de sentimentos e taxonomia.

```json
// Output (Lote limpo sem PII ou metadados desnecessários)
{
  "batch_id": "ALC-BAT-0001",
  "context_package": "mapa_da_noite_v1",
  "registros": [
    {
      "registro_id": "REG-0001-0001",
      "texto_limpo": "A infraestrutura da pista open air estava excelente mas a fila do bar demorou muito.",
      "caracteres_isolados": [],
      "linhas_excluidas_log_vazio": false
    }
  ],
  "hashing_lote_sha256": "fc8a3de89a2bc1d82f7d906ab21ef9a27cbef216d820dcd1e1a82efcd83ea88c"
}
```

### Interface I-04: Reasoning Service ➔ Audit Service
- **Contrato**: Submissão da hipótese e classificação temática gerada pelo cérebro cognitivo.

```json
// Output (Classificação proposta dependendo de verificação)
{
  "proposta_id": "ALC-PROP-0001",
  "registro_id": "REG-0001-0001",
  "eixo_classificacao": "infraestrutura_e_operacao",
  "nuance_identificada": "tensao_fila_espera",
  "grau_confianca": "alto",
  "justificativa_linguagem": "Menção explícita a tempo de espera e serviço de bar em contexto open air.",
  "modelo_ia_versao": "gpt-5.6-turbo"
}
```

### Interface I-05: Audit Service ➔ Monitoring Service
- **Contrato**: Cadeia de evidência consolidada com carimbo de aprovação e governança imutável.

```json
// Output (Evidence Chain fechada e pronta para exibição/decisão humana)
{
  "evidence_chain_id": "ALC-EVC-0001",
  "proposta_id": "ALC-PROP-0001",
  "fonte_id": "FON-0001",
  "registro_id": "REG-0001-0001",
  "arquivo_bruto_sha256": "b01e73772935ab8dec3e47d906c98b7ab0c57e8e146af60cec7c943f9ffd6c44",
  "auditado_por": "Kacia Oliveira",
  "status_auditoria": "aprovado",
  "voto_fidelidade_taxonômica": true,
  "data_auditoria": "2026-07-21T04:30:00-03:00"
}
```
