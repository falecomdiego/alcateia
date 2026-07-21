from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ORIGINAL_COLUMNS = [
    "my-serial-number",
    "index",
    "User ID",
    "Avatar URL",
    "Profile URL",
    "User Name",
    "Comment Text",
    "Comment Date",
]

STANDARD_COLUMNS = [
    "id_linha",
    "lote",
    "arquivo_origem",
    "aba_origem",
    "linha_origem",
    "perfil_alvo",
    "conta_identificada",
    "url_postagem",
    "tipo_conteudo",
    "data_postagem",
    "usuario_comentario",
    "url_perfil_comentario",
    "id_usuario_comentario",
    "comentario_bruto",
    "data_comentario",
    "curtidas_comentario",
    "respostas_comentario",
    "metrica_validacao",
]

REQUIRED_COLUMNS = ORIGINAL_COLUMNS + STANDARD_COLUMNS

LOG_COLUMNS = [
    "id_linha",
    "lote",
    "arquivo_origem",
    "linha_origem",
    "usuario_comentario",
    "comentario_bruto",
    "motivo_exclusao",
]

SYSTEM_NOISE_VALUES = {
    "null",
    "none",
    "nan",
    "n/a",
    "na",
    "undefined",
    "nao_informado",
    "não informado",
    "sem comentario",
    "sem comentário",
    "comentario removido",
    "comentário removido",
    "comment deleted",
    "deleted comment",
    "[deleted]",
    "[removed]",
}

URL_ONLY_RE = re.compile(r"^(?:https?://|www\.)\S+$", re.IGNORECASE)


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    input_csv = resolve_input_csv(args.csv_padronizado, project_root)
    output_dir = project_root / "06_bases_limpas_por_lote"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, fieldnames = read_csv(input_csv)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    if missing_columns:
        raise SystemExit(
            "CSV padronizado com estrutura divergente. Colunas ausentes: "
            + ", ".join(missing_columns)
        )

    lote = identify_lote(rows, input_csv)
    clean_path = output_dir / f"{lote}_base_limpa.csv"
    log_path = output_dir / f"{lote}_logs_exclusao.csv"
    report_path = output_dir / f"{lote}_relatorio_limpeza.md"
    ensure_outputs_do_not_exist([clean_path, log_path, report_path])

    kept_rows, exclusion_log = clean_rows(rows)
    reason_counts = Counter(item["motivo_exclusao"] for item in exclusion_log)

    write_csv(clean_path, fieldnames, kept_rows)
    write_csv(log_path, LOG_COLUMNS, exclusion_log)
    write_report(
        report_path=report_path,
        input_csv=input_csv,
        clean_path=clean_path,
        log_path=log_path,
        lote=lote,
        total_input=len(rows),
        total_kept=len(kept_rows),
        total_removed=len(exclusion_log),
        reason_counts=reason_counts,
        invisible_exclusions=0,
        fieldnames=fieldnames,
    )

    print(f"Base limpa: {clean_path}")
    print(f"Log de exclusao: {log_path}")
    print(f"Relatorio tecnico: {report_path}")
    print(f"Linhas de entrada: {len(rows)}")
    print(f"Linhas mantidas: {len(kept_rows)}")
    print(f"Linhas removidas: {len(exclusion_log)}")
    print("Motivos de exclusao:")
    if reason_counts:
        for reason, count in sorted(reason_counts.items()):
            print(f"- {reason}: {count}")
    else:
        print("- nenhum: 0")
    print("Exclusoes sem log: 0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Executa limpeza tecnica com rastreabilidade em um CSV padronizado "
            "de comentarios do Instagram."
        )
    )
    parser.add_argument(
        "csv_padronizado",
        help=(
            "Caminho de um CSV padronizado em 04_bases_tratadas_por_lote, "
            "por exemplo 04_bases_tratadas_por_lote/lote_01_base_padronizada.csv."
        ),
    )
    return parser.parse_args()


