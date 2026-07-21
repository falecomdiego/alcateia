import uuid
from datetime import datetime
from typing import Dict, Any

class DiscoveryService:
    """
    Discovery Service: Identifica, qualifica e prioriza o problema.
    Registra a demanda de investigação de forma estruturada.
    """

    @staticmethod
    def register_demand(context_package_id: str, question: str) -> Dict[str, Any]:
        """
        Qualifica e registra uma nova demanda de investigação.
        """
        if not question or len(question.strip()) < 10:
            raise ValueError("A pergunta de investigacao fornecida e muito curta ou invalida.")

        demanda_id = f"ALC-DEM-{uuid.uuid4().hex[:6].upper()}"
        data_hora = datetime.now().isoformat()
        status = "qualificado"

        return {
            "demanda_id": demanda_id,
            "context_package": context_package_id,
            "pergunta": question,
            "data_hora": data_hora,
            "status": status
        }
