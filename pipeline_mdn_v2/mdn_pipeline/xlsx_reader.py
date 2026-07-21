from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from xml.etree import ElementTree as ET

from .core import PipelineError


NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_OFFICE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PACKAGE = "http://schemas.openxmlformats.org/package/2006/relationships"


@dataclass(frozen=True)
class SheetData:
    name: str
    index: int
    rows: list[tuple[int, dict[str, str]]]


def read_xlsx(path: Path, expected_columns: Sequence[str]) -> list[SheetData]:
    try:
        with zipfile.ZipFile(path) as archive:
            shared_strings = _read_shared_strings(archive)
            sheets = _read_workbook_sheets(archive)
            output: list[SheetData] = []
            for sheet_index, (sheet_name, xml_path) in enumerate(sheets, start=1):
                rows = _read_sheet_rows(archive, xml_path, shared_strings)
                if not rows:
                    raise PipelineError(f"Aba vazia em {path.name}: {sheet_name}")
                header_number, header_values = rows[0]
                headers = _ordered_values(header_values)
                if headers != list(expected_columns):
                    raise PipelineError(
                        f"Cabeçalho divergente em {path.name}/{sheet_name} linha {header_number}. "
                        f"Esperado={list(expected_columns)} Encontrado={headers}"
                    )
                parsed_rows: list[tuple[int, dict[str, str]]] = []
                for row_number, values in rows[1:]:
                    parsed_rows.append(
                        (
                            row_number,
                            {
                                column: values.get(index, "")
                                for index, column in enumerate(expected_columns, start=1)
                            },
                        )
                    )
                output.append(SheetData(sheet_name, sheet_index, parsed_rows))
            return output
    except zipfile.BadZipFile as exc:
        raise PipelineError(f"XLSX inválido ou corrompido: {path}") from exc
    except KeyError as exc:
        raise PipelineError(f"Estrutura interna ausente no XLSX {path}: {exc}") from exc


def _read_workbook_sheets(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        rel.attrib.get("Id", ""): rel.attrib.get("Target", "")
        for rel in rels.findall(f"{{{NS_REL_PACKAGE}}}Relationship")
    }
    sheets: list[tuple[str, str]] = []
    for sheet in workbook.findall(f".//{{{NS_MAIN}}}sheet"):
        name = sheet.attrib.get("name", "").strip()
        rel_id = sheet.attrib.get(f"{{{NS_REL_OFFICE}}}id", "")
        target = targets.get(rel_id, "")
        if not name or not target:
            raise PipelineError("Relação de aba inválida no workbook")
        sheets.append((name, _normalize_target(target)))
    if not sheets:
        raise PipelineError("Nenhuma aba encontrada no XLSX")
    return sheets


def _normalize_target(target: str) -> str:
    value = target.replace("\\", "/")
    if value.startswith("/"):
        return value.lstrip("/")
    if value.startswith("xl/"):
        return value
    parts: list[str] = ["xl"]
    for part in value.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            if len(parts) > 1:
                parts.pop()
            continue
        parts.append(part)
    return "/".join(parts)


def _read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    values: list[str] = []
    for item in root.findall(f"{{{NS_MAIN}}}si"):
        parts = [node.text or "" for node in item.findall(f".//{{{NS_MAIN}}}t")]
        values.append("".join(parts))
    return values


def _read_sheet_rows(
    archive: zipfile.ZipFile,
    xml_path: str,
    shared_strings: list[str],
) -> list[tuple[int, dict[int, str]]]:
    root = ET.fromstring(archive.read(xml_path))
    output: list[tuple[int, dict[int, str]]] = []
    fallback_row = 0
    for row in root.findall(f".//{{{NS_MAIN}}}row"):
        fallback_row += 1
        row_number = int(row.attrib.get("r", fallback_row))
        values: dict[int, str] = {}
        fallback_column = 0
        for cell in row.findall(f"{{{NS_MAIN}}}c"):
            fallback_column += 1
            reference = cell.attrib.get("r", "")
            column = _column_index(reference) if reference else fallback_column
            values[column] = _cell_value(cell, shared_strings)
        output.append((row_number, values))
    return output


def _column_index(reference: str) -> int:
    match = re.match(r"^([A-Za-z]+)", reference)
    if not match:
        raise PipelineError(f"Referência de célula inválida: {reference}")
    value = 0
    for char in match.group(1).upper():
        value = value * 26 + (ord(char) - ord("A") + 1)
    return value


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t", "")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(f".//{{{NS_MAIN}}}t"))
    value_node = cell.find(f"{{{NS_MAIN}}}v")
    if value_node is None:
        return ""
    raw = value_node.text or ""
    if cell_type == "s":
        try:
            return shared_strings[int(raw)]
        except (ValueError, IndexError):
            raise PipelineError(f"Índice inválido em sharedStrings: {raw}")
    if cell_type == "b":
        return "true" if raw == "1" else "false"
    return raw


def _ordered_values(values: dict[int, str]) -> list[str]:
    if not values:
        return []
    return [values.get(index, "") for index in range(1, max(values) + 1)]

