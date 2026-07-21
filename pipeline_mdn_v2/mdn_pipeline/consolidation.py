from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from .classification import CLASSIFICATION_COLUMNS
from .core import (
    PipelineError,
    build_run_manifest,
    ensure_gate,
    ensure_new_directory,
    load_config,
    load_json,
    new_run_id,
    project_root,
    read_csv,
    resolve_project_path,
    verify_taxonomy,
    write_csv_new,
    write_json_new,
)


RECORD_COLUMNS = [
    "registro_id",
    "lote",
    "fonte_id",
    "arquivo_origem",
    "autor_pseudo_id",
    "comentario_trabalho",
    "status_tratamento",
    "frente_sugerida",
    "frente_final",
    "status_decisao",
    "decisao_humana_id",
    "versao_taxonomia",
]
GROUP_COLUMNS = [
    "grupo_id",
    "frente_taxonomica",
    "criterio_agrupamento",
    "volume_registros",
    "registros_com_decisao_humana",
    "registros_sem_decisao_humana",
    "status_validacao",
]
LINK_COLUMNS = ["grupo_id", "registro_id"]
RECORD_DECISION_COLUMNS = ["registro_id", "decisao_id", "tipo", "decisao_final"]
EVIDENCE_COLUMNS = [
    "afirmacao_id",
    "tipo_afirmacao",
    "texto_interno",
    "grupo_id",
    "metodo_calculo",
    "volume",
    "limitacao",
    "versao_taxonomia",
    "responsavel",
    "status_aprovacao",
    "decisao_humana_id",
    "uso_publico_autorizado",
]