def resolve_input_csv(raw_path: str, project_root: Path) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        cwd_candidate = Path.cwd() / candidate
        project_candidate = project_root / candidate
        candidate = cwd_candidate if cwd_candidate.exists() else project_candidate

    input_csv = candidate.resolve()
    if not input_csv.exists() or not input_csv.is_file():
        raise SystemExit(f"CSV padronizado de entrada nao encontrado: {input_csv}")

    allowed_dir = (project_root / "04_bases_tratadas_por_lote").resolve()
    if input_csv.parent != allowed_dir:
        raise SystemExit(
            "A limpeza deve usar apenas CSVs padronizados diretamente em "
            f"{allowed_dir}. Processamento interrompido."
        )

    forbidden_dirs = [
        (project_root / "02_xlsx_brutos_extensao_chrome").resolve(),
        (project_root / "03_lotes_processamento").resolve(),
    ]
    for forbidden_dir in forbidden_dirs:
        if input_csv == forbidden_dir or forbidden_dir in input_csv.parents:
            raise SystemExit(
                "A limpeza nao pode ler arquivos brutos XLSX nem pastas de lote bruto. "
                "Use o CSV padronizado da etapa anterior."
            )

    if input_csv.suffix.lower() != ".csv":
        raise SystemExit("A entrada da limpeza deve ser um arquivo CSV padronizado.")

    return input_csv


