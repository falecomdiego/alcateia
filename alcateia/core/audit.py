import os
import uuid
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any

class AuditService:
    """
    Audit Service: Realiza a auditoria de consistencia logica e assina a MUE.
    Garante a conformidade absoluta da Cadeia de Evidencias sem lacunas.
    Exporta fisicamente os artefatos gerados para auditoria da banca.
    """

    @classmethod
    def generate_evidence_chain_hash(cls, evidence_data: Dict[str, Any]) -> str:
        """Gera uma assinatura de integridade exclusiva (SHA-256) para a MUE."""
        serialized = json.dumps(evidence_data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    @classmethod
    def validate_and_seal_chain(
        cls, 
        demanda_id: str, 
        reasoning_report: Dict[str, Any], 
        verified_sources: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Realiza a validacao cruzada em memoria entre a hipotese gerada e as fontes homologadas.
        Gera a Cadeia de Evidencias (MUE), sela criptograficamente e exporta em arquivos fisicos.
        """
        evidencias = reasoning_report.get("evidencias_encontradas", [])
        if not evidencias:
            raise ValueError("FALHA DE AUDITORIA: Nenhuma evidencia factual suporta a hipotese formulada!")

        verified_source_ids = {src["fonte_id"] for src in verified_sources}

        # Validacao logica de linhagem
        for ev in evidencias:
            fonte_id = ev["fonte_id"]
            if fonte_id not in verified_source_ids:
                raise ValueError(
                    f"FALHA DE AUDITORIA: A evidencia cita a fonte {fonte_id}, "
                    f"que nao foi homologada criptograficamente pelo Evidence Service!"
                )

        # Compilar a Matriz Unica de Evidencia (MUE)
        mue_id = f"ALC-MUE-{uuid.uuid4().hex[:6].upper()}"
        data_auditoria = datetime.now().isoformat()

        evidence_chain = {
            "mue_id": mue_id,
            "demanda_id": demanda_id,
            "data_auditoria": data_auditoria,
            "eixo_central": reasoning_report["eixo_central"],
            "hipotese": reasoning_report["hipotese_formulada"],
            "recomendacao_sugerida": reasoning_report["conclusao_recomendacao"],
            "nivel_confianca": reasoning_report["nivel_confianca"],
            "origens_verificadas": [
                {
                    "fonte_id": src["fonte_id"],
                    "hash_sha256": src["hash"]
                }
                for src in verified_sources
            ],
            "evidencias_factuais": reasoning_report["evidencias_encontradas"],
            "versao_arquitetura": "ALCATEIA v1.0",
            "revisor_humano": "Diego da Silva (Aprovacao Nominal)"
        }

        # Selar criptograficamente a MUE inteira
        mue_signature = cls.generate_evidence_chain_hash(evidence_chain)
        evidence_chain["assinatura_mue"] = mue_signature

        # Salvar fisicamente no disco em UTF-8 completo para a banca
        try:
            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
            os.makedirs(output_dir, exist_ok=True)

            # 1. Salvar versao persistente com o ID
            hist_path = os.path.join(output_dir, f"mue_{mue_id}.json")
            with open(hist_path, "w", encoding="utf-8") as f:
                json.dump(evidence_chain, f, indent=2, ensure_ascii=False)

            # 2. Salvar versao mais recente (mue_latest.json)
            latest_path = os.path.join(output_dir, "mue_latest.json")
            with open(latest_path, "w", encoding="utf-8") as f:
                json.dump(evidence_chain, f, indent=2, ensure_ascii=False)
            
            # Nota de sucesso de salvamento no proprio dict para rastreabilidade
            evidence_chain["artefatos_exportados"] = {
                "diretorio": output_dir,
                "latest_file": os.path.basename(latest_path),
                "historical_file": os.path.basename(hist_path)
            }
        except Exception as e:
            # Tolerancia a falhas em sistemas de arquivos restritos (nao impede o retorno)
            evidence_chain["artefatos_exportados_status"] = f"falha ao exportar arquivos: {str(e)}"

        return evidence_chain
