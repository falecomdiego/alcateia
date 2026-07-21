import os
import csv
from typing import Dict, List, Any
from .base import BaseContextPackage

class MapaDaNoiteContextPackage(BaseContextPackage):
    """
    Pacote de contexto para o Mapa da Noite (MDN-RPP01).
    Integra de forma direta com o diário oficial de coletas e a pasta de dados protegidos.
    """

    @property
    def package_id(self) -> str:
        return "mapa_da_noite_v1"

    @property
    def name(self) -> str:
        return "Mapa da Noite - Tribal House SP"

    @property
    def version(self) -> str:
        return "1.1.0"

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
        """
        Carrega dinamicamente o mapeamento de fontes a partir do diário de coletas oficial.
        """
        mapping = {}
        # Caminho oficial relativo para o diário de coletas do Mapa da Noite
        diario_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "20_rodada_prospectiva_padronizada_01", "01_fontes_e_coleta", "MDN-RPP01-COL-001-V0.1.csv"
        ))
        
        # Se não encontrar no caminho relativo esperado, procura na raiz de dados protegidos
        dados_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "20_rodada_prospectiva_padronizada_01", "02_dados_brutos_protegidos", "dados"
        ))

        if not os.path.exists(diario_path):
            return mapping

        with open(diario_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Se a linha for o cabeçalho de metadados extra ou vazia, pula
                if not row.get("fonte_id"):
                    continue
                
                fonte_id = row["fonte_id"]
                arquivo_nome = row["arquivo_gerado"]
                arquivo_completo_path = os.path.join(dados_dir, arquivo_nome)
                
                mapping[fonte_id] = {
                    "arquivo_nome": arquivo_nome,
                    "arquivo_path": arquivo_completo_path,
                    "hash_sha256": row["hash_sha256"],
                    "quantidade_linhas_diario": int(row["quantidade_linhas"])
                }
        return mapping

    def get_taxonomy_definitions(self) -> Dict[str, List[str]]:
        return {
            "infraestrutura_e_operacao": [
                "fila", "bar", "pista", "som", "luz", "iluminação", "acústica",
                "banheiro", "banheiros", "chapelaria", "estrutura", "espaço", "entrada", "open air"
            ],
            "seguranca_e_saude": [
                "segurança", "seguranca", "brigada", "médico", "medico", "ambulância", 
                "ambulancia", "briga", "roubo", "furto", "empurra", "pânico", "queda"
            ],
            "reputacao_e_marca": [
                "evento", "festa", "curti", "amei", "decepção", "decepcao", "lixo",
                "maravilhoso", "selo", "organização", "organizacao", "flop", "top", "lindo"
            ],
            "atendimento_e_servico": [
                "atendimento", "staff", "host", "hostess", "garçom", "garcom", "bebida", "caixa", "ficha"
            ],
            "fora_classificacao_textual": [
                "emoji isolado", "marcação", "hashtag"
            ]
        }

    def get_mock_reasoning_data(self) -> Dict[str, Dict[str, Any]]:
        return {
            "infraestrutura": {
                "eixo": "infraestrutura_e_operacao",
                "evidencia": "Fila do bar demorou mais de 40 minutos para pegar uma água na pista open air.",
                "justificativa": "Reclamação explícita sobre tempo de espera no bar e localização na pista open air.",
                "nivel_confianca": "alto",
                "sugestao": "Aumentar em 30% os caixas móveis e redistribuir pontos de hidratação na pista open air."
            },
            "seguranca": {
                "eixo": "seguranca_e_saude",
                "evidencia": "Houve empurra-empurra na entrada e não vi brigadistas ou seguranças orientando.",
                "justificativa": "Relato de risco de pisoteamento devido a empurra-empurra e falta de coordenação de segurança.",
                "nivel_confianca": "alto",
                "sugestao": "Reestruturar as grades de contenção de fluxo na entrada e posicionar brigadistas a cada 10 metros."
            },
            "geral": {
                "eixo": "reputacao_e_marca",
                "evidencia": "O som estava incrível e a iluminação impecável, mas a organização pecou no acesso.",
                "justificativa": "Elogio técnico de luz e som contrastado com crítica de acessibilidade geral.",
                "nivel_confianca": "médio",
                "sugestao": "Manter os fornecedores de iluminação e som e auditar o plano de fluxo do portão de entrada."
            }
        }