def read_csv(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    return rows, fieldnames


def identify_lote(rows: List[Dict[str, str]], input_csv: Path) -> str:
    lotes = sorted({row.get("lote", "").strip() for row in rows if row.get("lote", "").strip()})
    if len(lotes) == 1:
        return lotes[0]
    if len(lotes) > 1:
        raise SystemExit(
            "CSV contem mais de um lote. A limpeza deve ser executada por lote. "
            f"Lotes encontrados: {', '.join(lotes)}"
        )

    match = re.match(r"^(lote_\d+)_base_padronizada\.csv$", input_csv.name, re.IGNORECASE)
    if match:
        return match.group(1)
    raise SystemExit("Nao foi possivel identificar o lote a partir do CSV de entrada.")


def ensure_outputs_do_not_exist(paths: List[Path]) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing:
        raise SystemExit(
            "Saidas ja existentes detectadas. O script nao apaga nem sobrescreve arquivos: "
            + "; ".join(existing)
        )


def clean_rows(rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    kept_rows: List[Dict[str, str]] = []
    exclusion_log: List[Dict[str, str]] = []
    seen_duplicate_keys = set()

    for row in rows:
        motivo = technical_exclusion_reason(row)
        if not motivo:
            duplicate_key = (
                row.get("arquivo_origem", ""),
                row.get("usuario_comentario", ""),
                row.get("comentario_bruto", ""),
            )
            if duplicate_key in seen_duplicate_keys:
                motivo = "duplicidade_exata_mesmo_arquivo_usuario_comentario"
            else:
                seen_duplicate_keys.add(duplicate_key)

        if motivo:
            exclusion_log.append(build_log_row(row, motivo))
        else:
            kept_rows.append(row)

    if len(rows) - len(kept_rows) != len(exclusion_log):
        raise SystemExit("Falha de rastreabilidade: quantidade removida difere do log.")

    return kept_rows, exclusion_log


def technical_exclusion_reason(row: Dict[str, str]) -> Optional[str]:
    comment = row.get("comentario_bruto", "")
    stripped = comment.strip()

    if not stripped:
        return "comentario_vazio"
    if has_illegible_control_chars(comment) or "\ufffd" in comment:
        return "linha_tecnicamente_ilegivel"
    if is_system_noise(stripped):
        return "marcacao_automatica_ou_ruido_sistema"
    if is_isolated_url(stripped):
        return "url_isolada"
    if is_only_emoji(stripped):
        return "comentario_apenas_emoji"
    if has_no_minimum_text_signal(stripped):
        return "sem_relevancia_gramatical_minima"
    return None


def build_log_row(row: Dict[str, str], motivo: str) -> Dict[str, str]:
    return {
        "id_linha": row.get("id_linha", ""),
        "lote": row.get("lote", ""),
        "arquivo_origem": row.get("arquivo_origem", ""),
        "linha_origem": row.get("linha_origem", ""),
        "usuario_comentario": row.get("usuario_comentario", ""),
        "comentario_bruto": row.get("comentario_bruto", ""),
        "motivo_exclusao": motivo,
    }


def has_illegible_control_chars(text: str) -> bool:
    allowed = {"\t", "\n", "\r"}
    for char in text:
        if char in allowed:
            continue
        if unicodedata.category(char) in {"Cc", "Cf"} and char not in {"\u200d", "\ufe0f", "\ufe0e"}:
            return True
    return False


def is_system_noise(text: str) -> bool:
    normalized = normalize_for_noise(text)
    return normalized in SYSTEM_NOISE_VALUES


def normalize_for_noise(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).strip().lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def is_isolated_url(text: str) -> bool:
    return bool(URL_ONLY_RE.match(text))


def has_no_minimum_text_signal(text: str) -> bool:
    if not any(char.isalnum() for char in text):
        return True
    compact = re.sub(r"\s+", "", text)
    if len(compact) == 1 and not compact.isdigit():
        return True
    return False


def is_only_emoji(text: str) -> bool:
    has_emoji_char = False
    for char in text:
        if char.isspace() or is_emoji_component(char):
            continue
        if is_emoji_char(char):
            has_emoji_char = True
            continue
        return False
    return has_emoji_char


def is_emoji_component(char: str) -> bool:
    codepoint = ord(char)
    return (
        codepoint == 0x200D
        or 0xFE00 <= codepoint <= 0xFE0F
        or 0x1F3FB <= codepoint <= 0x1F3FF
        or 0xE0020 <= codepoint <= 0xE007F
    )


def is_emoji_char(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x1F300 <= codepoint <= 0x1FAFF
        or 0x2600 <= codepoint <= 0x27BF
        or 0x2300 <= codepoint <= 0x23FF
    )


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    report_path: Path,
    input_csv: Path,
    clean_path: Path,
    log_path: Path,
    lote: str,
    total_input: int,
    total_kept: int,
    total_removed: int,
    reason_counts: Counter,
    invisible_exclusions: int,
    fieldnames: List[str],
) -> None:
    lines = [
        f"# Relatorio tecnico de limpeza - {lote}",
        "",
        "## Entrada processada",
        "",
        f"`{input_csv}`",
        "",
        "## Saidas geradas",
        "",
        f"- Base limpa: `{clean_path}`",
        f"- Log de exclusao: `{log_path}`",
        f"- Relatorio tecnico: `{report_path}`",
        "",
        "## Colunas preservadas",
        "",
    ]
    for column in fieldnames:
        lines.append(f"- `{column}`")

    lines.extend(
        [
            "",
            "## Totais",
            "",
            f"- Linhas de entrada: {total_input}",
            f"- Linhas mantidas: {total_kept}",
            f"- Linhas removidas: {total_removed}",
            f"- Exclusoes sem log: {invisible_exclusions}",
            "",
            "## Distribuicao dos motivos de exclusao",
            "",
        ]
    )
    if reason_counts:
        lines.extend(["| Motivo | Quantidade |", "|---|---:|"])
        for reason, count in sorted(reason_counts.items()):
            lines.append(f"| `{reason}` | {count} |")
    else:
        lines.append("- Nenhuma linha removida.")

    lines.extend(
        [
            "",
            "## Confirmacao de rastreabilidade",
            "",
            "Nenhuma exclusao ocorreu sem registro no log de exclusao.",
            "",
            "## Escopo tecnico",
            "",
            "Esta etapa nao classifica comentarios, nao interpreta sentimentos, nao gera diagnostico estrategico e nao reescreve `comentario_bruto`.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
