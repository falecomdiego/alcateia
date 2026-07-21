from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


DEFAULT_CONFIG = Path(
    "20_rodada_prospectiva_padronizada_01/config/MDN-RPP01-CONF-001-V0.1.json"
)
LOT_RE = re.compile(r"^lote_(\d{2})$")
SOURCE_RE = re.compile(r"^MDN-RPP01-FON-(\d{3})$")
RUN_RE = re.compile(r"^MDN-RPP01-EXE-\d{8}-\d{6}$")


class PipelineError(RuntimeError):
    """Erro controlado que interrompe uma etapa sem produzir resultado parcial."""


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_project_path(value: str | Path, root: Path | None = None) -> Path:
    base = (root or project_root()).resolve()
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise PipelineError(f"Falha ao ler JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PipelineError(f"JSON deve conter um objeto na raiz: {path}")
    return value


def load_config(path: str | Path | None = None, root: Path | None = None) -> tuple[dict[str, Any], Path]:
    base = (root or project_root()).resolve()
    config_path = resolve_project_path(path or DEFAULT_CONFIG, base)
    config = load_json(config_path)
    validate_config(config, base)
    return config, config_path


def validate_config(config: Mapping[str, Any], root: Path | None = None) -> None:
    base = (root or project_root()).resolve()
    required = ["round_id", "paths", "taxonomy", "gates", "validation", "public_safety"]
    missing = [key for key in required if key not in config]
    if missing:
        raise PipelineError("Configuração sem campos obrigatórios: " + ", ".join(missing))
    if config["round_id"] != "MDN-RPP01":
        raise PipelineError("round_id deve ser MDN-RPP01")

    paths = config["paths"]
    if not isinstance(paths, Mapping):
        raise PipelineError("paths deve ser um objeto")
    round_root = resolve_project_path(paths.get("round_root", ""), base)
    expected_root = (base / "20_rodada_prospectiva_padronizada_01").resolve()
    if round_root != expected_root:
        raise PipelineError("A configuração deve permanecer na pasta exclusiva da MDN-RPP01")
    for key, raw_path in paths.items():
        resolved = resolve_project_path(str(raw_path), base)
        if resolved != round_root and round_root not in resolved.parents:
            raise PipelineError(f"Caminho fora da rodada em paths.{key}: {resolved}")

    taxonomy = config["taxonomy"]
    taxonomy_path = resolve_project_path(taxonomy.get("source", ""), base)
    if not taxonomy_path.is_file():
        raise PipelineError(f"Taxonomia não encontrada: {taxonomy_path}")
    expected_hash = str(taxonomy.get("sha256", "")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        raise PipelineError("Hash SHA-256 da taxonomia inválido")
    if taxonomy.get("version") != "1.1" or taxonomy.get("frozen_for_round") is not True:
        raise PipelineError("A rodada exige Taxonomia Mestre V1.1 congelada")
    if taxonomy.get("allow_mid_round_changes") is not False:
        raise PipelineError("Alteração da taxonomia durante a rodada deve estar bloqueada")

    gates = config["gates"]
    gate_order = [
        "G0_protocol",
        "G1_collection",
        "G2_analysis",
        "G3_consolidation",
        "G4_publication",
        "G5_reapplication",
    ]
    for gate in gate_order:
        if not isinstance(gates.get(gate), bool):
            raise PipelineError(f"Gate ausente ou não booleano: {gate}")
    for previous, current in zip(gate_order, gate_order[1:]):
        if gates[current] and not gates[previous]:
            raise PipelineError(f"{current} não pode estar aprovado com {previous} bloqueado")

    period = config.get("period", {})
    if gates["G0_protocol"] and (not period.get("start") or not period.get("end")):
        raise PipelineError("G0 aprovado exige período inicial e final")
    lots = config.get("lots", [])
    if not isinstance(lots, list) or any(not LOT_RE.fullmatch(str(item)) for item in lots):
        raise PipelineError("lots deve conter somente códigos lote_NN")
    if gates["G1_collection"] and not lots:
        raise PipelineError("G1 aprovado exige ao menos um lote registrado")

    validation = config["validation"]
    if int(validation.get("minimum_sample", 0)) < 1:
        raise PipelineError("minimum_sample deve ser positivo")
    for key in ("sample_rate", "double_review_rate", "minimum_public_precision"):
        value = float(validation.get(key, -1))
        if not 0 < value <= 1:
            raise PipelineError(f"validation.{key} deve estar entre 0 e 1")
    if int(config["public_safety"].get("minimum_cell_size", 0)) < 2:
        raise PipelineError("minimum_cell_size deve ser pelo menos 2")


def ensure_gate(config: Mapping[str, Any], gate: str) -> None:
    if config.get("gates", {}).get(gate) is not True:
        raise PipelineError(f"Execução bloqueada: {gate} ainda não foi aprovado")


def validate_lot(config: Mapping[str, Any], lot: str) -> str:
    match = LOT_RE.fullmatch(lot)
    if not match:
        raise PipelineError("Lote deve seguir o formato lote_NN")
    if lot not in config.get("lots", []):
        raise PipelineError(f"Lote não registrado na configuração: {lot}")
    return match.group(1)


def source_number(source_id: str) -> str:
    match = SOURCE_RE.fullmatch(source_id)
    if not match:
        raise PipelineError(f"fonte_id inválido: {source_id}")
    return match.group(1)


def new_run_id(now: datetime | None = None) -> str:
    value = now or datetime.now().astimezone()
    return f"MDN-RPP01-EXE-{value.strftime('%Y%m%d-%H%M%S')}"


def record_id(lot_number: str, source_id: str, sheet_index: int, row_number: int) -> str:
    if sheet_index < 1 or row_number < 2:
        raise PipelineError("Índices de aba e linha inválidos para registro_id")
    return (
        f"MDN-RPP01-L{lot_number}-F{source_number(source_id)}-"
        f"A{sheet_index:02d}-R{row_number:06d}"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_hash(root: Path | None = None) -> str:
    base = (root or project_root()).resolve() / "pipeline_mdn_v2"
    digest = hashlib.sha256()
    files = sorted(
        [*base.rglob("*.py"), *base.rglob("*.json")],
        key=lambda item: item.as_posix(),
    )
    for path in files:
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def ensure_new_directory(path: Path) -> None:
    if path.exists():
        raise PipelineError(f"Saída já existe; sobrescrita proibida: {path}")
    path.mkdir(parents=True, exist_ok=False)


def write_csv_new(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    if path.exists():
        raise PipelineError(f"Arquivo já existe; sobrescrita proibida: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        return [dict(row) for row in reader], fields


def write_json_new(path: Path, value: Mapping[str, Any]) -> None:
    if path.exists():
        raise PipelineError(f"Arquivo já existe; sobrescrita proibida: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text_new(path: Path, value: str) -> None:
    if path.exists():
        raise PipelineError(f"Arquivo já existe; sobrescrita proibida: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.casefold())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", normalized).strip()


def term_present(normalized_text: str, term: str) -> bool:
    normalized_term = normalize_text(term)
    if not normalized_term:
        return False
    pattern = r"(?<!\w)" + re.escape(normalized_term) + r"(?!\w)"
    return re.search(pattern, normalized_text) is not None


def file_inventory(paths: Iterable[Path]) -> list[dict[str, Any]]:
    inventory = []
    for path in sorted(paths, key=lambda item: item.as_posix()):
        inventory.append(
            {
                "path": path.as_posix(),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    return inventory


def build_run_manifest(
    *,
    run_id: str,
    stage: str,
    config_path: Path,
    config: Mapping[str, Any],
    inputs: Sequence[Path],
    outputs: Sequence[Path],
    counts: Mapping[str, int],
    inconsistencies: Sequence[str] = (),
    human_decisions: Sequence[str] = (),
) -> dict[str, Any]:
    if not RUN_RE.fullmatch(run_id):
        raise PipelineError(f"execucao_id inválido: {run_id}")
    config_root = config_path.resolve().parents[2]
    taxonomy_path = resolve_project_path(config["taxonomy"]["source"], config_root)
    return {
        "execucao_id": run_id,
        "etapa": stage,
        "data_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
        "operador": os.environ.get("USERNAME") or os.environ.get("USER") or "nao_informado",
        "comando": list(sys.argv),
        "diretorio_execucao": Path.cwd().resolve().as_posix(),
        "ambiente": {
            "python": sys.version.split()[0],
            "sistema": platform.platform(),
        },
        "codigo": {
            "versao": "0.1.0",
            "hash_pacote": package_hash(),
        },
        "configuracao": {
            "path": config_path.as_posix(),
            "sha256": sha256_file(config_path),
        },
        "taxonomia": {
            "versao": config["taxonomy"]["version"],
            "path": taxonomy_path.as_posix(),
            "sha256": sha256_file(taxonomy_path),
        },
        "entradas": file_inventory(inputs),
        "saidas": file_inventory(outputs),
        "contagens": dict(counts),
        "inconsistencias": list(inconsistencies),
        "decisoes_humanas_incorporadas": list(human_decisions),
    }


def verify_taxonomy(config: Mapping[str, Any], root: Path | None = None) -> str:
    path = resolve_project_path(config["taxonomy"]["source"], root or project_root())
    actual = sha256_file(path)
    expected = str(config["taxonomy"]["sha256"]).lower()
    if actual != expected:
        raise PipelineError(
            "Taxonomia divergiu do snapshot congelado. Processamento interrompido: "
            f"esperado={expected} atual={actual}"
        )
    return actual


def verify_run_manifest(path: Path) -> dict[str, int]:
    manifest = load_json(path)
    checked_inputs = 0
    checked_outputs = 0
    for section, counter_name in (("entradas", "inputs"), ("saidas", "outputs")):
        entries = manifest.get(section)
        if not isinstance(entries, list):
            raise PipelineError(f"Manifesto sem lista {section}")
        for item in entries:
            if not isinstance(item, Mapping):
                raise PipelineError(f"Entrada inválida no manifesto: {item}")
            file_path = Path(str(item.get("path", "")))
            if not file_path.is_file():
                raise PipelineError(f"Arquivo do manifesto não encontrado: {file_path}")
            actual = sha256_file(file_path)
            if actual != item.get("sha256"):
                raise PipelineError(f"Hash divergente no manifesto: {file_path}")
            if counter_name == "inputs":
                checked_inputs += 1
            else:
                checked_outputs += 1
    return {"entradas_verificadas": checked_inputs, "saidas_verificadas": checked_outputs}
