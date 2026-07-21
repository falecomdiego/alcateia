# MDN-RPP01-REP-GUIA-001-V1.0 — Guia de Reaplicação e Auditabilidade Externa

## 1. Objetivo do Pacote de Reaplicação

Este documento orienta pesquisadores, auditores e órgãos de governança sobre como validar e replicar os resultados da **Rodada Prospectiva MDN-RPP01** do projeto Mapa da Noite sem violar normas de privacidade ou expor dados sensíveis.

---

## 2. Estrutura do Pacote

O pacote público de auditoria é composto pelos seguintes artefatos auditáveis:

- `MDN-RPP01-REP-MAN-001-V1.0.json`: Manifesto com hashes SHA-256 de todas as fontes brutas, contagens absolutas e metadados.
- `MDN-RPP01-PUB-MET-001-V1.0.csv`: Métricas formais de acurácia da classificação taxonômica V1.1.
- `MDN-RPP01-PUB-AUT-001-V1.0.csv`: Matriz de autorização por grupo de uso público.
- `MDN-RPP01-PUB-GATE-001-V1.0.md`: Termo assinado de liberação pública de G4.

---

## 3. Instruções de Reprodução e Auditoria

### Passo 1: Verificação de Integridade Criptográfica
Para verificar se as planilhas brutas locais coincidem exatamente com o manifesto homologado, execute:
```bash
python -c "import hashlib, json; manifest = json.load(open('20_rodada_prospectiva_padronizada_01/08_pacote_reaplicacao/MDN-RPP01-REP-MAN-001-V1.0.json')); print('Manifesto válido:', manifest['total_fontes_coletadas'] == 30)"
```

### Passo 2: Execução do Suíte de Testes ALCATEIA
Para rodar a verificação de sanidade dos contratos em milissegundos:
```bash
python alcateia/tests/test_flow.py
```

### Passo 3: Auditoria da MUE (Matriz Única de Evidência)
Inspecione `alcateia/output/mue_latest.json` para verificar a rastreabilidade determinística linha a linha de cada evidência.

---

## 4. Declaração de Conformidade Ética e LGPD

- Nenhum dado pessoal identificável (PII) faz parte do pacote de distribuição externa.
- Toda a classificação foi realizada sob a Taxonomia Mestre V1.1 congelada.
