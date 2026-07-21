from __future__ import annotations

import hashlib
import math
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Mapping

from .core import (
    PipelineError,
    build_run_manifest,
    ensure_gate,
    ensure_new_directory,
    load_config,
    load_json,
    new_run_id,
    normalize_text,
    project_root,
    read_csv,
    resolve_project_path,
    term_present,
    validate_lot,
    verify_taxonomy,
    write_csv_new,
    write_json_new,
)
from .ingest import WORK_COLUMNS


CLASSIFICATION_COLUMNS = [
    *WORK_COLUMNS,
    "frente_taxonomica",
    "frentes_candidatas",
    "termos_detectados",
    "quantidade_termos",
    "marcadores_sensiveis",
    "status_classificacao",
    "requer_validacao_humana",
    "justificativa_vinculo",
    "decisao_humana_id",
]


def classify_lot(
    *,
    lot: str,
    input_csv: Path,
    config_path: str | Path | None = None,
    root: Path | None = None,
    run_id: str | None = None,
) -> Path:
    config, resolved_config = load_config(config_path, root)
    ensure_gate(config, "G2_analysis")
    verify_taxonomy(config, root)
    validate_lot(config, lot)
    base = (root or project_root()).resolve()
    processing_root = resolve_project_path(config["paths"]["processing"], base)
    allowed_root = (processing_root / "lotes" / lot / "04_limpeza_e_logs").resolve()
    input_path = input_csv.resolve()
    if allowed_root not in input_path.parents or input_path.name != "registros_tratados.csv":
        raise PipelineError(f"Classificação só aceita registros_tratados.csv de {lot}")

    rows, fields = read_csv(input_path)
    missing = [field for field in WORK_COLUMNS if field not in fields]
    if missing:
        raise PipelineError(f"Base tratada sem colunas: {missing}")
    _validate_rows(rows, lot)
    rules_path = Path(__file__).with_name("taxonomy_rules_v1_1.json")
    rules = load_json(rules_path)
    if rules.get("taxonomy_version") != config["taxonomy"]["version"]:
        raise PipelineError("Regras de triagem não correspondem à taxonomia congelada")

    classified = [_classify_row(row, rules) for row in rows]
    queue = [row for row in classified if row["requer_validacao_humana"] == "true"]
    counts = {
        "entrada": len(classified),
        "mantidos": sum(row["status_tratamento"] == "mantido" for row in classified),
        "sugeridos": sum(row["status_classificacao"] == "sugerida" for row in classified),
        "nao_determinado": sum(row["status_classificacao"] == "nao_determinado" for row in classified),
        "nao_aplicavel": sum(row["status_classificacao"] == "nao_aplicavel" for row in classified),
        "fila_validacao_obrigatoria": len(queue),
        "exclusoes": 0,
    }

    current_run = run_id or new_run_id()
    output_dir = processing_root / "lotes" / lot / "05_classificacao_taxonomica" / current_run
    ensure_new_directory(output_dir)
    classified_path = output_dir / "classificacao_taxonomica.csv"
    queue_path = output_dir / "fila_validacao_obrigatoria.csv"
    write_csv_new(classified_path, CLASSIFICATION_COLUMNS, classified)
    write_csv_new(queue_path, CLASSIFICATION_COLUMNS, queue)
    outputs = [classified_path, queue_path]
    manifest = build_run_manifest(
        run_id=current_run,
        stage="classificacao_taxonomica_de_triagem",
        config_path=resolved_config,
        config=config,
        inputs=[input_path, rules_path],
        outputs=outputs,
        counts=counts,
        inconsistencies=[
            "Regras lexicais produzem sugestões; não constituem validação humana nem interpretação contextual."
        ],
    )
    write_json_new(output_dir / "manifesto_execucao.json", manifest)
    return output_dir


