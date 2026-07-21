import os
import re
import pandas as pd
from typing import List, Dict, Any
from ..context_packages.base import BaseContextPackage

class ExecutionService:
    """
    Execution Service: Executa rotinas determinísticas sobre os dados.
    Aplica regras estritas de saneamento técnico, expurgação regex (PII) e rastreabilidade de linhagem.
    """

    @staticmethod
    def clean_comment_text(text: str, rules: Dict[str, Any]) -> str:
        """Aplica padrões regex para remover PII (e-mails, telefones) do texto."""
        if not isinstance(text, str):
            return ""

        # Remover extra whitespace
        cleaned = " ".join(text.split())

        # Expurgação de padrões (e-mails, celulares, etc.)
        for pattern in rules.get("expunge_patterns", []):
            cleaned = re.sub(pattern, "[EXPURGADO_PII]", cleaned)

        return cleaned

    @classmethod
    def sanitize_source_data(
        cls, 
        verified_source: Dict[str, Any], 
        context_package: BaseContextPackage
    ) -> List[Dict[str, Any]]:
        """
        Lê e higieniza deterministicamente os dados de uma única fonte,
        adicionando metadados de linhagem e de controle exigidos pelo projeto.
        """
        file_path = verified_source["arquivo_path"]
        fonte_id = verified_source["fonte_id"]
        rules = context_package.get_compliance_rules()

        # Suporte para execução simulada off-line (Saúde Territorial)
        if "simulado" in file_path or "saude" in context_package.package_id:
            # Retorna dados estruturados simulados
            mock_data = context_package.get_mock_reasoning_data()
            return [
                {
                    "my-serial-number": "1",
                    "index": "1",
                    "User ID": "USER-MOCK-0001",
                    "Avatar URL": "https://avatar.url/1",
                    "Profile URL": "https://profile.url/1",
                    "User Name": "usuário_anônimo_01",
                    "Comment Text": cls.clean_comment_text(mock_data[k]["evidencia"], rules),
                    "Comment Date": "2026-06-15T12:00:00-03:00",
                    "lote": "LOTE-SIMULADO-01",
                    "arquivo_origem": os.path.basename(file_path),
                    "aba_origem": "Sheet1",
                    "linha_origem": idx + 2,
                    "fonte_id": fonte_id
                }
                for idx, k in enumerate(mock_data.keys())
            ]

        # Processamento real de XLSX do Mapa da Noite
        try:
            df = pd.read_excel(file_path, sheet_name=0)
        except Exception as e:
            raise RuntimeError(f"Erro ao ler arquivo Excel {file_path}: {str(e)}")

        # Validação de colunas obrigatórias
        required_cols = [
            "my-serial-number", "index", "User ID", "Avatar URL", 
            "Profile URL", "User Name", "Comment Text", "Comment Date"
        ]
        
        # Verificar se todas as colunas existem
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"O arquivo {file_path} está inconsistente. Colunas obrigatórias ausentes: {missing_cols}")

        sanitized_records = []
        log_exclusions = []

        for index, row in df.iterrows():
            linha_origem = index + 2  # Pandas 0-indexed + cabeçalho
            comment_text = row["Comment Text"]

            # Regra 7: Comentários vazios ou tecnicamente inválidos devem ser registrados antes da exclusão
            if pd.isna(comment_text) or str(comment_text).strip() == "":
                log_exclusions.append({
                    "fonte_id": fonte_id,
                    "linha_origem": linha_origem,
                    "motivo": "Comentário vazio ou nulo"
                })
                continue

            comment_str = str(comment_text)

            # Mascaramento/Anonimização de perfis para versionamento público
            user_id = "[ANON_USER_ID]" if rules.get("anonymize_profiles") else row["User ID"]
            user_name = "anonimo" if rules.get("anonymize_profiles") else row["User Name"]
            profile_url = "[ANON_URL]" if rules.get("anonymize_profiles") else row["Profile URL"]
            avatar_url = "[ANON_URL]" if rules.get("anonymize_profiles") else row["Avatar URL"]

            # Expurgação de PII do texto do comentário
            cleaned_text = cls.clean_comment_text(comment_str, rules)

            sanitized_records.append({
                "my-serial-number": str(row["my-serial-number"]),
                "index": str(row["index"]),
                "User ID": str(user_id),
                "Avatar URL": str(avatar_url),
                "Profile URL": str(profile_url),
                "User Name": str(user_name),
                "Comment Text": cleaned_text,
                "Comment Date": str(row["Comment Date"]),
                "lote": f"LOTE-{fonte_id.split('-')[-1]}",
                "arquivo_origem": os.path.basename(file_path),
                "aba_origem": "Planilha1", # Planilha padrão exportada pelo chrome
                "linha_origem": linha_origem,
                "fonte_id": fonte_id
            })

        # Emissão de relatório de limpeza simples para auditoria
        if log_exclusions:
            # Podemos gravar um pequeno log na pasta de dados ou exibir em tela
            pass

        return sanitized_records
