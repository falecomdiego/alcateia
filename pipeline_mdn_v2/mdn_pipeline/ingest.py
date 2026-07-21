from __future__ import annotations

import hashlib
import hmac
import os
from pathlib import Path
from typing import Any, Mapping

from .core import (
    PipelineError,
    build_run_manifest,
    ensure_gate,
    ensure_new_directory,
    load_config,
    new_run_id,
    project_root,
    read_csv,
    record_id,
    resolve_project_path,
    sha256_file,
    validate_lot,
    verify_taxonomy,
    write_csv_new,
    write_json_new,
)
from .xlsx_reader import read_xlsx


WORK_COLUMNS = [
    "rodada_id",
    "registro_id",
    "lote",
    "fonte_id",
    "coleta_id",
    "arquivo_origem",
    "hash_arquivo_origem",
    "aba_origem",
    "linha_origem",
    "versao_taxonomia",
    "execucao_id",
    "autor_pseudo_id",
    "comentario_trabalho",
    "data_comentario",
    "status_tratamento",
    "motivo_tratamento",
]


def ingest_lot(
    *,
    lot: str,
    input_dir: Path,
    source_inventory: Path,
    collection_log: Path,
    lot_manifest: Path,
    config_path: str | Path | None = None,
    root: Path | None = None,
    run_id: str | None = None,
    pseudonym_key: str | None = None,
) -> Path:
    config, resolved_config = load_config(config_path, root)
    ensure_gate(config, "G1_collection")
    verify_taxonomy(config, root)
    lot_number = validate_lot(config, lot)
    base = (root or project_root()).resolve()

    raw_root = resolve_project_path(config["paths"]["raw_protected"], base)
    expected_input = (raw_root / lot).resolve()
    actual_input = input_dir.resolve()
    if actual_input != expected_input:
        raise PipelineError(f"Entrada do lote deve ser exatamente {expected_input}")
    if not actual_input.is_dir():
        raise PipelineError(f"Pasta de lote não encontrada: {actual_input}")

    key = pseudonym_key or os.environ.get("MDN_PSEUDONYM_KEY", "")
    if len(key.encode("utf-8")) < 16:
        raise PipelineError(
            "MDN_PSEUDONYM_KEY ausente ou curta. Use segredo com pelo menos 16 bytes fora do Git."
        )

    inventory = _load_source_inventory(source_inventory)
    collections = _load_collection_log(collection_log)
    manifest_rows = _load_lot_manifest(lot_manifest, lot)
    files = sorted(actual_input.glob("*.xlsx"), key=lambda item: item.name.casefold())
    if not files:
        raise PipelineError(f"Nenhum XLSX encontrado para {lot}")

    expected_names = {row["arquivo_gerado"] for row in manifest_rows}
    actual_names = {path.name for path in files}
    if expected_names != actual_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        raise PipelineError(f"Arquivos divergentes no lote. ausentes={missing} extras={extra}")

    manifest_by_file = {row["arquivo_gerado"]: row for row in manifest_rows}
    expected_columns = list(config["required_original_columns"])
    current_run = run_id or new_run_id()
    protected_rows: list[dict[str, str]] = []
    work_rows: list[dict[str, str]] = []
    mappings: dict[str, dict[str, str]] = {}
    seen_record_ids: set[str] = set()

    for file_path in files:
        lot_row = manifest_by_file[file_path.name]
        source_id = lot_row["fonte_id"]
        collection_id = lot_row["coleta_id"]
        if source_id not in inventory:
            raise PipelineError(f"Fonte do lote não existe no inventário: {source_id}")
        if inventory[source_id].get("status_planejado") != "aprovada":
            raise PipelineError(f"Fonte não aprovada para coleta: {source_id}")
        collection = collections.get(collection_id)
        if not collection:
            raise PipelineError(f"coleta_id ausente no log: {collection_id}")
        if collection.get("fonte_id") != source_id:
            raise PipelineError(f"Fonte divergente em {collection_id}")
        if collection.get("resultado") not in {"sucesso", "coletado"}:
            raise PipelineError(f"Coleta não concluída com sucesso: {collection_id}")
        if collection.get("arquivo_gerado") != file_path.name:
            raise PipelineError(f"Arquivo divergente em {collection_id}")

        actual_hash = sha256_file(file_path)
        registered_hashes = {
            lot_row.get("hash_sha256", "").lower(),
            collection.get("hash_sha256", "").lower(),
        }
        if registered_hashes != {actual_hash}:
            raise PipelineError(
                f"Hash divergente para {file_path.name}: registrado={registered_hashes} atual={actual_hash}"
            )

        sheets = read_xlsx(file_path, expected_columns)
        for sheet in sheets:
            for row_number, original in sheet.rows:
                rid = record_id(lot_number, source_id, sheet.index, row_number)
                if rid in seen_record_ids:
                    raise PipelineError(f"registro_id duplicado: {rid}")
                seen_record_ids.add(rid)
                control = {
                    "rodada_id": config["round_id"],
                    "registro_id": rid,
                    "lote": lot,
                    "fonte_id": source_id,
                    "coleta_id": collection_id,
                    "arquivo_origem": file_path.name,
                    "hash_arquivo_origem": actual_hash,
                    "aba_origem": sheet.name,
                    "linha_origem": str(row_number),
                    "versao_taxonomia": config["taxonomy"]["version"],
                    "execucao_id": current_run,
                }
                protected_rows.append({**original, **control})
                pseudo_source = (
                    original.get("User ID", "").strip()
                    or original.get("Profile URL", "").strip()
                    or original.get("User Name", "").strip()
                    or rid
                )
                pseudo_id = _pseudonym(key, pseudo_source)
                work_rows.append(
                    {
                        **control,
                        "autor_pseudo_id": pseudo_id,
                        "comentario_trabalho": original.get("Comment Text", ""),
                        "data_comentario": original.get("Comment Date", ""),
                        "status_tratamento": "nao_avaliado",
                        "motivo_tratamento": "",
                    }
                )
                mappings.setdefault(
                    pseudo_id,
                    {
                        "autor_pseudo_id": pseudo_id,
                        "User ID": original.get("User ID", ""),
                        "Profile URL": original.get("Profile URL", ""),
                        "User Name": original.get("User Name", ""),
                    },
                )

    processing_root = resolve_project_path(config["paths"]["processing"], base)
    output_dir = processing_root / "lotes" / lot / "02_ingestao" / current_run
    ensure_new_directory(output_dir)
    protected_path = output_dir / "base_tratada_protegida.csv"
    work_path = output_dir / "base_trabalho_pseudonimizada.csv"
    mapping_path = output_dir / "mapeamento_pseudonimos_protegido.csv"
    write_csv_new(
        protected_path,
        [*expected_columns, *config["control_columns"]],
        protected_rows,
    )
    write_csv_new(work_path, WORK_COLUMNS, work_rows)
    write_csv_new(
        mapping_path,
        ["autor_pseudo_id", "User ID", "Profile URL", "User Name"],
        mappings.values(),
    )
    outputs = [protected_path, work_path, mapping_path]
    run_manifest = build_run_manifest(
        run_id=current_run,
        stage="ingestao_e_pseudonimizacao",
        config_path=resolved_config,
        config=config,
        inputs=[source_inventory, collection_log, lot_manifest, *files],
        outputs=outputs,
        counts={
            "arquivos": len(files),
            "registros": len(protected_rows),
            "autores_pseudonimizados": len(mappings),
            "exclusoes": 0,
        },
    )
    write_json_new(output_dir / "manifesto_execucao.json", run_manifest)
    return output_dir