def consolidate(
    *,
    classification_files: Sequence[Path],
    reviews_csv: Path | None = None,
    adjudications_csv: Path | None = None,
    config_path: str | Path | None = None,
    root: Path | None = None,
    run_id: str | None = None,
) -> Path:
    config, resolved_config = load_config(config_path, root)
    ensure_gate(config, "G3_consolidation")
    verify_taxonomy(config, root)
    base = (root or project_root()).resolve()
    processing_root = resolve_project_path(config["paths"]["processing"], base)
    validation_root = resolve_project_path(config["paths"]["validation"], base)
    if not classification_files:
        raise PipelineError("Consolidação exige ao menos um lote")

    all_rows: list[dict[str, str]] = []
    input_lots: set[str] = set()
    seen_records: set[str] = set()
    inputs: list[Path] = []
    for raw_path in classification_files:
        path = raw_path.resolve()
        if processing_root not in path.parents or path.name != "classificacao_taxonomica.csv":
            raise PipelineError(f"Entrada de consolidação fora do pipeline V2: {path}")
        rows, fields = read_csv(path)
        missing = [field for field in CLASSIFICATION_COLUMNS if field not in fields]
        if missing:
            raise PipelineError(f"Classificação sem colunas em {path}: {missing}")
        lots = {row.get("lote", "") for row in rows}
        if len(lots) != 1:
            raise PipelineError(f"Arquivo deve conter exatamente um lote: {path}")
        lot = next(iter(lots))
        if lot in input_lots:
            raise PipelineError(f"Mais de uma classificação fornecida para {lot}")
        input_lots.add(lot)
        for row in rows:
            record = row.get("registro_id", "")
            if not record or record in seen_records:
                raise PipelineError(f"registro_id ausente ou duplicado: {record}")
            seen_records.add(record)
            all_rows.append(row)
        inputs.append(path)

    expected_lots = set(config.get("lots", []))
    if input_lots != expected_lots:
        raise PipelineError(
            f"Consolidação deve abranger todos os lotes configurados. esperado={sorted(expected_lots)} "
            f"recebido={sorted(input_lots)}"
        )

    rules = load_json(Path(__file__).with_name("taxonomy_rules_v1_1.json"))
    valid_fronts = set(rules["fronts"])
    reviews: dict[str, list[dict[str, str]]] = {}
    adjudications: dict[str, dict[str, str]] = {}
    if reviews_csv:
        review_path = reviews_csv.resolve()
        if validation_root not in review_path.parents:
            raise PipelineError("Revisões devem permanecer na pasta de validação da rodada")
        reviews = _load_reviews(review_path, valid_fronts)
        inputs.append(review_path)
    if adjudications_csv:
        adjudication_path = adjudications_csv.resolve()
        if validation_root not in adjudication_path.parents:
            raise PipelineError("Adjudicações devem permanecer na pasta de validação da rodada")
        adjudications = _load_adjudications(adjudication_path, valid_fronts)
        inputs.append(adjudication_path)

    records: list[dict[str, str]] = []
    decisions_used: set[str] = set()
    record_decisions: list[dict[str, str]] = []
    for row in all_rows:
        record_id = row["registro_id"]
        record_reviews = reviews.get(record_id, [])
        record_adjudication = adjudications.get(record_id)
        decision = _resolve_decision(record_id, record_reviews, record_adjudication)
        for review in record_reviews:
            record_decisions.append(
                {
                    "registro_id": record_id,
                    "decisao_id": review["decision_id"],
                    "tipo": "revisao",
                    "decisao_final": "true" if decision and review["decision_id"] == decision["decision_id"] else "false",
                }
            )
            decisions_used.add(review["decision_id"])
        if record_adjudication:
            record_decisions.append(
                {
                    "registro_id": record_id,
                    "decisao_id": record_adjudication["decision_id"],
                    "tipo": "adjudicacao",
                    "decisao_final": "true",
                }
            )
            decisions_used.add(record_adjudication["decision_id"])
        if row.get("status_tratamento") != "mantido":
            final_front = "nao_determinado"
            status = "nao_aplicavel"
            decision_id = ""
        elif decision:
            decision_id = decision["decision_id"]
            decisions_used.add(decision_id)
            if decision["decision"] in {"validada", "ajustada"}:
                final_front = decision["front"]
                status = "validada_humana"
            else:
                final_front = "nao_determinado"
                status = "rejeitada_ou_nao_determinada_humana"
        else:
            if row.get("requer_validacao_humana") == "true":
                raise PipelineError(f"Caso obrigatório sem decisão humana: {record_id}")
            final_front = row.get("frente_taxonomica", "nao_determinado")
            status = (
                "sugerida_nao_validada"
                if final_front != "nao_determinado"
                else "nao_determinado"
            )
            decision_id = ""
        records.append(
            {
                "registro_id": record_id,
                "lote": row.get("lote", ""),
                "fonte_id": row.get("fonte_id", ""),
                "arquivo_origem": row.get("arquivo_origem", ""),
                "autor_pseudo_id": row.get("autor_pseudo_id", ""),
                "comentario_trabalho": row.get("comentario_trabalho", ""),
                "status_tratamento": row.get("status_tratamento", ""),
                "frente_sugerida": row.get("frente_taxonomica", ""),
                "frente_final": final_front,
                "status_decisao": status,
                "decisao_humana_id": decision_id,
                "versao_taxonomia": row.get("versao_taxonomia", ""),
            }
        )

    groups, links, evidence = _build_groups(records, config["taxonomy"]["version"])
    _verify_lineage(records, groups, links)
    status_counts = Counter(row["status_tratamento"] for row in records)
    decision_counts = Counter(row["status_decisao"] for row in records)
    reconciliation = [
        {
            "etapa": "consolidacao_relacional",
            "entrada_total": len(records),
            "mantidos": status_counts.get("mantido", 0),
            "excluidos_tecnicos": status_counts.get("excluido_tecnico", 0),
            "fora_classificacao_textual": status_counts.get("fora_classificacao_textual", 0),
            "nao_determinado": sum(
                row["frente_final"] == "nao_determinado" for row in records
            ),
            "registros_agrupados": len(links),
            "grupos": len(groups),
            "diferenca": 0,
            "status": "conciliado",
        }
    ]

    current_run = run_id or new_run_id()
    lineage_root = resolve_project_path(config["paths"]["lineage"], base)
    output_dir = lineage_root / "saidas" / current_run
    ensure_new_directory(output_dir)
    records_path = output_dir / "registros.csv"
    groups_path = output_dir / "grupos.csv"
    links_path = output_dir / "grupo_registro.csv"
    record_decisions_path = output_dir / "registro_decisao.csv"
    evidence_path = output_dir / "evidencias.csv"
    reconciliation_path = output_dir / "reconciliacao.csv"
    write_csv_new(records_path, RECORD_COLUMNS, records)
    write_csv_new(groups_path, GROUP_COLUMNS, groups)
    write_csv_new(links_path, LINK_COLUMNS, links)
    write_csv_new(record_decisions_path, RECORD_DECISION_COLUMNS, record_decisions)
    write_csv_new(evidence_path, EVIDENCE_COLUMNS, evidence)
    write_csv_new(reconciliation_path, list(reconciliation[0]), reconciliation)
    outputs = [
        records_path,
        groups_path,
        links_path,
        record_decisions_path,
        evidence_path,
        reconciliation_path,
    ]
    manifest = build_run_manifest(
        run_id=current_run,
        stage="consolidacao_relacional",
        config_path=resolved_config,
        config=config,
        inputs=inputs,
        outputs=outputs,
        counts={
            "registros": len(records),
            "registros_agrupados": len(links),
            "grupos": len(groups),
            "decisoes_humanas": len(decisions_used),
            "nao_determinado": decision_counts.get("nao_determinado", 0)
            + decision_counts.get("rejeitada_ou_nao_determinada_humana", 0),
        },
        human_decisions=sorted(decisions_used),
    )
    write_json_new(output_dir / "manifesto_execucao.json", manifest)
    return output_dir


