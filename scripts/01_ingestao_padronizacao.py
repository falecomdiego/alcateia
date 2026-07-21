from __future__ import annotations

import argparse
import csv
import re
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET


NAO_INFORMADO = "nao_informado"

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

MATRIX_COLUMNS = [
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

OUTPUT_COLUMNS = ORIGINAL_COLUMNS + MATRIX_COLUMNS

FIELDS_WITHOUT_SOURCE = [
    "url_postagem",
    "tipo_conteudo",
    "data_postagem",
    "curtidas_comentario",
    "respostas_comentario",
]

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_OFFICE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


@dataclass
class FileReadResult:
    file_name: str
    sheets_read: List[str] = field(default_factory=list)
    columns_by_sheet: Dict[str, List[str]] = field(default_factory=dict)
    row_count: int = 0
    rows: List[Dict[str, str]] = field(default_factory=list)
    inconsistencies: List[str] = field(default_factory=list)


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    input_dir = resolve_input_dir(args.pasta_entrada, project_root)
    output_dir = project_root / "04_bases_tratadas_por_lote"
    output_dir.mkdir(parents=True, exist_ok=True)

    lote = input_dir.name
    csv_path = output_dir / f"{lote}_base_padronizada.csv"
    report_path = output_dir / f"{lote}_relatorio_colunas.md"

    files = sorted(input_dir.glob("*.xlsx"), key=lambda item: item.name.lower())
    if not files:
        report = build_report(
            input_dir=input_dir,
            lote=lote,
            files=[],
            results=[],
            rows=[],
            nao_informado_counts=Counter(),
            comentario_vazio_count=0,
            data_ausente_count=0,
            inconsistencies=["Nenhum arquivo XLSX encontrado na pasta informada."],
            csv_path=None,
        )
        write_text(report_path, report)
        print_summary(report_path, None, 0, 1)
        return 1

    all_rows: List[Dict[str, str]] = []
    all_results: List[FileReadResult] = []
    all_inconsistencies: List[str] = []
    nao_informado_counts: Counter[str] = Counter()
    comentario_vazio_count = 0
    data_ausente_count = 0

    for file_path in files:
        result = read_xlsx_file(file_path, lote)
        all_results.append(result)
        all_inconsistencies.extend(result.inconsistencies)
        all_rows.extend(result.rows)

    if all_inconsistencies:
        report = build_report(
            input_dir=input_dir,
            lote=lote,
            files=files,
            results=all_results,
            rows=all_rows,
            nao_informado_counts=nao_informado_counts,
            comentario_vazio_count=comentario_vazio_count,
            data_ausente_count=data_ausente_count,
            inconsistencies=all_inconsistencies,
            csv_path=None,
        )
        write_text(report_path, report)
        print_summary(report_path, None, len(all_rows), len(all_inconsistencies))
        return 1

    for row in all_rows:
        for field_name, value in row.items():
            if value == NAO_INFORMADO:
                nao_informado_counts[field_name] += 1
        if not row["comentario_bruto"].strip():
            comentario_vazio_count += 1
        if row["data_comentario"] == NAO_INFORMADO or not row["data_comentario"].strip():
            data_ausente_count += 1

    write_csv(csv_path, all_rows)
    report = build_report(
        input_dir=input_dir,
        lote=lote,
        files=files,
        results=all_results,
        rows=all_rows,
        nao_informado_counts=nao_informado_counts,
        comentario_vazio_count=comentario_vazio_count,
        data_ausente_count=data_ausente_count,
        inconsistencies=[],
        csv_path=csv_path,
    )
    write_text(report_path, report)
    print_summary(report_path, csv_path, len(all_rows), 0)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Executa a Camada 2: ingestao e padronizacao tecnica de um lote "
            "de XLSX de comentarios do Instagram."
        )
    )
    parser.add_argument(
        "pasta_entrada",
        help="Pasta de lote dentro de 03_lotes_processamento, por exemplo 03_lotes_processamento/lote_01.",
    )
    return parser.parse_args()


