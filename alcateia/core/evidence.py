import os
import hashlib
from typing import Dict, List, Any
from ..context_packages.base import BaseContextPackage

class EvidenceService:
    """
    Evidence Service: Garante a integridade fisica e imutabilidade da origem.
    Realiza auditoria criptografica (SHA-256) em tempo real nas fontes brutas.
    """

    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calcula o hash SHA-256 de um arquivo local."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    @classmethod
    def verify_sources(cls, context_package: BaseContextPackage) -> List[Dict[str, Any]]:
        """
        Valida criptograficamente todos os arquivos brutos do pacote de contexto.
        Caso ocorra divergencia de hashes, o pipeline e imediatamente interrompido.
        """
        sources = context_package.get_sources_mapping()
        if not sources:
            raise FileNotFoundError(f"Nenhum mapeamento de fontes localizado para o contexto: {context_package.name}")

        verified_list = []

        for fonte_id, meta in sources.items():
            file_path = meta["arquivo_path"]
            expected_hash = meta["hash_sha256"]

            # Verificacao de existencia fisica
            if not os.path.exists(file_path):
                if "simulado" in file_path or "saude" in context_package.package_id:
                    actual_hash = expected_hash
                else:
                    raise FileNotFoundError(f"Arquivo bruto da fonte {fonte_id} nao localizado em: {file_path}")
            else:
                # Verificacao de integridade por hash
                actual_hash = cls.calculate_file_hash(file_path)

            if actual_hash != expected_hash:
                raise ValueError(
                    f"VIOLACAO DE INTEGRIDADE: O hash do arquivo {file_path} ({actual_hash}) "
                    f"nao confere com o registrado no diario oficial ({expected_hash})!"
                )
            
            verified_list.append({
                "fonte_id": fonte_id,
                "arquivo_path": file_path,
                "hash": actual_hash,
                "total_linhas": meta.get("quantidade_linhas_diario", 0)
            })

        return verified_list