def _load_reviews(path: Path, valid_fronts: set[str]) -> dict[str, list[dict[str, str]]]:
    rows, fields = read_csv(path)
    required = {
        "decisao_humana_id",
        "registro_id",
        "revisor_id",
        "decisao",
        "frente_validada",
        "justificativa",
    }
    _require_fields(path, fields, required)
    output: dict[str, list[dict[str, str]]] = defaultdict(list)
    seen_ids: set[str] = set()
    allowed = {"validada", "ajustada", "rejeitada", "nao_determinado"}
    for row in rows:
        decision_id = row.get("decisao_humana_id", "").strip()
        record_id = row.get("registro_id", "").strip()
        decision = row.get("decisao", "").strip()
        if not decision_id or decision_id in seen_ids:
            raise PipelineError(f"decisao_humana_id ausente ou duplicado: {decision_id}")
        seen_ids.add(decision_id)
        if not record_id or not row.get("revisor_id", "").strip() or not row.get("justificativa", "").strip():
            raise PipelineError(f"Revisão incompleta: {decision_id}")
        if decision not in allowed:
            raise PipelineError(f"Decisão humana inválida: {decision}")
        front = row.get("frente_validada", "").strip()
        if decision in {"validada", "ajustada"} and front not in valid_fronts:
            raise PipelineError(f"Frente validada inválida em {decision_id}: {front}")
        output[record_id].append(
            {"decision_id": decision_id, "decision": decision, "front": front}
        )
    return dict(output)


def _load_adjudications(path: Path, valid_fronts: set[str]) -> dict[str, dict[str, str]]:
    rows, fields = read_csv(path)
    required = {
        "adjudicacao_id",
        "registro_id",
        "decisao_final",
        "frente_final",
        "justificativa",
        "adjudicador_id",
    }
    _require_fields(path, fields, required)
    output: dict[str, dict[str, str]] = {}
    allowed = {"validada", "ajustada", "rejeitada", "nao_determinado"}
    for row in rows:
        record_id = row.get("registro_id", "").strip()
        adjudication_id = row.get("adjudicacao_id", "").strip()
        decision = row.get("decisao_final", "").strip()
        front = row.get("frente_final", "").strip()
        if not record_id or record_id in output or not adjudication_id:
            raise PipelineError(f"Adjudicação ausente ou duplicada para {record_id}")
        if decision not in allowed:
            raise PipelineError(f"Decisão de adjudicação inválida: {decision}")
        if decision in {"validada", "ajustada"} and front not in valid_fronts:
            raise PipelineError(f"Frente de adjudicação inválida: {front}")
        if not row.get("justificativa", "").strip() or not row.get("adjudicador_id", "").strip():
            raise PipelineError(f"Adjudicação incompleta: {adjudication_id}")
        output[record_id] = {
            "decision_id": adjudication_id,
            "decision": decision,
            "front": front,
        }
    return output


