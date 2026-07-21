# MDN-RPP01-REP-GUIA-001-V0.1 — Guia de reaplicação

## Objetivo

Permitir que uma pessoa que não participou da construção valide a configuração, execute a fixture sintética e confirme os controles do pipeline sem acessar dados reais.

## Pré-requisitos

- Python 3.11 ou superior;
- Git funcional;
- cópia autorizada do repositório;
- nenhuma dependência Python externa;
- `MDN_PSEUDONYM_KEY` definida apenas para ingestão de dados reais ou testes específicos de pseudonimização.

## Teste seguro inicial

Na raiz do projeto:

```powershell
python -m unittest discover -s pipeline_mdn_v2/tests -v
python -m pipeline_mdn_v2.mdn_pipeline.cli validate-config
python -m pipeline_mdn_v2.mdn_pipeline.cli verify-taxonomy
```

Esses comandos não leem os lotes da rodada inicial e não processam dados reais.

## Registro do terceiro

O avaliador deve registrar:

- ambiente e versões;
- comandos executados;
- resultados obtidos;
- dúvidas surgidas;
- instruções insuficientes;
- necessidade de intervenção do idealizador;
- divergências em relação aos resultados esperados.

## Critério de G5

G5 somente poderá ser aprovado se a fixture for reproduzida, as dúvidas forem registradas e nenhuma intervenção estrutural do idealizador for necessária.

