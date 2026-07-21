from typing import Dict, List, Any
from .base import BaseContextPackage

class SaudeTerritorialContextPackage(BaseContextPackage):
    """
    Pacote de contexto simulado para Inteligência Territorial em Saúde e Proteção Social.
    Demonstra a independência de domínio e capacidade de generalização da ALCATEIA.
    """

    @property
    def package_id(self) -> str:
        return "saude_territorial_v1"

    @property
    def name(self) -> str:
        return "Inteligência Territorial - Saúde e Assistência Social"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_compliance_rules(self) -> Dict[str, Any]:
        return {
            "expunge_patterns": [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", # E-mails
                r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\s?\d{4}-?\d{4}|\d{4}-?\d{4})\b" # Celulares/Telefones
            ],
            "strip_urls": True,
            "anonymize_profiles": True,
            "strip_replies": True
        }

    def get_sources_mapping(self) -> Dict[str, Dict[str, Any]]:
        # Mapeamento estático simulado para o domínio de Saúde
        return {
            "FON-SAUDE-0001": {
                "arquivo_nome": "saude_ubs_sul_20260601.xlsx",
                "arquivo_path": "simulado_ubs_sul.xlsx",
                "hash_sha256": "88484ccce206e751a27bddd67618862d812be1c42b1f943e71fa3416e78fcabc",
                "quantidade_linhas_diario": 120
            }
        }

    def get_taxonomy_definitions(self) -> Dict[str, List[str]]:
        return {
            "atendimento_medico": [
                "médico", "medico", "consulta", "atendimento", "espera", "demora", "médica", "clínico"
            ],
            "insumos_e_remedios": [
                "remédio", "remedio", "medicamento", "vacina", "falta", "farmácia", "remédios", "insumos"
            ],
            "infraestrutura_ubs": [
                "ubs", "posto", "posto de saúde", "limpeza", "cadeira", "ar condicionado", "estrutura", "banheiro"
            ],
            "assistencia_social": [
                "cras", "creas", "benefício", "auxílio", "cadastro único", "bolsa família", "assistente social"
            ],
            "fora_classificacao_textual": [
                "emoji isolado", "marcação", "hashtag"
            ]
        }

    def get_mock_reasoning_data(self) -> Dict[str, Dict[str, Any]]:
        return {
            "insumos": {
                "eixo": "insumos_e_remedios",
                "evidencia": "Fui ao posto de saúde ontem e disseram que está faltando vacina de gripe e remédio de pressão.",
                "justificativa": "Reclamação direta sobre desabastecimento de imunizantes e medicamentos de uso contínuo.",
                "nivel_confianca": "alto",
                "sugestao": "Acionar o canal de distribuição municipal e remanejar o estoque excedente da UBS vizinha."
            },
            "atendimento": {
                "eixo": "atendimento_medico",
                "evidencia": "A fila da triagem demorou 2 horas porque só tinha um clínico geral atendendo.",
                "justificativa": "Relato de tempo de espera excessivo associado à escassez de profissionais médicos escalados.",
                "nivel_confianca": "alto",
                "sugestao": "Redistribuir a grade de plantões e implantar triagem eletrônica prioritária para idosos."
            }
        }