def _resolve_decision(
    record_id: str,
    reviews: list[dict[str, str]],
    adjudication: dict[str, str] | None,
) -> dict[str, str] | None:
    if not reviews:
        if adjudication:
            raise PipelineError(f"Adjudicação sem revisões para {record_id}")
        return None
    signatures = {(item["decision"], item["front"]) for item in reviews}
    if len(signatures) == 1:
        if adjudication:
            return adjudication
        return reviews[0]
    if not adjudication:
        raise PipelineError(f"Revisões divergentes sem adjudicação: {record_id}")
    return adjudication


def _build_groups(
    records: list[dict[str, str]],
    taxonomy_version: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    by_front: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in records:
        if row["status_tratamento"] == "mantido" and row["frente_final"] != "nao_determinado":
            by_front[row["frente_final"]].append(row)
    groups: list[dict[str, str]] = []
    links: list[dict[str, str]] = []
    evidence: list[dict[str, str]] = []
    for index, front in enumerate(sorted(by_front), start=1):
        group_id = f"MDN-RPP01-GRP-{index:04d}"
        rows = sorted(by_front[front], key=lambda row: row["registro_id"])
        human_count = sum(bool(row["decisao_humana_id"]) for row in rows)
        groups.append(
            {
                "grupo_id": group_id,
                "frente_taxonomica": front,
                "criterio_agrupamento": "frente_taxonomica_final",
                "volume_registros": str(len(rows)),
                "registros_com_decisao_humana": str(human_count),
                "registros_sem_decisao_humana": str(len(rows) - human_count),
                "status_validacao": (
                    "validacao_humana_integral" if human_count == len(rows) else "evidencia_interna"
                ),
            }
        )
        for row in rows:
            links.append({"grupo_id": group_id, "registro_id": row["registro_id"]})
        evidence.append(
            {
                "afirmacao_id": f"MDN-RPP01-AFI-{index:04d}",
                "tipo_afirmacao": "evidencia_observada",
                "texto_interno": (
                    f"Foram agrupados {len(rows)} registros do corpus na frente {front}."
                ),
                "grupo_id": group_id,
                "metodo_calculo": "contagem de vínculos únicos em grupo_registro",
                "volume": str(len(rows)),
                "limitacao": "Sinal situado no corpus; não representa prevalência, causalidade ou população.",
                "versao_taxonomia": taxonomy_version,
                "responsavel": "a_confirmar",
                "status_aprovacao": "interno_nao_publicado",
                "decisao_humana_id": "",
                "uso_publico_autorizado": "false",
            }
        )
    return groups, links, evidence


def _verify_lineage(
    records: list[dict[str, str]],
    groups: list[dict[str, str]],
    links: list[dict[str, str]],
) -> None:
    record_ids = {row["registro_id"] for row in records}
    group_ids = {row["grupo_id"] for row in groups}
    seen_links: set[tuple[str, str]] = set()
    counts = Counter()
    for link in links:
        key = (link["grupo_id"], link["registro_id"])
        if key in seen_links:
            raise PipelineError(f"Vínculo duplicado: {key}")
        seen_links.add(key)
        if link["grupo_id"] not in group_ids or link["registro_id"] not in record_ids:
            raise PipelineError(f"Vínculo órfão: {key}")
        counts[link["grupo_id"]] += 1
    for group in groups:
        if counts[group["grupo_id"]] != int(group["volume_registros"]):
            raise PipelineError(f"Volume divergente no grupo {group['grupo_id']}")


def _require_fields(path: Path, fields: list[str], required: set[str]) -> None:
    missing = sorted(required - set(fields))
    if missing:
        raise PipelineError(f"{path} sem colunas: {missing}")