def _pseudonym(key: str, value: str) -> str:
    digest = hmac.new(key.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).hexdigest()
    return "MDN-AUTOR-" + digest[:20].upper()


def _load_source_inventory(path: Path) -> dict[str, dict[str, str]]:
    rows, fields = read_csv(path)
    required = {"fonte_id", "status_planejado", "motivo_inclusao"}
    _require_fields(path, fields, required)
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        source_id = row.get("fonte_id", "").strip()
        if not source_id:
            continue
        if source_id in output:
            raise PipelineError(f"fonte_id duplicado no inventário: {source_id}")
        if not row.get("motivo_inclusao", "").strip():
            raise PipelineError(f"Fonte sem motivo de inclusão: {source_id}")
        output[source_id] = row
    return output


def _load_collection_log(path: Path) -> dict[str, dict[str, str]]:
    rows, fields = read_csv(path)
    required = {
        "coleta_id",
        "fonte_id",
        "ferramenta",
        "versao_ferramenta",
        "resultado",
        "arquivo_gerado",
        "hash_sha256",
    }
    _require_fields(path, fields, required)
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        collection_id = row.get("coleta_id", "").strip()
        if not collection_id:
            continue
        if collection_id in output:
            raise PipelineError(f"coleta_id duplicado: {collection_id}")
        if row.get("resultado") in {"sucesso", "coletado"}:
            for field in ("ferramenta", "versao_ferramenta", "arquivo_gerado", "hash_sha256"):
                if not row.get(field, "").strip():
                    raise PipelineError(f"{collection_id} sem {field}")
        output[collection_id] = row
    return output


def _load_lot_manifest(path: Path, lot: str) -> list[dict[str, str]]:
    rows, fields = read_csv(path)
    required = {
        "lote",
        "fonte_id",
        "coleta_id",
        "arquivo_gerado",
        "hash_sha256",
        "status_autorizacao",
        "decisao_id",
    }
    _require_fields(path, fields, required)
    selected = [row for row in rows if row.get("lote") == lot]
    if not selected:
        raise PipelineError(f"Manifesto não contém arquivos para {lot}")
    names: set[str] = set()
    for row in selected:
        if row.get("status_autorizacao") != "autorizado":
            raise PipelineError(f"Arquivo não autorizado no lote: {row.get('arquivo_gerado')}")
        if not row.get("decisao_id", "").strip():
            raise PipelineError("Autorização de lote sem decisao_id")
        name = row.get("arquivo_gerado", "")
        if name in names:
            raise PipelineError(f"Arquivo duplicado no manifesto: {name}")
        names.add(name)
    return selected


def _require_fields(path: Path, fields: list[str], required: set[str]) -> None:
    missing = sorted(required - set(fields))
    if missing:
        raise PipelineError(f"{path} sem colunas: {missing}")
