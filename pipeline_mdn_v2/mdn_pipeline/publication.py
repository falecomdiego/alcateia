from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from .consolidation import EVIDENCE_COLUMNS, GROUP_COLUMNS
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
    write_text_new,
)


PUBLIC_COLUMNS = [
    "tema_publico_id",
    "frente_taxonomica",
    "volume_agregado",
    "tipo_resultado",
    "nota_de_leitura",
]
PROHIBITED_PATTERNS = [
    re.compile(r"https?://", re.IGNORECASE),
    re.compile(r"www\.", re.IGNORECASE),
    re.compile(r"@[A-Za-z0-9_.]+"),
    re.compile(r"MDN-AUTOR-", re.IGNORECASE),
    re.compile(r"\bUser ID\b", re.IGNORECASE),
    re.compile(r"\bProfile URL\b", re.IGNORECASE),
    re.compile(r"\bComment Text\b", re.IGNORECASE),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(r"\b[0-9a-f]{64}\b", re.IGNORECASE),
]


def build_public_candidate(
    *,
    groups_csv: Path,
    evidence_csv: Path,
    metrics_csv: Path,
    authorization_csv: Path,
    release_record_json: Path,
    config_path: str | Path | None = None,
    root: Path | None = None,
    run_id: str | None = None,
) -> Path:
    config, resolved_config = load_config(config_path, root)
    ensure_gate(config, "G4_publication")
    verify_taxonomy(config, root)
    base = (root or project_root()).resolve()
    lineage_root = resolve_project_path(config["paths"]["lineage"], base)
    public_root = resolve_project_path(config["paths"]["public_product"], base)
    groups_path = groups_csv.resolve()
    evidence_path = evidence_csv.resolve()
    if lineage_root not in groups_path.parents or lineage_root not in evidence_path.parents:
        raise PipelineError("Publicação só aceita consolidação produzida pelo pipeline V2")
    if groups_path.parent != evidence_path.parent:
        raise PipelineError("Grupos e evidências devem pertencer à mesma execução")

    metrics_path = metrics_csv.resolve()
    authorization_path = authorization_csv.resolve()
    release_path = release_record_json.resolve()
    for controlled_path in (metrics_path, authorization_path, release_path):
        if public_root not in controlled_path.parents:
            raise PipelineError(f"Controle de publicação fora da pasta da rodada: {controlled_path}")
    release = load_json(release_path)
    _validate_release_record(release, config)
    if release["source_execution_id"] != groups_path.parent.name:
        raise PipelineError("Registro de liberação não corresponde à execução consolidada")
    metrics = _load_metrics(metrics_path, float(config["validation"]["minimum_public_precision"]))
    authorizations = _load_authorizations(authorization_path)
    groups, group_fields = read_csv(groups_path)
    evidence, evidence_fields = read_csv(evidence_path)
    _require_fields(groups_path, group_fields, set(GROUP_COLUMNS))
    _require_fields(evidence_path, evidence_fields, set(EVIDENCE_COLUMNS))
    evidence_by_group = {row["grupo_id"]: row for row in evidence}
    if len(evidence_by_group) != len(evidence):
        raise PipelineError("Mais de uma afirmação de evidência por grupo")

    rules = load_json(Path(__file__).with_name("taxonomy_rules_v1_1.json"))
    labels = {front_id: front["label"] for front_id, front in rules["fronts"].items()}
    minimum_cell = int(config["public_safety"]["minimum_cell_size"])
    selected: list[dict[str, str]] = []
    decisions: list[str] = []
    for group in sorted(groups, key=lambda row: row["grupo_id"]):
        group_id = group["grupo_id"]
        authorization = authorizations.get(group_id)
        if not authorization or authorization["uso_publico_autorizado"] != "true":
            continue
        front = group["frente_taxonomica"]
        metric = metrics.get(front)
        if not metric or metric["approved"] is not True:
            raise PipelineError(f"Frente autorizada sem métrica pública aprovada: {front}")
        volume = int(group["volume_registros"])
        if volume < minimum_cell:
            raise PipelineError(
                f"Grupo autorizado abaixo do limiar público {minimum_cell}: {group_id}"
            )
        evidence_row = evidence_by_group.get(group_id)
        if not evidence_row or evidence_row.get("tipo_afirmacao") != "evidencia_observada":
            raise PipelineError(f"Grupo sem evidência observada correspondente: {group_id}")
        if front not in labels:
            raise PipelineError(f"Frente desconhecida: {front}")
        decisions.append(authorization["decisao_humana_id"])
        selected.append(
            {
                "tema_publico_id": f"MDN-TEMA-{len(selected) + 1:03d}",
                "frente_taxonomica": labels[front],
                "volume_agregado": str(volume),
                "tipo_resultado": "sinal_agregado_observado_no_corpus",
                "nota_de_leitura": (
                    "Contagem situada no conjunto coletado; não representa prevalência, "
                    "causalidade, culpa ou população."
                ),
            }
        )
    if not selected:
        raise PipelineError("Nenhum grupo possui autorização pública válida")
    _scan_public_rows(selected)

    current_run = run_id or new_run_id()
    output_dir = public_root / "saidas" / current_run
    ensure_new_directory(output_dir)
    public_path = output_dir / "temas_agregados_publicos.csv"
    note_path = output_dir / "nota_metodologica_publica.md"
    write_csv_new(public_path, PUBLIC_COLUMNS, selected)
    note = (
        "# Nota metodológica pública — MDN-RPP01\n\n"
        "Os resultados descrevem sinais agregados encontrados no corpus definido para a rodada. "
        "Não constituem amostra representativa, diagnóstico populacional, atribuição de causa, "
        "responsabilidade ou validação científica. Comentários literais e identificadores não "
        "integram este pacote.\n"
    )
    write_text_new(note_path, note)
    _scan_public_text(note)
    outputs = [public_path, note_path]
    manifest = build_run_manifest(
        run_id=current_run,
        stage="sanitizacao_e_pacote_publico",
        config_path=resolved_config,
        config=config,
        inputs=[groups_path, evidence_path, metrics_path, authorization_path, release_path],
        outputs=outputs,
        counts={"grupos_avaliados": len(groups), "temas_publicados": len(selected)},
        human_decisions=sorted(set(decisions + [str(release["decision_id"])])),
    )
    write_json_new(output_dir / "manifesto_execucao.json", manifest)
    return output_dir


