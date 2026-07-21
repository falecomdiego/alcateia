# MDN-RPP01-STATUS-001-V1.0 — Status de implantação

## Data

21/07/2026

## Estado atual

A rodada prospectiva **MDN-RPP01** concluiu com sucesso a sua fase de coleta de dados (**Gate G1 aprovado** por meio da decisão formal `MDN-RPP01-DEC-0015`). 

Todas as 30 publicações previstas no inventário de fontes foram extraídas manualmente via extensão Chrome homologada (conforme decisão `MDN-RPP01-DEC-0014`) e auditadas de forma rigorosa por meio do script de diagnóstico técnico. Um volume total de **7.468 comentários brutos** foi consolidado e registrado no Diário de Coletas (`MDN-RPP01-COL-001-V0.1.csv`), acompanhado por suas respectivas contagens de registros e hashes imutáveis `SHA-256`. 

O **Gate G2 (Análise por lote)** está formalmente liberado para execução.

---

## Alteração temporal

- período anterior: 01/06/2026 a 15/06/2026;
- período vigente no manifesto: 01/06/2026 a 30/06/2026;
- motivo: incluir comentários e repercussões posteriores ao dia 15 relacionados às festas do período de Corpus Christi;
- regra: aplicar a janela completa a todas as fontes aprovadas;
- proibição: selecionar apenas comentários ou fontes já conhecidos como relevantes depois do corte original;
- configuração executável: período oficial de 01/06/2026 a 30/06/2026 ativado na configuração do JSON.

---

## Campos definidos

- campo: Tribal House em São Paulo;
- contextos comparáveis: clubes fechados e `open air`;
- pergunta central operacionalizada na janela de 1 a 30 de junho;
- responsável da rodada, operador de coleta, responsável metodológico, responsável pela proteção de dados e responsável pela publicação: Diego da Silva;
- revisora independente: Kacia Oliveira (aceite formal direto e disponibilidade registrados);
- retenção de dados protegidos: 12 meses após encerramento de G1 (iniciando em 21/07/2026);
- ferramenta de coleta real: Extensão Chrome homologada (minimização prévia de e-mail, telefone e replies ativa).

---

## Inventário de fontes e status de coleta (30/30)

O diário oficial de coletas `01_fontes_e_coleta/MDN-RPP01-COL-001-V0.1.csv` foi totalmente preenchido e auditado, apontando os seguintes resultados técnicos das extrações brutas:

| Fonte ID | Coleta ID | Linhas Brutas | Hash SHA-256 | Status |
| :--- | :---: | :---: | :--- | :---: |
| `FON-0001` | `COL-0001` | 256 | `b01e737729...` | Sucesso |
| `FON-0002` | `COL-0002` | 485 | `9eee7f0749...` | Sucesso |
| `FON-0003` | `COL-0003` | 246 | `e361fcbc50...` | Sucesso |
| `FON-0004` | `COL-0004` | 48 | `603adac627...` | Sucesso |
| `FON-0005` | `COL-0005` | 611 | `3a53f959b7...` | Sucesso |
| `FON-0006` | `COL-0006` | 142 | `d11f45be0b...` | Sucesso |
| `FON-0007` | `COL-0007` | 113 | `30fc75495a...` | Sucesso |
| `FON-0008` | `COL-0008` | 49 | `47dbe6d140...` | Sucesso |
| `FON-0009` | `COL-0009` | 229 | `b2a1dd0f80...` | Sucesso |
| `FON-0010` | `COL-0010` | 25 | `acd157a301...` | Sucesso |
| `FON-0011` | `COL-0011` | 64 | `59ed21966d...` | Sucesso |
| `FON-0012` | `COL-0012` | 1944 | `1d11cdac58...` | Sucesso |
| `FON-0013` | `COL-0013` | 486 | `fb608e23e2...` | Sucesso |
| `FON-0014` | `COL-0014` | 42 | `1c0014a4f8...` | Sucesso |
| `FON-0015` | `COL-0015` | 57 | `c34f8eda8c...` | Sucesso |
| `FON-0016` | `COL-0016` | 41 | `9f32003ea6...` | Sucesso |
| `FON-0017` | `COL-0017` | 53 | `bae9cd6144...` | Sucesso |
| `FON-0018` | `COL-0018` | 168 | `74cc12fae9...` | Sucesso |
| `FON-0019` | `COL-0019` | 51 | `16c6467ab8...` | Sucesso |
| `FON-0020` | `COL-0020` | 51 | `879621a928...` | Sucesso |
| `FON-0021` | `COL-0021` | 29 | `1d5b2e480b...` | Sucesso |
| `FON-0022` | `COL-0022` | 165 | `b0f3ea9797...` | Sucesso |
| `FON-0023` | `COL-0023` | 659 | `88484ccce2...` | Sucesso |
| `FON-0024` | `COL-0024` | 228 | `1124728a4e...` | Sucesso |
| `FON-0025` | `COL-0025` | 398 | `220df39b44...` | Sucesso |
| `FON-0026` | `COL-0026` | 117 | `e98b535920...` | Sucesso |
| `FON-0027` | `COL-0027` | 269 | `d3be164853...` | Sucesso |
| `FON-0028` | `COL-0028` | 131 | `d0c1f78306...` | Sucesso |
| `FON-0029` | `COL-0029` | 170 | `730fbf9199...` | Sucesso |
| `FON-0030` | `COL-0030` | 141 | `290c1a7848...` | Sucesso |
| **Total Geral** | | **7.468** | | |

---

## Detalhes da Coleta Manual

- **Motivo da Coleta Manual**: Conforme `MDN-RPP01-DEC-0014`, o script automático que usava Instaloader enfrentou bloqueios de requisições (`403 Forbidden`) persistentes impostos pelo endpoint do Instagram. 
- **Conformidade Metodológica**: A extração manual foi realizada sob cookies ativos da sessão do navegador e manteve o mesmo filtro estrito de conformidade. Não foram coletadas as colunas de PII (`User ID`, `Avatar URL`, `Profile URL` e `User Name`) para versionamento público, permanecendo apenas na camada tratada e protegida.
- **Minimização de Dados**: E-mails, telefones e replies foram desativados/excluídos na origem durante a extração da extensão Chrome.

---

## Estado dos gates

| Gate | Estado |
|---|---|
| G0 — Protocolo | aprovado |
| G1 — Coleta | aprovado |
| G2 — Análise por lote | liberado para execução |
| G3 — Consolidação | bloqueado |
| G4 — Publicação | bloqueado |
| G5 — Reaplicação externa | bloqueado |

Aprovado em 21/07/2026 por decisão formal registrada no diário de decisões (`MDN-RPP01-DEC-0015`).
