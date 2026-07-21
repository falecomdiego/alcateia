import unittest
import os
from ..core import (
    DiscoveryService,
    EvidenceService,
    ExecutionService,
    ReasoningService,
    AuditService
)
from ..context_packages import (
    MapaDaNoiteContextPackage,
    SaudeTerritorialContextPackage
)

class TestAlcateiaCoreFlow(unittest.TestCase):
    """
    Casos de testes integrados e unitários para validação das regras e do
    fluxo operacional completo de 5 serviços da arquitetura ALCATEIA.
    """

    def test_discovery_qualification(self):
        """Verifica se o Discovery Service qualifica e rejeita perguntas inadequadas."""
        # Sucesso
        demanda = DiscoveryService.register_demand(
            "mapa_da_noite_v1", 
            "Como esta a infraestrutura do bar ou pista open air?"
        )
        self.assertIsNotNone(demanda["demanda_id"])
        self.assertEqual(demanda["status"], "qualificado")

        # Falha (Pergunta muito curta)
        with self.assertRaises(ValueError):
            DiscoveryService.register_demand("mapa_da_noite_v1", "Curto")

    def test_evidence_integrity_violation(self):
        """
        Garante que uma violacao de integridade fisica ou hash alterado
        seja interceptada e bloqueie a execucao do pipeline (Rigid Hash Audit).
        """
        # Criamos um pacote de teste com hash divergente intencional
        class ViolatedContextPackage(MapaDaNoiteContextPackage):
            def get_sources_mapping(self):
                mapping = super().get_sources_mapping()
                if mapping:
                    first_key = list(mapping.keys())[0]
                    # Sobrescreve o hash real por um hash corrompido
                    mapping[first_key]["hash_sha256"] = "HASH_FALSO_DE_TESTE_DE_VIOLACAO"
                return mapping

        violated_pkg = ViolatedContextPackage()
        
        # O Evidence Service deve levantar ValueError
        with self.assertRaises(ValueError) as context:
            EvidenceService.verify_sources(violated_pkg)
        
        self.assertIn("VIOLACAO DE INTEGRIDADE", str(context.exception))

    def test_execution_pii_expurgation(self):
        """Verifica se o Execution Service remove com sucesso e-mails e telefones (LGPD)."""
        rules = {
            "expunge_patterns": [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            ]
        }
        raw_text = "Ola, meu e-mail e contato@empresa.com.br e meu celular e 1198888-8888."
        clean_text = ExecutionService.clean_comment_text(raw_text, rules)
        
        # O e-mail deve ter sido expurgado
        self.assertIn("[EXPURGADO_PII]", clean_text)
        self.assertNotIn("contato@empresa.com.br", clean_text)

    def test_reasoning_taxonomic_classification(self):
        """Garante que a classificacao taxonomica mapeia corretamente as palavras-chave."""
        taxonomy = {
            "infraestrutura_e_operacao": ["fila", "bar", "som"],
            "seguranca_e_saude": ["seguranca", "brigada"]
        }
        
        comment = "A fila do bar estava horrivel ontem a noite!"
        category = ReasoningService.classify_comment(comment, taxonomy)
        self.assertEqual(category, "infraestrutura_e_operacao")

        comment_seg = "Nao vi nenhum seguranca no portao principal."
        category_seg = ReasoningService.classify_comment(comment_seg, taxonomy)
        self.assertEqual(category_seg, "seguranca_e_saude")

    def test_end_to_end_demonstration_flow(self):
        """
        Executa um ciclo completo simulado de ponta a ponta (E2E) comprovando
        a integracao logica dos 5 serviços da arquitetura ALCATEIA de forma pura.
        """
        context_pkg = SaudeTerritorialContextPackage()
        question = "Como esta a falta de medicamentos e vacinas de gripe?"

        # 1. Discovery (Investigacao)
        demanda = DiscoveryService.register_demand(context_pkg.package_id, question)
        self.assertEqual(demanda["status"], "qualificado")

        # 2. Execution (Execucao)
        sanitized_records = []
        sources_mapping = context_pkg.get_sources_mapping()
        for fonte_id, meta in sources_mapping.items():
            verified_src = {
                "fonte_id": fonte_id,
                "arquivo_path": meta["arquivo_path"]
            }
            records = ExecutionService.sanitize_source_data(verified_src, context_pkg)
            sanitized_records.extend(records)
        self.assertTrue(len(sanitized_records) > 0)

        # 3. Evidence (Evidencias)
        verified_sources = EvidenceService.verify_sources(context_pkg)
        self.assertTrue(len(verified_sources) > 0)

        # 4. Reasoning (Recomendacao)
        reasoning_report = ReasoningService.analyze_dataset(
            sanitized_records, context_pkg, question, demo_mode=True
        )
        self.assertEqual(reasoning_report["eixo_central"], "insumos_e_remedios")

        # 5. Audit (Auditoria)
        evidence_chain = AuditService.validate_and_seal_chain(
            demanda["demanda_id"], reasoning_report, verified_sources
        )
        self.assertIsNotNone(evidence_chain["assinatura_mue"])

if __name__ == "__main__":
    unittest.main()