def resolve_input_dir(raw_path: str, project_root: Path) -> Path:
    candidate = Path(raw_path)
    attempted = [candidate]
    if not candidate.is_absolute():
        cwd_candidate = (Path.cwd() / candidate)
        project_candidate = (project_root / candidate)
        attempted = [cwd_candidate, project_candidate]
        candidate = cwd_candidate if cwd_candidate.exists() else project_candidate

    input_dir = candidate.resolve()
    if not input_dir.exists() or not input_dir.is_dir():
        attempted_text = ", ".join(str(path) for path in attempted)
        raise SystemExit(f"Pasta de entrada nao encontrada: {attempted_text}")

    expected_parent = (project_root / "03_lotes_processamento").resolve()
    if input_dir.parent != expected_parent:
        raise SystemExit(
            "A pasta de entrada deve ser um lote diretamente dentro de "
            f"{expected_parent}. Processamento interrompido."
        )

    forbidden_raw_dir = (project_root / "02_xlsx_brutos_extensao_chrome").resolve()
    if input_dir == forbidden_raw_dir or forbidden_raw_dir in input_dir.parents:
        raise SystemExit(
            "Leitura direta de 02_xlsx_brutos_extensao_chrome nao permitida. "
            "Use uma pasta de lote em 03_lotes_processamento."
        )

    return input_dir


def read_xlsx_file(file_path: Path, lote: str) -> FileReadResult:
    result = FileReadResult(file_name=file_path.name)
    try:
        with zipfile.ZipFile(file_path) as archive:
            shared_strings = read_shared_strings(archive)
            sheets = read_workbook_sheets(archive)

            if len(sheets) != 1 or sheets[0]["name"] != "Sheet1":
                sheet_names = ", ".join(sheet["name"] for sheet in sheets) or "nenhuma"
                result.inconsistencies.append(
                    f"{file_path.name}: abas encontradas ({sheet_names}); esperado apenas Sheet1."
                )
                return result

            sheet = sheets[0]
            rows = read_sheet_rows(archive, sheet["path"], shared_strings)
            if not rows:
                result.sheets_read.append(sheet["name"])
                result.columns_by_sheet[sheet["name"]] = []
                result.inconsistencies.append(f"{file_path.name}: aba Sheet1 sem cabecalho.")
                return result

            header_row = rows[0]
            headers = [header_row["values"].get(index, "") for index in sorted(header_row["values"])]
            result.sheets_read.append(sheet["name"])
            result.columns_by_sheet[sheet["name"]] = headers

            if headers != ORIGINAL_COLUMNS:
                result.inconsistencies.append(
                    f"{file_path.name}: colunas divergentes em Sheet1. "
                    f"Encontradas: {headers}. Esperadas: {ORIGINAL_COLUMNS}."
                )
                return result

            header_map = {
                column_name: index + 1 for index, column_name in enumerate(ORIGINAL_COLUMNS)
            }
            perfil_alvo = extract_perfil_alvo(file_path.name)
            for row in rows[1:]:
                values = row["values"]
                if not any(str(values.get(column_index, "")).strip() for column_index in header_map.values()):
                    continue

                output_row = build_output_row(
                    lote=lote,
                    file_name=file_path.name,
                    sheet_name=sheet["name"],
                    row_number=row["number"],
                    values=values,
                    header_map=header_map,
                    perfil_alvo=perfil_alvo,
                )
                result.rows.append(output_row)

            result.row_count = len(result.rows)
            return result
    except zipfile.BadZipFile:
        result.inconsistencies.append(f"{file_path.name}: arquivo XLSX invalido ou corrompido.")
    except KeyError as exc:
        result.inconsistencies.append(f"{file_path.name}: componente interno ausente no XLSX ({exc}).")
    except ET.ParseError as exc:
        result.inconsistencies.append(f"{file_path.name}: erro ao ler XML interno do XLSX ({exc}).")
    except OSError as exc:
        result.inconsistencies.append(f"{file_path.name}: erro de leitura ({exc}).")
    return result


def read_xml(archive: zipfile.ZipFile, name: str) -> ET.Element:
    with archive.open(name) as handle:
        return ET.fromstring(handle.read())


def read_workbook_sheets(archive: zipfile.ZipFile) -> List[Dict[str, str]]:
    workbook = read_xml(archive, "xl/workbook.xml")
    rels = read_xml(archive, "xl/_rels/workbook.xml.rels")
    rel_map = {}
    for rel in rels:
        rel_id = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rel_id and target:
            rel_map[rel_id] = normalize_target(target)

    sheets = []
    for sheet in workbook.findall(f".//{{{NS_MAIN}}}sheet"):
        rel_id = sheet.attrib.get(f"{{{NS_REL_OFFICE}}}id")
        sheets.append(
            {
                "name": sheet.attrib.get("name", ""),
                "path": rel_map.get(rel_id, ""),
            }
        )
    return sheets


