from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any

from .core import (
    PipelineError,
    build_run_manifest,
    ensure_gate,
    ensure_new_directory,
    load_config,
    new_run_id,
    normalize_text,
    project_root,
    read_csv,
    resolve_project_path,
    validate_lot,
    verify_taxonomy,
    write_csv_new,
    write_json_new,
)
from .ingest import WORK_COLUMNS


TREATMENT_LOG_COLUMNS = [
    "registro_id",
    "lote",
    "fonte_id",
    "arquivo_origem",
    "status_tratamento",
    "motivo_tratamento",
]

SYSTEM_NOISE = {
    "null",
    "none",
    "nan",
    "n/a",
    "na",
    "undefined",
    "nao informado",
    "sem comentario",
    "comentario removido",
    "comment deleted",
    "deleted comment",
    "[deleted]",
    "[removed]",
}
URL_ONLY_RE = re.compile(r"^(?:https?://|www\.)\S+$", re.IGNORECASE)


def clean_lot(
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
    allowed_root = (processing_root / "lotes" / lot / "02_ingestao").resolve()
    input_path = input_csv.resolve()
    if allowed_root not in input_path.parents:
        raise PipelineError(f"Limpeza só aceita saída de ingestão de {lot}: {allowed_root}")

    rows, fields = read_csv(input_path)
    missing = [field for field in WORK_COLUMNS if field not in fields]
    if missing:
        raise PipelineError(f"Base de trabalho sem colunas: {missing}")
    if not rows:
        raise PipelineError("Base de trabalho vazia")
    _validate_rows(rows, lot)

    seen_duplicates: set[tuple[str, str, str]] = set()
    treated: list[dict[str, str]] = []
    log_rows: list[dict[str, str]] = []
    counts = {
        "entrada": len(rows),
        "mantidos": 0,
        "excluidos_tecnicos": 0,
        "fora_classificacao_textual": 0,
    }

    for original in rows:
        row = dict(original)
        text = row.get("comentario_trabalho", "")
        status, reason = _technical_status(text)
        if status == "mantido":
            duplicate_key = (
                row.get("arquivo_origem", ""),
                row.get("autor_pseudo_id", ""),
                normalize_text(text),
            )
            if duplicate_key in seen_duplicates:
                status = "excluido_tecnico"
                reason = "duplicidade_exata_mesmo_arquivo_autor_pseudonimo_texto"
            else:
                seen_duplicates.add(duplicate_key)
        row["status_tratamento"] = status
        row["motivo_tratamento"] = reason
        treated.append(row)
        counts[_count_key(status)] += 1
        if status != "mantido":
            log_rows.append({field: row.get(field, "") for field in TREATMENT_LOG_COLUMNS})

    if counts["entrada"] != (
        counts["mantidos"]
        + counts["excluidos_tecnicos"]
        + counts["fora_classificacao_textual"]
    ):
        raise PipelineError("Balanço de tratamento não fecha")

    current_run = run_id or new_run_id()
    output_dir = processing_root / "lotes" / lot / "04_limpeza_e_logs" / current_run
    ensure_new_directory(output_dir)
    treated_path = output_dir / "registros_tratados.csv"
    classifiable_path = output_dir / "base_classificavel.csv"
    log_path = output_dir / "log_tratamento.csv"
    reconciliation_path = output_dir / "reconciliacao_tratamento.csv"
    write_csv_new(treated_path, WORK_COLUMNS, treated)
    write_csv_new(
        classifiable_path,
        WORK_COLUMNS,
        [row for row in treated if row["status_tratamento"] == "mantido"],
    )
    write_csv_new(log_path, TREATMENT_LOG_COLUMNS, log_rows)
    write_csv_new(
        reconciliation_path,
        [
            "etapa",
            "entrada",
            "mantidos",
            "excluidos_tecnicos",
            "fora_classificacao_textual",
            "diferenca",
            "status",
        ],
        [
            {
                "etapa": "tratamento",
                **counts,
                "diferenca": 0,
                "status": "conciliado",
            }
        ],
    )
    outputs = [treated_path, classifiable_path, log_path, reconciliation_path]
    manifest = build_run_manifest(
        run_id=current_run,
        stage="limpeza_e_triagem",
        config_path=resolved_config,
        config=config,
        inputs=[input_path],
        outputs=outputs,
        counts=counts,
    )
    write_json_new(output_dir / "manifesto_execucao.json", manifest)
    return output_dir


def _validate_rows(rows: list[dict[str, str]], lot: str) -> None:
    seen: set[str] = set()
    for row in rows:
        if row.get("lote") != lot:
            raise PipelineError(f"Base contém registro de outro lote: {row.get('registro_id')}")
        record = row.get("registro_id", "")
        if not record or record in seen:
            raise PipelineError(f"registro_id ausente ou duplicado: {record}")
        seen.add(record)


def _technical_status(text: str) -> tuple[str, str]:
    stripped = text.strip()
    if not stripped:
        return "excluido_tecnico", "comentario_vazio"
    if _has_illegible_chars(text) or "\ufffd" in text:
        return "excluido_tecnico", "linha_tecnicamente_ilegivel"
    if normalize_text(stripped) in SYSTEM_NOISE:
        return "excluido_tecnico", "marcacao_automatica_ou_ruido_sistema"
    if URL_ONLY_RE.fullmatch(stripped):
        return "excluido_tecnico", "url_isolada"
    if _is_only_emoji(stripped):
        return "fora_classificacao_textual", "comentario_apenas_emoji_preservado"
    if not any(char.isalnum() for char in stripped):
        return "excluido_tecnico", "sem_sinal_textual_minimo"
    compact = re.sub(r"\s+", "", stripped)
    if len(compact) == 1 and not compact.isdigit():
        return "excluido_tecnico", "sem_sinal_textual_minimo"
    return "mantido", ""


def _count_key(status: str) -> str:
    return {
        "mantido": "mantidos",
        "excluido_tecnico": "excluidos_tecnicos",
        "fora_classificacao_textual": "fora_classificacao_textual",
    }[status]


def _has_illegible_chars(text: str) -> bool:
    allowed = {"\t", "\n", "\r"}
    for char in text:
        if char in allowed:
            continue
        if unicodedata.category(char) in {"Cc", "Cf"} and char not in {"\u200d", "\ufe0f", "\ufe0e"}:
            return True
    return False


def _is_only_emoji(text: str) -> bool:
    found = False
    for char in text:
        if char.isspace() or _is_emoji_component(char):
            continue
        if _is_emoji_char(char):
            found = True
            continue
        return False
    return found


def _is_emoji_component(char: str) -> bool:
    code = ord(char)
    return (
        code == 0x200D
        or 0xFE00 <= code <= 0xFE0F
        or 0x1F3FB <= code <= 0x1F3FF
        or 0xE0020 <= code <= 0xE007F
    )


def _is_emoji_char(char: str) -> bool:
    code = ord(char)
    return (
        0x1F300 <= code <= 0x1FAFF
        or 0x2600 <= code <= 0x27BF
        or 0x2300 <= code <= 0x23FF
    )