def build_validation_sample(
    *,
    lot: str,
    input_csv: Path,
    config_path: str | Path | None = None,
    root: Path | None = None,
    run_id: str | None = None,
) -> Path:
    config, resolved_config = load_config(config_path, root)
    ensure_gate(config, "G2_analysis")
    verify_taxonomy(config, root)
    validate_lot(config, lot)
    base = (root or project_root()).resolve()
    processing_root = resolve_project_path(config["paths"]["processing"], base)
    allowed_root = (processing_root / "lotes" / lot / "05_classificacao_taxonomica").resolve()
    input_path = input_csv.resolve()
    if allowed_root not in input_path.parents or input_path.name != "classificacao_taxonomica.csv":
        raise PipelineError(f"Amostra só aceita classificação oficial de triagem de {lot}")
    rows, fields = read_csv(input_path)
    missing = [field for field in CLASSIFICATION_COLUMNS if field not in fields]
    if missing:
        raise PipelineError(f"Classificação sem colunas: {missing}")
    eligible = [row for row in rows if row.get("status_tratamento") == "mantido"]
    n = len(eligible)
    minimum = int(config["validation"]["minimum_sample"])
    rate = float(config["validation"]["sample_rate"])
    target = min(n, max(minimum, math.ceil(rate * n))) if n else 0
    mandatory = [row for row in eligible if row.get("requer_validacao_humana") == "true"]
    mandatory_ids = {row["registro_id"] for row in mandatory}
    remaining = [row for row in eligible if row["registro_id"] not in mandatory_ids]
    additional = _stratified_deterministic_sample(
        remaining,
        max(0, target - len(mandatory)),
        config["round_id"],
    )
    selected = [*mandatory, *additional]
    selected.sort(key=lambda row: _stable_key(row["registro_id"], config["round_id"]))
    double_count = math.ceil(float(config["validation"]["double_review_rate"]) * len(selected))
    double_ids = {row["registro_id"] for row in selected[:double_count]}
    sample_rows = []
    for row in selected:
        sample_rows.append(
            {
                **row,
                "amostra_motivo": (
                    "revisao_integral_obrigatoria"
                    if row["registro_id"] in mandatory_ids
                    else "amostra_geral_estratificada"
                ),
                "dupla_revisao_obrigatoria": (
                    "true" if row["registro_id"] in double_ids else "false"
                ),
            }
        )

    current_run = run_id or new_run_id()
    output_dir = processing_root / "lotes" / lot / "06_fila_validacao_humana" / current_run
    ensure_new_directory(output_dir)
    sample_path = output_dir / "amostra_validacao.csv"
    write_csv_new(
        sample_path,
        [*CLASSIFICATION_COLUMNS, "amostra_motivo", "dupla_revisao_obrigatoria"],
        sample_rows,
    )
    manifest = build_run_manifest(
        run_id=current_run,
        stage="amostragem_validacao_humana",
        config_path=resolved_config,
        config=config,
        inputs=[input_path],
        outputs=[sample_path],
        counts={
            "elegiveis": n,
            "alvo_formula": target,
            "revisao_integral": len(mandatory),
            "amostra_total": len(sample_rows),
            "dupla_revisao": len(double_ids),
        },
    )
    write_json_new(output_dir / "manifesto_execucao.json", manifest)
    return output_dir


def _classify_row(row: Mapping[str, str], rules: Mapping[str, Any]) -> dict[str, str]:
    output = dict(row)
    if row.get("status_tratamento") != "mantido":
        output.update(
            {
                "frente_taxonomica": "nao_determinado",
                "frentes_candidatas": "",
                "termos_detectados": "",
                "quantidade_termos": "0",
                "marcadores_sensiveis": "",
                "status_classificacao": "nao_aplicavel",
                "requer_validacao_humana": "false",
                "justificativa_vinculo": "Registro fora da classificação textual.",
                "decisao_humana_id": "",
            }
        )
        return output

    text = normalize_text(row.get("comentario_trabalho", ""))
    candidates: dict[str, list[str]] = {}
    for front_id, front in rules["fronts"].items():
        terms = sorted({term for term in front["terms"] if term_present(text, term)})
        if terms:
            candidates[front_id] = terms
    markers: list[str] = []
    for marker_type, terms in rules["human_review_markers"].items():
        if any(term_present(text, term) for term in terms):
            markers.append(marker_type)

    candidate_ids = sorted(candidates)
    all_terms = sorted({term for values in candidates.values() for term in values})
    always_human = set(rules["fronts_always_human_review"])
    human_required = bool(markers or always_human.intersection(candidate_ids) or len(candidate_ids) > 1)
    if len(candidate_ids) == 1:
        front = candidate_ids[0]
        status = "sugerida"
        justification = "Sugestão lexical baseada nos termos recuperáveis: " + "; ".join(all_terms)
    else:
        front = "nao_determinado"
        status = "nao_determinado"
        if not candidate_ids:
            justification = "Nenhum termo das regras de triagem foi encontrado; não houve enquadramento forçado."
        else:
            justification = "Mais de uma frente candidata; decisão contextual reservada à validação humana."
            human_required = True
    output.update(
        {
            "frente_taxonomica": front,
            "frentes_candidatas": ";".join(candidate_ids),
            "termos_detectados": ";".join(all_terms),
            "quantidade_termos": str(len(all_terms)),
            "marcadores_sensiveis": ";".join(sorted(markers)),
            "status_classificacao": status,
            "requer_validacao_humana": "true" if human_required else "false",
            "justificativa_vinculo": justification,
            "decisao_humana_id": "",
        }
    )
    return output


def _validate_rows(rows: list[dict[str, str]], lot: str) -> None:
    seen: set[str] = set()
    for row in rows:
        if row.get("lote") != lot:
            raise PipelineError("Classificação recebeu mais de um lote")
        record = row.get("registro_id", "")
        if not record or record in seen:
            raise PipelineError(f"registro_id ausente ou duplicado: {record}")
        seen.add(record)


def _stable_key(record_id: str, seed: str) -> str:
    return hashlib.sha256(f"{seed}|{record_id}".encode("utf-8")).hexdigest()


def _stratified_deterministic_sample(
    rows: list[dict[str, str]],
    limit: int,
    seed: str,
) -> list[dict[str, str]]:
    if limit <= 0:
        return []
    strata: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row.get("fonte_id", ""),
            row.get("frente_taxonomica", ""),
            row.get("status_classificacao", ""),
        )
        strata[key].append(row)
    queues: deque[deque[dict[str, str]]] = deque()
    for key in sorted(strata):
        ordered = sorted(strata[key], key=lambda row: _stable_key(row["registro_id"], seed))
        queues.append(deque(ordered))
    selected: list[dict[str, str]] = []
    while queues and len(selected) < limit:
        queue = queues.popleft()
        selected.append(queue.popleft())
        if queue:
            queues.append(queue)
    return selected

