import sys
import os
import argparse
import json
from .core import (
    DiscoveryService,
    EvidenceService,
    ExecutionService,
    ReasoningService,
    AuditService
)
from .context_packages import (
    MapaDaNoiteContextPackage,
    SaudeTerritorialContextPackage
)

def print_premium_header(title: str):
    print("=" * 80)
    print(f"  [ALCATEIA] {title.upper()}")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="ALCATEIA - Evidence-Oriented Multi-Agent Architecture (CLI Orquestrador MVP v1.0)"
    )
    parser.add_argument(
        "--context", 
        type=str, 
        required=True, 
        choices=["mapa_da_noite", "saude_territorial"],
        help="O pacote de contexto (Context Package) a ser carregado."
    )
    parser.add_argument(
        "--question", 
        type=str, 
        required=True, 
        help="A pergunta central ou problema a ser investigado pela ALCATEIA."
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Executa a análise cognitiva em tempo real via API do Gemini (requer GEMINI_API_KEY no ambiente)."
    )

    args = parser.parse_args()

    print_premium_header("ALCATEIA - Orquestrador de Inteligencia por Evidencias")
    print(f"[*] Executando fluxo linear de decisao...")

    # [PERGUNTA] Entrada do usuário
    print(f"\n[+] Pergunta de entrada: '{args.question}'")

    # 1. INVESTIGACAO (Discovery)
    print(f"\n[1/5] [INVESTIGACAO] Qualificando contexto para: '{args.context}'...")
    if args.context == "mapa_da_noite":
        context_pkg = MapaDaNoiteContextPackage()
    else:
        context_pkg = SaudeTerritorialContextPackage()

    print(f" | Nome do contexto: {context_pkg.name} (Versao: {context_pkg.version})")
    
    try:
        demanda = DiscoveryService.register_demand(context_pkg.package_id, args.question)
        print(f" | [OK] Demanda Qualificada: {demanda['demanda_id']} | Status: {demanda['status']}")
    except Exception as e:
        print(f" | [ERRO] Falha na investigacao inicial: {str(e)}")
        sys.exit(1)

    # 2. EXECUCAO (Execution)
    print(f"\n[2/5] [EXECUCAO] Executando saneamento deterministico e expurgos de privacidade...")
    sanitized_records = []
    
    # Obter mapeamento bruto para passar para a execucao
    sources_mapping = context_pkg.get_sources_mapping()
    
    try:
        print(f" | Processando e normalizando dados brutos em memoria (Linhagem ativa)...")
        for fonte_id, meta in sources_mapping.items():
            # Cria estrutura simplificada para o Execution Service trabalhar em memoria
            verified_src = {
                "fonte_id": fonte_id,
                "arquivo_path": meta["arquivo_path"]
            }
            records = ExecutionService.sanitize_source_data(verified_src, context_pkg)
            sanitized_records.extend(records)
        print(f" | [OK] Saneamento concluido. Total de {len(sanitized_records)} interacoes prontas.")
    except Exception as e:
        print(f" | [ERRO] Falha no processamento deterministico dos dados: {str(e)}")
        sys.exit(1)

    # 3. EVIDENCIAS (Evidence)
    print(f"\n[3/5] [EVIDENCIAS] Realizando auditoria de integridade fisica e criptografica (SHA-256)...")
    try:
        verified_sources = EvidenceService.verify_sources(context_pkg)
        print(f" | [OK] {len(verified_sources)} fontes de dados brutas validadas com hashes compativeis!")
        for src in verified_sources[:2]:
            print(f"   - {src['fonte_id']} -> {os.path.basename(src['arquivo_path'])} (SHA-256: {src['hash'][:10]}...)")
        if len(verified_sources) > 2:
            print(f"   - ... e mais {len(verified_sources) - 2} fontes auditadas com sucesso.")
    except Exception as e:
        print(f" | [ERRO] VIOLACAO DE INTEGRIDADE DETECTADA: {str(e)}")
        sys.exit(1)

    # 4. RECOMENDACAO (Reasoning)
    print(f"\n[4/5] [RECOMENDACAO] Iniciando analise cognitiva e processamento de recomendacao...")
    try:
        reasoning_report = ReasoningService.analyze_dataset(
            sanitized_records, 
            context_pkg, 
            args.question, 
            demo_mode=not args.live
        )
        print(f" | Eixo de vulnerabilidade identificado: '{reasoning_report['eixo_central']}'")
        print(f" | Hipotese formulada: {reasoning_report['hipotese_formulada']}")
        print(f" | Nivel de Incerteza do Julgamento: {reasoning_report['nivel_confianca'].upper()}")
        print(f" | Recomendacao sugerida: {reasoning_report['conclusao_recomendacao']}")
    except Exception as e:
        print(f" | [ERRO] Falha na formulacao de recomendacao: {str(e)}")
        sys.exit(1)

    # 5. AUDITORIA (Audit)
    print(f"\n[5/5] [AUDITORIA] Executando auditoria relacional cruzada e selando a MUE...")
    try:
        evidence_chain = AuditService.validate_and_seal_chain(
            demanda["demanda_id"], 
            reasoning_report, 
            verified_sources
        )
        print(f" | [OK] Cadeia de Evidencias validada e assinada com sucesso!")
        print(f" | ID da MUE: {evidence_chain['mue_id']}")
        print(f" | Assinatura digital da Cadeia (MUE): {evidence_chain['assinatura_mue']}")
    except Exception as e:
        print(f" | [ERRO] Falha critica de auditoria logica: {str(e)}")
        sys.exit(1)

    # Impressão Final do Resultado do Processo em Formato JSON de Alta Rastreabilidade
    print("\n" + "=" * 80)
    print("  [MUE] MATRIZ UNICA DE EVIDENCIA (MUE) GERADA COM RASTREABILIDADE TOTAL")
    print("=" * 80)
    print(json.dumps(evidence_chain, indent=2, ensure_ascii=True))
    print("=" * 80)
    print("  [ALCATEIA] EXECUCAO CONCLUIDA EM CONFORMIDADE COM A ARQUITETURA v1.0")
    print("=" * 80)

if __name__ == "__main__":
    main()
