from __future__ import annotations

import argparse
import ast
import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


NAO_IDENTIFICADO = "nao_identificado"
SEM_CRITERIO = "sem_criterio_identificado"

BASE_REQUIRED_COLUMNS = [
    "id_linha",
    "lote",
    "arquivo_origem",
    "perfil_alvo",
    "conta_identificada",
    "url_postagem",
    "tipo_conteudo",
    "data_postagem",
    "usuario_comentario",
    "comentario_bruto",
    "metrica_validacao",
]

OUTPUT_COLUMNS = [
    "id_linha",
    "lote",
    "arquivo_origem",
    "perfil_alvo",
    "conta_identificada",
    "url_postagem",
    "tipo_conteudo",
    "data_postagem",
    "usuario_comentario",
    "comentario_bruto",
    "comentario_limpo",
    "metrica_validacao",
    "eixo_mercado",
    "categoria_operacional",
    "categoria_experiencial",
    "entidade_monitorada",
    "criterio_corte_aplicado",
    "justificativa_vinculo",
    "status_relevancia",
    "grau_confianca",
]

SAMPLE_COLUMNS = [
    "id_linha",
    "arquivo_origem",
    "usuario_comentario",
    "comentario_bruto",
    "comentario_limpo",
    "eixo_mercado",
    "categoria_operacional",
    "categoria_experiencial",
    "entidade_monitorada",
    "criterio_corte_aplicado",
    "justificativa_vinculo",
    "status_relevancia",
    "grau_confianca",
]


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    input_csv = resolve_input_csv(args.base_limpa, project_root)
    rules_dir = project_root / "rules"
    output_dir = project_root / "07_classificacao_pilar2_por_lote"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, fieldnames = read_csv(input_csv)
    validate_base_columns(fieldnames)
    lote = identify_lote(rows, input_csv)

    rules = load_all_rules(rules_dir)
    output_rows = classify_rows(rows, rules)

    if len(output_rows) != len(rows):
        raise SystemExit("Falha de controle: a classificacao nao preservou todas as linhas.")

    table_path = output_dir / f"{lote}_tabela_pilar2.csv"
    report_path = output_dir / f"{lote}_relatorio_classificacao_pilar2.md"
    sample_path = output_dir / f"{lote}_amostra_revisao_pilar2.csv"

    write_csv(table_path, OUTPUT_COLUMNS, output_rows)
    write_csv(sample_path, SAMPLE_COLUMNS, build_review_sample(output_rows, 50))
    write_report(
        report_path=report_path,
        input_csv=input_csv,
        table_path=table_path,
        sample_path=sample_path,
        lote=lote,
        output_rows=output_rows,
        rules=rules,
        inconsistencies=[],
    )

    print(f"Tabela Pilar 2: {table_path}")
    print(f"Relatorio tecnico: {report_path}")
    print(f"Amostra de revisao: {sample_path}")
    print(f"Linhas processadas: {len(output_rows)}")
    print_counter("Distribuicao por eixo_mercado", Counter(row["eixo_mercado"] for row in output_rows))
    print_counter(
        "Distribuicao por status_relevancia",
        Counter(row["status_relevancia"] for row in output_rows),
    )
    print_counter(
        "Distribuicao por grau_confianca",
        Counter(row["grau_confianca"] for row in output_rows),
    )
    print("Linhas excluidas: 0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Executa classificacao tecnica da Camada 2 para gerar a tabela "
            "estruturada de saida do Pilar 2, sem diagnostico estrategico."
        )
    )
    parser.add_argument(
        "base_limpa",
        help=(
            "Caminho de uma base limpa por lote em 06_bases_limpas_por_lote, "
            "por exemplo 06_bases_limpas_por_lote/lote_01_base_limpa.csv."
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
        raise SystemExit(f"Base limpa de entrada nao encontrada: {input_csv}")

    allowed_dir = (project_root / "06_bases_limpas_por_lote").resolve()
    if input_csv.parent != allowed_dir:
        raise SystemExit(
            "A classificacao do Pilar 2 deve usar apenas CSVs de base limpa "
            f"diretamente em {allowed_dir}. Processamento interrompido."
        )

    if input_csv.suffix.lower() != ".csv":
        raise SystemExit("A entrada da classificacao deve ser um arquivo CSV.")

    forbidden_dirs = [
        (project_root / "02_xlsx_brutos_extensao_chrome").resolve(),
        (project_root / "03_lotes_processamento").resolve(),
        (project_root / "04_bases_tratadas_por_lote").resolve(),
    ]
    for forbidden_dir in forbidden_dirs:
        if input_csv == forbidden_dir or forbidden_dir in input_csv.parents:
            raise SystemExit(
                "Entrada invalida para classificacao. Use somente uma base limpa "
                "gerada pela etapa 02."
            )

    return input_csv


def read_csv(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    return rows, fieldnames


def validate_base_columns(fieldnames: List[str]) -> None:
    missing = [column for column in BASE_REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        raise SystemExit(
            "Base limpa com estrutura divergente. Colunas ausentes: "
            + ", ".join(missing)
        )


def identify_lote(rows: List[Dict[str, str]], input_csv: Path) -> str:
    lotes = sorted({row.get("lote", "").strip() for row in rows if row.get("lote", "").strip()})
    if len(lotes) == 1:
        return lotes[0]
    if len(lotes) > 1:
        raise SystemExit(
            "Base limpa contem mais de um lote. A classificacao deve ser executada por lote. "
            f"Lotes encontrados: {', '.join(lotes)}"
        )

    match = re.match(r"^(lote_\d+)_base_limpa\.csv$", input_csv.name, re.IGNORECASE)
    if match:
        return match.group(1)
    raise SystemExit("Nao foi possivel identificar o lote a partir da base limpa.")


def load_all_rules(rules_dir: Path) -> Dict[str, object]:
    operational_path = rules_dir / "categorias_operacionais.yml"
    experiential_path = rules_dir / "categorias_experienciais.yml"
    entities_path = rules_dir / "entidades_monitoradas.yml"

    missing = [str(path) for path in [operational_path, experiential_path] if not path.exists()]
    if missing:
        raise SystemExit("Arquivos de regras obrigatorios ausentes: " + "; ".join(missing))

    operational = load_rule_items(operational_path, expected_type="operacional")
    experiential = load_rule_items(experiential_path, expected_type="experiencial")
    entities = load_entity_items(entities_path) if entities_path.exists() else []

    return {
        "arquivos_carregados": [
            str(operational_path),
            str(experiential_path),
        ]
        + ([str(entities_path)] if entities_path.exists() else []),
        "entidades_monitoradas_existente": entities_path.exists(),
        "operacional": operational,
        "experiencial": experiential,
        "entidades": entities,
    }


def load_rule_items(path: Path, expected_type: str) -> List[Dict[str, object]]:
    data = load_yaml_like(path)
    raw_items = data.get("categorias", [])
    items = []
    for item in raw_items:
        item_type = str(item.get("tipo_categoria", "")).strip()
        if item_type != expected_type:
            continue
        items.append(normalize_rule_item(item))
    return items


def load_entity_items(path: Path) -> List[Dict[str, object]]:
    data = load_yaml_like(path)
    raw_items = (
        data.get("entidades")
        or data.get("entidades_monitoradas")
        or data.get("categorias")
        or data.get("itens")
        or []
    )
    return [normalize_rule_item(item) for item in raw_items]


def load_yaml_like(path: Path) -> Dict[str, object]:
    try:
        import yaml  # type: ignore

        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if isinstance(data, dict):
            return data
    except ImportError:
        pass

    return parse_simple_yaml(path)


def parse_simple_yaml(path: Path) -> Dict[str, object]:
    data: Dict[str, object] = {"categorias": []}
    current_section: Optional[str] = None
    current_item: Optional[Dict[str, object]] = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            if current_section not in data:
                data[current_section] = []
            current_item = None
            continue

        if current_section and line.startswith("  - "):
            if current_item:
                as_list = data.setdefault(current_section, [])
                if isinstance(as_list, list):
                    as_list.append(current_item)
            current_item = {}
            remainder = line[4:].strip()
            if ":" in remainder:
                key, value = remainder.split(":", 1)
                current_item[key.strip()] = parse_scalar_or_list(value.strip())
            continue

        if current_item is not None and line.startswith("    ") and ":" in line:
            key, value = line.strip().split(":", 1)
            current_item[key.strip()] = parse_scalar_or_list(value.strip())

    if current_section and current_item:
        as_list = data.setdefault(current_section, [])
        if isinstance(as_list, list):
            as_list.append(current_item)

    return data


def parse_scalar_or_list(value: str) -> object:
    value = value.strip()
    if value == "":
        return ""
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, (str, int, float, list)):
            return parsed
    except (SyntaxError, ValueError):
        pass
    return value.strip('"').strip("'")


def normalize_rule_item(item: Dict[str, object]) -> Dict[str, object]:
    item_id = str(item.get("id") or item.get("nome") or "").strip()
    name = str(item.get("nome") or item_id).strip()
    keywords = as_text_list(item.get("palavras_chave", []))
    expressions = as_text_list(item.get("expressoes_equivalentes", []))
    associated_terms = as_text_list(item.get("termos_associados", []))
    try:
        weight = int(item.get("peso_inicial", 1))
    except (TypeError, ValueError):
        weight = 1
    return {
        "id": item_id,
        "nome": name,
        "palavras_chave": keywords,
        "expressoes_equivalentes": expressions,
        "termos_associados": associated_terms,
        "peso_inicial": max(1, min(3, weight)),
    }


def as_text_list(value: object) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def classify_rows(rows: List[Dict[str, str]], rules: Dict[str, object]) -> List[Dict[str, str]]:
    output_rows = []
    for row in rows:
        comentario_bruto = row.get("comentario_bruto", "")
        comentario_limpo = row.get("comentario_limpo", "").strip()
        if not comentario_limpo:
            comentario_limpo = clean_comment_for_matching(comentario_bruto)

        operational_matches = match_items(
            comentario_limpo, rules["operacional"], label="categoria_operacional"
        )
        experiential_matches = match_items(
            comentario_limpo, rules["experiencial"], label="categoria_experiencial"
        )
        entity_matches = match_items(
            comentario_limpo, rules["entidades"], label="entidade_monitorada"
        )

        axis = determine_axis(operational_matches, experiential_matches, entity_matches)
        criteria = collect_criteria(operational_matches, experiential_matches, entity_matches)
        justification = build_justification(
            operational_matches, experiential_matches, entity_matches
        )
        status = determine_status(axis, operational_matches, experiential_matches, entity_matches)
        confidence = determine_confidence(
            axis, operational_matches, experiential_matches, entity_matches
        )

        output_rows.append(
            {
                "id_linha": row.get("id_linha", ""),
                "lote": row.get("lote", ""),
                "arquivo_origem": row.get("arquivo_origem", ""),
                "perfil_alvo": row.get("perfil_alvo", ""),
                "conta_identificada": row.get("conta_identificada", ""),
                "url_postagem": row.get("url_postagem", ""),
                "tipo_conteudo": row.get("tipo_conteudo", ""),
                "data_postagem": row.get("data_postagem", ""),
                "usuario_comentario": row.get("usuario_comentario", ""),
                "comentario_bruto": comentario_bruto,
                "comentario_limpo": comentario_limpo,
                "metrica_validacao": row.get("metrica_validacao", ""),
                "eixo_mercado": axis,
                "categoria_operacional": join_ids(operational_matches),
                "categoria_experiencial": join_ids(experiential_matches),
                "entidade_monitorada": join_ids(entity_matches),
                "criterio_corte_aplicado": criteria,
                "justificativa_vinculo": justification,
                "status_relevancia": status,
                "grau_confianca": confidence,
            }
        )
    return output_rows


def clean_comment_for_matching(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def match_items(
    comment: str, items: object, label: str
) -> List[Dict[str, object]]:
    if not isinstance(items, list):
        return []

    normalized_comment = normalize_text(comment)
    matches = []
    for item in items:
        if not isinstance(item, dict):
            continue
        item_matches = []
        item_matches.extend(
            match_terms(normalized_comment, item.get("expressoes_equivalentes", []), "expressao_equivalente")
        )
        item_matches.extend(
            match_terms(normalized_comment, item.get("palavras_chave", []), "palavra_chave")
        )
        item_matches.extend(
            match_terms(normalized_comment, item.get("termos_associados", []), "termo_associado")
        )
        if item_matches:
            first_match = item_matches[0]
            matches.append(
                {
                    "label": label,
                    "id": str(item.get("id", "")),
                    "nome": str(item.get("nome", item.get("id", ""))),
                    "peso_inicial": int(item.get("peso_inicial", 1)),
                    "criterio": first_match["criterio"],
                    "evidencia": first_match["termo_original"],
                    "all_matches": item_matches,
                }
            )
    return matches


def match_terms(
    normalized_comment: str, terms: object, criterion: str
) -> List[Dict[str, str]]:
    matches = []
    for term in as_text_list(terms):
        normalized_term = normalize_text(term)
        if not normalized_term:
            continue
        if term_is_present(normalized_comment, normalized_term):
            matches.append(
                {
                    "criterio": criterion,
                    "termo_original": term,
                    "termo_normalizado": normalized_term,
                }
            )
    return matches


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def term_is_present(normalized_comment: str, normalized_term: str) -> bool:
    if " " in normalized_term:
        return normalized_term in normalized_comment
    pattern = r"(?<![\w])" + re.escape(normalized_term) + r"(?![\w])"
    return bool(re.search(pattern, normalized_comment))


def determine_axis(
    operational: List[Dict[str, object]],
    experiential: List[Dict[str, object]],
    entities: List[Dict[str, object]],
) -> str:
    active_axes = [
        bool(operational),
        bool(experiential),
        bool(entities),
    ]
    if sum(active_axes) == 0:
        return "nao_classificado"
    if sum(active_axes) > 1:
        return "misto"
    if operational:
        return "operacional"
    if experiential:
        return "experiencial"
    return "entidade_monitorada"


def collect_criteria(*match_groups: List[Dict[str, object]]) -> str:
    criteria = []
    for group in match_groups:
        for match in group:
            criterion = str(match.get("criterio", "")).strip()
            if criterion and criterion not in criteria:
                criteria.append(criterion)
    return "; ".join(criteria) if criteria else SEM_CRITERIO


def build_justification(*match_groups: List[Dict[str, object]]) -> str:
    parts = []
    for group in match_groups:
        for match in group:
            label = str(match.get("label", "categoria"))
            item_id = str(match.get("id", ""))
            criterion = str(match.get("criterio", ""))
            evidence = str(match.get("evidencia", ""))
            if item_id and criterion and evidence:
                parts.append(f"{label} '{item_id}' por {criterion} '{evidence}'")
    if parts:
        return "; ".join(parts)
    return (
        "Nenhuma palavra-chave, expressao equivalente ou entidade monitorada "
        "dos arquivos de regras foi encontrada no comentario."
    )


def determine_status(
    axis: str,
    operational: List[Dict[str, object]],
    experiential: List[Dict[str, object]],
    entities: List[Dict[str, object]],
) -> str:
    total_matches = len(operational) + len(experiential) + len(entities)
    if axis == "nao_classificado":
        return "baixa_relevancia"
    if total_matches > 4:
        return "ambigua"
    return "relevante"


def determine_confidence(
    axis: str,
    operational: List[Dict[str, object]],
    experiential: List[Dict[str, object]],
    entities: List[Dict[str, object]],
) -> str:
    if axis == "nao_classificado":
        return "baixo"
    matches = operational + experiential + entities
    if len(matches) > 4:
        return "baixo"
    if any(match.get("criterio") == "expressao_equivalente" for match in matches):
        return "alto"
    if any(int(match.get("peso_inicial", 1)) >= 3 for match in matches):
        return "alto"
    return "medio"


def join_ids(matches: List[Dict[str, object]]) -> str:
    ids = []
    for match in matches:
        item_id = str(match.get("id", "")).strip()
        if item_id and item_id not in ids:
            ids.append(item_id)
    return "; ".join(ids) if ids else NAO_IDENTIFICADO


def build_review_sample(rows: List[Dict[str, str]], limit: int) -> List[Dict[str, str]]:
    classified = [row for row in rows if row["eixo_mercado"] != "nao_classificado"]
    unclassified = [row for row in rows if row["eixo_mercado"] == "nao_classificado"]
    sample = classified[: limit // 2] + unclassified[: limit - (limit // 2)]
    if len(sample) < limit:
        used_ids = {row["id_linha"] for row in sample}
        for row in rows:
            if row["id_linha"] not in used_ids:
                sample.append(row)
                used_ids.add(row["id_linha"])
            if len(sample) >= limit:
                break
    return sample[:limit]


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    report_path: Path,
    input_csv: Path,
    table_path: Path,
    sample_path: Path,
    lote: str,
    output_rows: List[Dict[str, str]],
    rules: Dict[str, object],
    inconsistencies: List[str],
) -> None:
    lines = [
        f"# Relatorio tecnico de classificacao Pilar 2 - {lote}",
        "",
        "## Base limpa processada",
        "",
        f"`{input_csv}`",
        "",
        "## Arquivos de regras carregados",
        "",
    ]
    for path in rules.get("arquivos_carregados", []):
        lines.append(f"- `{path}`")
    if not rules.get("entidades_monitoradas_existente"):
        lines.append("- `entidades_monitoradas.yml`: nao encontrado; campo `entidade_monitorada` preenchido como `nao_identificado` quando aplicavel.")

    lines.extend(
        [
            "",
            "## Arquivos gerados",
            "",
            f"- Tabela Pilar 2: `{table_path}`",
            f"- Amostra de revisao: `{sample_path}`",
            f"- Relatorio tecnico: `{report_path}`",
            "",
            "## Totais",
            "",
            f"- Total de linhas classificadas: {len(output_rows)}",
            f"- Comentarios nao_classificados: {count_value(output_rows, 'eixo_mercado', 'nao_classificado')}",
            "- Linhas excluidas: 0",
            "- Confirmacao: nenhuma linha foi excluida nesta etapa.",
            "",
        ]
    )
    append_counter_section(lines, "Quantidade por eixo_mercado", output_rows, "eixo_mercado")
    append_counter_section(lines, "Quantidade por categoria_operacional", output_rows, "categoria_operacional")
    append_counter_section(lines, "Quantidade por categoria_experiencial", output_rows, "categoria_experiencial")
    append_counter_section(lines, "Quantidade por entidade_monitorada", output_rows, "entidade_monitorada")
    append_counter_section(lines, "Quantidade por status_relevancia", output_rows, "status_relevancia")
    append_counter_section(lines, "Quantidade por grau_confianca", output_rows, "grau_confianca")

    lines.extend(["", "## Inconsistencias encontradas", ""])
    if inconsistencies:
        for item in inconsistencies:
            lines.append(f"- {item}")
    else:
        lines.append("- Nenhuma inconsistencia estrutural identificada.")

    lines.extend(
        [
            "",
            "## Escopo tecnico",
            "",
            "Esta saida e uma tabela estruturada de classificacao por regras. Nao contem diagnostico estrategico, analise reputacional ou conclusao interpretativa.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def append_counter_section(
    lines: List[str], title: str, rows: List[Dict[str, str]], column: str
) -> None:
    counter = split_counter(row.get(column, "") for row in rows)
    lines.extend([f"## {title}", "", "| Valor | Quantidade |", "|---|---:|"])
    if counter:
        for value, count in sorted(counter.items()):
            lines.append(f"| `{value}` | {count} |")
    else:
        lines.append("| Nenhum | 0 |")
    lines.append("")


def split_counter(values: Iterable[str]) -> Counter:
    counter: Counter = Counter()
    for value in values:
        parts = [part.strip() for part in str(value).split(";") if part.strip()]
        for part in parts:
            counter[part] += 1
    return counter


def count_value(rows: List[Dict[str, str]], column: str, target: str) -> int:
    return sum(1 for row in rows if row.get(column) == target)


def print_counter(title: str, counter: Counter) -> None:
    print(f"{title}:")
    if not counter:
        print("- nenhum: 0")
        return
    for key, count in sorted(counter.items()):
        print(f"- {key}: {count}")


if __name__ == "__main__":
    sys.exit(main())
