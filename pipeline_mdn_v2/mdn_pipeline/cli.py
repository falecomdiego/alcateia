from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .classification import build_validation_sample, classify_lot
from .consolidation import consolidate
from .core import (
    DEFAULT_CONFIG,
    PipelineError,
    load_config,
    verify_run_manifest,
    verify_taxonomy,
)
from .ingest import ingest_lot
from .publication import build_public_candidate
from .treatment import clean_lot


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "validate-config":
            config, path = load_config(args.config)
            print(f"Configuração válida: {path}")
            for gate, value in config["gates"].items():
                print(f"{gate}: {'aprovado' if value else 'bloqueado'}")
            return 0
        if args.command == "verify-taxonomy":
            config, _ = load_config(args.config)
            print(f"Taxonomia íntegra: {verify_taxonomy(config)}")
            return 0
        if args.command == "verify-run":
            counts = verify_run_manifest(args.manifest.resolve())
            print(f"Manifesto íntegro: {args.manifest.resolve()}")
            print(f"Entradas verificadas: {counts['entradas_verificadas']}")
            print(f"Saídas verificadas: {counts['saidas_verificadas']}")
            return 0
        if args.command == "ingest-lot":
            output = ingest_lot(
                lot=args.lot,
                input_dir=args.input_dir,
                source_inventory=args.source_inventory,
                collection_log=args.collection_log,
                lot_manifest=args.lot_manifest,
                config_path=args.config,
                run_id=args.run_id,
            )
        elif args.command == "clean-lot":
            output = clean_lot(
                lot=args.lot,
                input_csv=args.input_csv,
                config_path=args.config,
                run_id=args.run_id,
            )
        elif args.command == "classify-lot":
            output = classify_lot(
                lot=args.lot,
                input_csv=args.input_csv,
                config_path=args.config,
                run_id=args.run_id,
            )
        elif args.command == "build-validation-sample":
            output = build_validation_sample(
                lot=args.lot,
                input_csv=args.input_csv,
                config_path=args.config,
                run_id=args.run_id,
            )
        elif args.command == "consolidate":
            output = consolidate(
                classification_files=args.classification,
                reviews_csv=args.reviews,
                adjudications_csv=args.adjudications,
                config_path=args.config,
                run_id=args.run_id,
            )
        elif args.command == "build-public":
            output = build_public_candidate(
                groups_csv=args.groups,
                evidence_csv=args.evidence,
                metrics_csv=args.metrics,
                authorization_csv=args.authorization,
                release_record_json=args.release_record,
                config_path=args.config,
                run_id=args.run_id,
            )
        else:
            parser.error("Comando desconhecido")
            return 2
        print(f"Saída criada: {output.resolve()}")
        print("Consulte manifesto_execucao.json para contagens, hashes e inconsistências.")
        return 0
    except PipelineError as exc:
        print(f"BLOQUEADO: {exc}", file=sys.stderr)
        return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mdn-pipeline-v2",
        description="Pipeline prospectivo, rastreável e bloqueado por gates do Mapa da Noite.",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate-config", help="Valida estrutura, caminhos, taxonomia e gates.")
    sub.add_parser("verify-taxonomy", help="Confere o hash da Taxonomia Mestre V1.1.")
    verify = sub.add_parser("verify-run", help="Recalcula hashes de um manifesto de execução.")
    verify.add_argument("--manifest", type=Path, required=True)

    ingest = sub.add_parser("ingest-lot", help="Ingere e pseudonimiza um lote autorizado.")
    _add_lot_and_run(ingest)
    ingest.add_argument("--input-dir", type=Path, required=True)
    ingest.add_argument("--source-inventory", type=Path, required=True)
    ingest.add_argument("--collection-log", type=Path, required=True)
    ingest.add_argument("--lot-manifest", type=Path, required=True)

    clean = sub.add_parser("clean-lot", help="Executa limpeza e triagem sem apagar registros.")
    _add_lot_and_run(clean)
    clean.add_argument("--input-csv", type=Path, required=True)

    classify = sub.add_parser("classify-lot", help="Gera sugestões taxonômicas e fila humana.")
    _add_lot_and_run(classify)
    classify.add_argument("--input-csv", type=Path, required=True)

    sample = sub.add_parser(
        "build-validation-sample",
        help="Cria amostra determinística e marca dupla revisão.",
    )
    _add_lot_and_run(sample)
    sample.add_argument("--input-csv", type=Path, required=True)

    consolidate_parser = sub.add_parser(
        "consolidate",
        help="Consolida lotes com tabelas relacionais e decisões humanas.",
    )
    consolidate_parser.add_argument("--classification", type=Path, action="append", required=True)
    consolidate_parser.add_argument("--reviews", type=Path)
    consolidate_parser.add_argument("--adjudications", type=Path)
    consolidate_parser.add_argument("--run-id")

    public = sub.add_parser(
        "build-public",
        help="Gera candidato público somente após todos os gates e aprovações.",
    )
    public.add_argument("--groups", type=Path, required=True)
    public.add_argument("--evidence", type=Path, required=True)
    public.add_argument("--metrics", type=Path, required=True)
    public.add_argument("--authorization", type=Path, required=True)
    public.add_argument("--release-record", type=Path, required=True)
    public.add_argument("--run-id")
    return parser


def _add_lot_and_run(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--lot", required=True)
    parser.add_argument("--run-id")


if __name__ == "__main__":
    raise SystemExit(main())

