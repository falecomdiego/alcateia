import time
import datetime
from typing import Dict, Any, Optional
from .db import get_db_connection

class ApiTelemetryManager:
    """
    Gerenciador de Telemetria e Observabilidade de API da ALCATEIA.
    Registra requisições externas, headers de controle (x-request-id e X-Client-Request-Id),
    monitora rate limits (x-ratelimit-*) e gerencia resiliência contra erros HTTP 429.
    """

    @staticmethod
    def generate_client_request_id(rodada_id: str, agent_id: str, sequence_num: int = 1) -> str:
        """Gera um identificador único de requisição do cliente alinhado ao padrão ALCATEIA."""
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        return f"ALCATEIA-{rodada_id}-{agent_id}-EXEC-{today_str}-{sequence_num:03d}"

    @classmethod
    def log_api_call(
        cls,
        endpoint: str,
        model: str,
        status_code: int,
        client_request_id: str,
        request_id: Optional[str] = None,
        processing_ms: Optional[int] = None,
        rate_limits: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Estrutura e registra a telemetria de uma chamada de API para auditabilidade e suporte.
        """
        telemetry_entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "endpoint": endpoint,
            "model": model,
            "status_code": status_code,
            "client_request_id": client_request_id,
            "request_id": request_id or "N/A",
            "processing_ms": processing_ms or 0,
            "rate_limits": rate_limits or {},
            "error": error or ("rate_limit_exceeded" if status_code == 429 else None)
        }
        return telemetry_entry

    @classmethod
    def handle_rate_limit_retry(cls, max_retries: int = 3, initial_delay: float = 1.0):
        """
        Auxiliar para retry com backoff exponencial quando ocorre HTTP 429 (Rate Limit Exceeded).
        """
        delay = initial_delay
        for attempt in range(1, max_retries + 1):
            yield attempt, delay
            time.sleep(delay)
            delay *= 2.0


class MonitoringService:
    """
    Monitoring Service: Acompanha a execução e monitora resultados.
    Persiste de forma definitiva as Cadeias de Evidência e gerencia a telemetria e observabilidade do ciclo.
    """

    @staticmethod
    def save_and_close_cycle(evidence_chain: Dict[str, Any]) -> Dict[str, Any]:
        """
        Salva de forma definitiva a Cadeia de Evidência no SQLite relacional (se disponível)
        e altera o status da demanda investigativa para resolvido.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        demanda_id = evidence_chain["demanda_id"]
        chain_id = evidence_chain["mue_id"]
        eixo = evidence_chain["eixo_central"]
        incerteza = evidence_chain["nivel_confianca"]
        revisor = evidence_chain["revisor_humano"]
        data_auditoria = evidence_chain["data_auditoria"]
        assinatura = evidence_chain["assinatura_mue"]

        # 1. Salvar registros na tabela de cadeias_evidencia
        for idx, ev in enumerate(evidence_chain["evidencias_factuais"]):
            cursor.execute(
                """
                INSERT INTO cadeias_evidencia (
                    chain_id, demanda_id, fonte_id, registro_id, texto_evidencia, 
                    categoria_taxonomica, grau_incerteza, hash_origem, aprovador_humano, data_auditoria
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(chain_id) DO NOTHING
                """,
                (
                    f"{chain_id}-{idx}",
                    demanda_id,
                    ev["fonte_id"],
                    ev["registro_id"],
                    ev["texto_original"],
                    eixo,
                    incerteza,
                    assinatura, # Usando a assinatura como âncora de segurança
                    revisor,
                    data_auditoria
                )
            )

        # 2. Atualizar o status da demanda para 'encerrado'
        cursor.execute(
            """
            UPDATE demandas_investigacao
            SET status = 'resolvido'
            WHERE demanda_id = ?
            """,
            (demanda_id,)
        )

        conn.commit()
        conn.close()

        # Retorna indicadores sintéticos do monitoramento
        return {
            "status_monitoramento": "sucesso",
            "cadeia_evidencia_id": chain_id,
            "registros_salvos": len(evidence_chain["evidencias_factuais"]),
            "data_registro": data_auditoria,
            "assinatura_criptografica": assinatura
        }