def normalize_target(target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    if target.startswith("xl/"):
        return target
    return f"xl/{target}"


def read_shared_strings(archive: zipfile.ZipFile) -> List[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []

    root = read_xml(archive, "xl/sharedStrings.xml")
    strings = []
    for item in root.findall(f".//{{{NS_MAIN}}}si"):
        text_parts = [node.text or "" for node in item.findall(f".//{{{NS_MAIN}}}t")]
        strings.append("".join(text_parts))
    return strings


def read_sheet_rows(
    archive: zipfile.ZipFile, sheet_path: str, shared_strings: List[str]
) -> List[Dict[str, object]]:
    sheet_root = read_xml(archive, sheet_path)
    rows = []
    fallback_number = 0
    for row in sheet_root.findall(f".//{{{NS_MAIN}}}sheetData/{{{NS_MAIN}}}row"):
        fallback_number += 1
        row_number = int(row.attrib.get("r", fallback_number))
        values = {}
        for cell in row.findall(f"{{{NS_MAIN}}}c"):
            cell_ref = cell.attrib.get("r", "")
            if not cell_ref:
                continue
            values[column_index(cell_ref)] = cell_value(cell, shared_strings)
        if values:
            rows.append({"number": row_number, "values": values})
    return rows


def column_index(cell_ref: str) -> int:
    match = re.match(r"^([A-Z]+)", cell_ref.upper())
    if not match:
        return 0

    index = 0
    for char in match.group(1):
        index = index * 26 + (ord(char) - ord("A") + 1)
    return index


def cell_value(cell: ET.Element, shared_strings: List[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        text_parts = [node.text or "" for node in cell.findall(f".//{{{NS_MAIN}}}t")]
        return "".join(text_parts)

    value_node = cell.find(f"{{{NS_MAIN}}}v")
    if value_node is None:
        return ""

    raw_value = value_node.text or ""
    if cell_type == "s":
        try:
            return shared_strings[int(raw_value)]
        except (ValueError, IndexError):
            return raw_value
    return raw_value


def build_output_row(
    lote: str,
    file_name: str,
    sheet_name: str,
    row_number: int,
    values: Dict[int, str],
    header_map: Dict[str, int],
    perfil_alvo: str,
) -> Dict[str, str]:
    raw = {
        column_name: values.get(column_index_value, "")
        for column_name, column_index_value in header_map.items()
    }

    user_id = raw["User ID"].strip()
    user_name = raw["User Name"].strip()
    profile_url = raw["Profile URL"].strip()
    comment_text = raw["Comment Text"]
    comment_date = raw["Comment Date"].strip()

    matrix = {
        "id_linha": f"{lote}|{file_name}|linha_{row_number}",
        "lote": lote,
        "arquivo_origem": file_name,
        "aba_origem": sheet_name,
        "linha_origem": str(row_number),
        "perfil_alvo": perfil_alvo,
        "conta_identificada": user_id or NAO_INFORMADO,
        "url_postagem": NAO_INFORMADO,
        "tipo_conteudo": NAO_INFORMADO,
        "data_postagem": NAO_INFORMADO,
        "usuario_comentario": user_name or NAO_INFORMADO,
        "url_perfil_comentario": profile_url or NAO_INFORMADO,
        "id_usuario_comentario": user_id or NAO_INFORMADO,
        "comentario_bruto": comment_text,
        "data_comentario": comment_date or NAO_INFORMADO,
        "curtidas_comentario": NAO_INFORMADO,
        "respostas_comentario": NAO_INFORMADO,
    }
    matrix["metrica_validacao"] = build_validation_flag(raw, matrix)

    output = {}
    for column_name in ORIGINAL_COLUMNS:
        output[column_name] = raw[column_name]
    for column_name in MATRIX_COLUMNS:
        output[column_name] = matrix[column_name]
    return output


def build_validation_flag(raw: Dict[str, str], matrix: Dict[str, str]) -> str:
    flags = []
    if not raw["Comment Text"].strip():
        flags.append("comentario_vazio")
    if not raw["User Name"].strip():
        flags.append("usuario_ausente")
    if not raw["Comment Date"].strip():
        flags.append("data_ausente")

    ignored = {"comentario_bruto", "metrica_validacao"}
    has_nao_informado = any(
        value == NAO_INFORMADO for key, value in matrix.items() if key not in ignored
    )
    if has_nao_informado:
        flags.append("campo_nao_informado")

    if not flags:
        return "ok"
    return "|".join(flags)


def extract_perfil_alvo(file_name: str) -> str:
    match = re.match(r"^IGComment-All_\d{14}_(.+)\.xlsx$", file_name, flags=re.IGNORECASE)
    if not match:
        return NAO_INFORMADO
    perfil = match.group(1).strip()
    return perfil or NAO_INFORMADO


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def build_report(
    input_dir: Path,
    lote: str,
    files: List[Path],
    results: List[FileReadResult],
    rows: List[Dict[str, str]],
    nao_informado_counts: Counter[str],
    comentario_vazio_count: int,
    data_ausente_count: int,
    inconsistencies: List[str],
    csv_path: Optional[Path],
) -> str:
    sheets_by_file = {
        result.file_name: ", ".join(result.sheets_read) if result.sheets_read else "nenhuma"
        for result in results
    }
    columns_by_file = []
    for result in results:
        for sheet_name, columns in result.columns_by_sheet.items():
            columns_by_file.append((result.file_name, sheet_name, columns))

    lines = [
        f"# Relatorio tecnico de colunas - {lote}",
        "",
        "## Caminho de entrada processado",
        "",
        f"`{input_dir}`",
        "",
        "## Arquivos XLSX lidos",
        "",
        f"Quantidade de arquivos XLSX: {len(files)}",
        "",
    ]

    for file_path in files:
        lines.append(f"- `{file_path.name}`")

    lines.extend(["", "## Abas lidas", ""])
    if sheets_by_file:
        for file_name, sheets in sheets_by_file.items():
            lines.append(f"- `{file_name}`: {sheets}")
    else:
        lines.append("- Nenhuma aba lida.")

    lines.extend(["", "## Colunas encontradas", ""])
    if columns_by_file:
        for file_name, sheet_name, columns in columns_by_file:
            formatted_columns = ", ".join(f"`{column}`" for column in columns) or "nenhuma"
            lines.append(f"- `{file_name}` / `{sheet_name}`: {formatted_columns}")
    else:
        lines.append("- Nenhuma coluna encontrada.")

    lines.extend(["", "## Quantidade de linhas por arquivo", "", "| Arquivo | Linhas consolidadas |", "|---|---:|"])
    if results:
        for result in results:
            lines.append(f"| `{result.file_name}` | {result.row_count} |")
    else:
        lines.append("| Nenhum arquivo | 0 |")

    lines.extend(
        [
            "",
            "## Total de linhas consolidadas",
            "",
            str(len(rows)),
            "",
            "## Campos ausentes no XLSX original",
            "",
        ]
    )
    for field_name in FIELDS_WITHOUT_SOURCE:
        lines.append(f"- `{field_name}`")

    lines.extend(
        [
            "",
            "## Campos preenchidos como nao_informado",
            "",
            "| Campo | Quantidade |",
            "|---|---:|",
        ]
    )
    if nao_informado_counts:
        for field_name in sorted(nao_informado_counts):
            lines.append(f"| `{field_name}` | {nao_informado_counts[field_name]} |")
    else:
        lines.append("| Nenhum | 0 |")

    lines.extend(
        [
            "",
            "## Validacoes tecnicas",
            "",
            f"- Comentarios vazios: {comentario_vazio_count}",
            f"- Datas ausentes: {data_ausente_count}",
            "- Linhas excluidas: 0",
            "- Confirmacao: nenhuma linha foi excluida nesta etapa.",
            "",
            "## Inconsistencias estruturais",
            "",
        ]
    )
    if inconsistencies:
        for item in inconsistencies:
            lines.append(f"- {item}")
    else:
        lines.append("- Nenhuma inconsistencia estrutural identificada.")

    lines.extend(["", "## Arquivos gerados", ""])
    if csv_path:
        lines.append(f"- CSV padronizado: `{csv_path}`")
    else:
        lines.append("- CSV padronizado: nao gerado por inconsistencia estrutural ou erro de leitura.")
    lines.append("- Relatorio tecnico: este arquivo.")
    lines.append("")
    return "\n".join(lines)


def print_summary(
    report_path: Path, csv_path: Optional[Path], total_rows: int, inconsistency_count: int
) -> None:
    print(f"Relatorio tecnico: {report_path}")
    if csv_path:
        print(f"CSV padronizado: {csv_path}")
    else:
        print("CSV padronizado: nao gerado")
    print(f"Linhas processadas: {total_rows}")
    print(f"Inconsistencias encontradas: {inconsistency_count}")


if __name__ == "__main__":
    sys.exit(main())