def _validate_release_record(release: dict, config: dict) -> None:
    if release.get("round_id") != config["round_id"] or release.get("approved") is not True:
        raise PipelineError("Registro de liberação pública não aprovado")
    required = [
        "candidate_version",
        "approval_date",
        "round_owner",
        "sanitization_owner",
        "second_reviewer",
        "source_execution_id",
        "decision_id",
    ]
    missing = [field for field in required if not release.get(field)]
    if missing:
        raise PipelineError("Registro de liberação incompleto: " + ", ".join(missing))


def _load_metrics(path: Path, threshold: float) -> dict[str, dict[str, object]]:
    rows, fields = read_csv(path)
    required = {"frente_taxonomica", "precisao", "n_referencia", "aprovada_publicacao"}
    _require_fields(path, fields, required)
    output: dict[str, dict[str, object]] = {}
    for row in rows:
        front = row.get("frente_taxonomica", "").strip()
        if not front:
            continue
        try:
            precision = float(row.get("precisao", ""))
            reference_n = int(row.get("n_referencia", ""))
        except ValueError as exc:
            raise PipelineError(f"Métrica inválida para {front}") from exc
        approved = row.get("aprovada_publicacao") == "true"
        if approved and (precision < threshold or reference_n < 1):
            raise PipelineError(f"Métrica aprovada abaixo do critério para {front}")
        if front in output:
            raise PipelineError(f"Métrica duplicada para {front}")
        output[front] = {"precision": precision, "reference_n": reference_n, "approved": approved}
    return output


def _load_authorizations(path: Path) -> dict[str, dict[str, str]]:
    rows, fields = read_csv(path)
    required = {"grupo_id", "uso_publico_autorizado", "decisao_humana_id", "justificativa"}
    _require_fields(path, fields, required)
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        group_id = row.get("grupo_id", "").strip()
        if not group_id:
            continue
        if group_id in output:
            raise PipelineError(f"Autorização pública duplicada: {group_id}")
        if row.get("uso_publico_autorizado") == "true":
            if not row.get("decisao_humana_id", "").strip() or not row.get("justificativa", "").strip():
                raise PipelineError(f"Autorização pública incompleta: {group_id}")
        output[group_id] = row
    return output


def _scan_public_rows(rows: Sequence[dict[str, str]]) -> None:
    for row in rows:
        for value in row.values():
            _scan_public_text(value)


def _scan_public_text(value: str) -> None:
    for pattern in PROHIBITED_PATTERNS:
        if pattern.search(value):
            raise PipelineError(f"Conteúdo proibido detectado no pacote público: {pattern.pattern}")


def _require_fields(path: Path, fields: list[str], required: set[str]) -> None:
    missing = sorted(required - set(fields))
    if missing:
        raise PipelineError(f"{path} sem colunas: {missing}")
