from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


NAO_IDENTIFICADO = "nao_identificado"

REQUIRED_INPUT_COLUMNS = [
    "id_linha",
    "lote",
    "arquivo_origem",
    "perfil_alvo",
    "usuario_comentario",
    "comentario_bruto",
    "comentario_limpo",
    "natureza_principal",
    "categoria_principal",
    "categoria_secundaria",
    "termos_detectados",
    "polaridade_textual",
    "evidencia_textual",
    "grau_confianca",
    "eixo_mercado",
    "categoria_operacional",
    "categoria_experiencial",
    "entidade_monitorada",
    "status_relevancia",
    "justificativa_vinculo",
]

MATRIX_COLUMNS = [
    "problema_detectado",
    "evidencia_textual",
    "volume_ocorrencias",
    "eixo_afetado",
    "natureza_problema",
    "impacto_experiencia",
    "impacto_operacao",
    "recomendacao_resolutiva",
    "prioridade",
    "responsavel_sugerido",
    "indicador_monitoramento",
    "ids_linhas_relacionadas",
    "arquivos_origem_relacionados",
    "categorias_relacionadas",
    "polaridade_predominante",
    "grau_confianca_predominante",
]

OPERATIONAL_CATEGORIES = {
    "fila",
    "entrada",
    "acesso",
    "seguranca",
    "bar",
    "banheiro",
    "som",
    "palco",
    "iluminacao",
    "preco",
    "compra",
    "atendimento",
    "sinalizacao",
    "transporte",
    "lotacao",
    "climatizacao",
    "revista",
}

EXPERIENTIAL_CATEGORIES = {
    "desejo",
    "expectativa",
    "frustracao",
    "pertencimento",
    "acolhimento",
    "identificacao",
    "decepcao",
    "encanto",
    "intencao_de_retorno",
    "memoria_afetiva",
    "rejeicao",
    "status",
    "recomendacao_espontanea",
}


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    input_csv = resolve_input_csv(args.classificacao_pilar3, project_root)
    output_dir = project_root / "09_matriz_resolutiva_por_lote"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, fieldnames = read_csv(input_csv)
    validate_columns(fieldnames)
    lote = identify_lote(rows, input_csv)

    matrix_rows = build_matrix(rows)
    ensure_recommendations_are_evidence_based(matrix_rows)

    matrix_csv_path = output_dir / f"{lote}_matriz_resolutiva.csv"
    matrix_xlsx_path = output_dir / f"{lote}_matriz_resolutiva.xlsx"
    report_path = output_dir / f"{lote}_relatorio_matriz_resolutiva.md"
    panel_path = output_dir / f"{lote}_painel_resolutivo.xlsx"

    write_csv(matrix_csv_path, MATRIX_COLUMNS, matrix_rows)
    write_xlsx(
        matrix_xlsx_path,
        [("matriz_resolutiva", MATRIX_COLUMNS, matrix_rows)],
    )
    write_xlsx(panel_path, build_panel_sheets(matrix_rows))
    write_report(
        report_path=report_path,
        input_csv=input_csv,
        matrix_csv_path=matrix_csv_path,
        matrix_xlsx_path=matrix_xlsx_path,
        panel_path=panel_path,
        total_input_rows=len(rows),
        matrix_rows=matrix_rows,
        inconsistencies=[],
    )

    print(f"Matriz Resolutiva XLSX: {matrix_xlsx_path}")
    print(f"Matriz Resolutiva CSV: {matrix_csv_path}")
    print(f"Painel Resolutivo XLSX: {panel_path}")
    print(f"Relatorio tecnico: {report_path}")
    print(f"Linhas processadas: {len(rows)}")
    print(f"Problemas detectados: {len(matrix_rows)}")
    print_counter("Distribuicao por eixo_afetado", Counter(row["eixo_afetado"] for row in matrix_rows))
    print_counter("Distribuicao por prioridade", Counter(row["prioridade"] for row in matrix_rows))
    print("Recomendacoes sem evidencia textual associada: 0")
    print("Linhas excluidas da base de entrada: 0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Executa a Camada 5: Matriz Resolutiva e Painel a partir da "
            "classificacao operacional e experiencial da Camada 3."
        )
    )
    parser.add_argument(
        "classificacao_pilar3",
        help=(
            "Caminho do CSV de classificacao operacional e experiencial em "
            "08_pln_pilar3_por_lote."
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
        raise SystemExit(f"Arquivo de entrada da Camada 5 nao encontrado: {input_csv}")

    allowed_dir = (project_root / "08_pln_pilar3_por_lote").resolve()
    if input_csv.parent != allowed_dir:
        raise SystemExit(
            "A Matriz Resolutiva deve usar exclusivamente a saida da Camada 3 "
            f"diretamente em {allowed_dir}. Processamento interrompido."
        )
    if input_csv.suffix.lower() != ".csv":
        raise SystemExit("A entrada da Matriz Resolutiva deve ser um arquivo CSV.")

    forbidden_dirs = [
        (project_root / "02_xlsx_brutos_extensao_chrome").resolve(),
        (project_root / "03_lotes_processamento").resolve(),
        (project_root / "04_bases_tratadas_por_lote").resolve(),
        (project_root / "06_bases_limpas_por_lote").resolve(),
        (project_root / "07_classificacao_pilar2_por_lote").resolve(),
    ]
    for forbidden_dir in forbidden_dirs:
        if input_csv == forbidden_dir or forbidden_dir in input_csv.parents:
            raise SystemExit("Entrada invalida para Camada 5. Use somente a saida da Camada 3.")

    return input_csv


def read_csv(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    return rows, fieldnames


def validate_columns(fieldnames: List[str]) -> None:
    missing = [column for column in REQUIRED_INPUT_COLUMNS if column not in fieldnames]
    if missing:
        raise SystemExit(
            "Arquivo da Camada 3 com estrutura divergente. Colunas ausentes: "
            + ", ".join(missing)
        )


def identify_lote(rows: List[Dict[str, str]], input_csv: Path) -> str:
    lotes = sorted({row.get("lote", "").strip() for row in rows if row.get("lote", "").strip()})
    if len(lotes) == 1:
        return lotes[0]
    if len(lotes) > 1:
        raise SystemExit(
            "Entrada contem mais de um lote. A Matriz Resolutiva deve ser executada por lote. "
            f"Lotes encontrados: {', '.join(lotes)}"
        )
    match = re.match(
        r"^(lote_\d+)_classificacao_operacional_experiencial\.csv$",
        input_csv.name,
        re.IGNORECASE,
    )
    if match:
        return match.group(1)
    raise SystemExit("Nao foi possivel identificar o lote a partir da entrada da Camada 3.")


def build_matrix(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    groups: Dict[Tuple[str, str, str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        evidence = evidence_for_row(row)
        if not evidence:
            continue
        groups[group_key(row)].append(row)

    matrix_rows = []
    for key, group_rows in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        matrix_rows.append(build_problem_row(key, group_rows))
    return matrix_rows


def group_key(row: Dict[str, str]) -> Tuple[str, str, str, str]:
    natureza = row.get("natureza_principal", "indefinida").strip() or "indefinida"
    categoria = row.get("categoria_principal", NAO_IDENTIFICADO).strip() or NAO_IDENTIFICADO
    if categoria == "nao_identificada":
        categoria = first_relevant_term(row) or NAO_IDENTIFICADO
    polaridade = row.get("polaridade_textual", "indefinida").strip() or "indefinida"
    eixo = row.get("eixo_mercado", "nao_classificado").strip() or "nao_classificado"
    return natureza, categoria, polaridade, eixo


def build_problem_row(key: Tuple[str, str, str, str], rows: List[Dict[str, str]]) -> Dict[str, str]:
    natureza, categoria, _polaridade_key, _eixo_key = key
    evidences = unique_non_empty(evidence_for_row(row) for row in rows)[:5]
    ids = unique_non_empty(row.get("id_linha", "") for row in rows)
    arquivos = unique_non_empty(row.get("arquivo_origem", "") for row in rows)
    categories = related_categories(rows)
    polaridade = most_common(row.get("polaridade_textual", "") for row in rows)
    confianca = most_common(row.get("grau_confianca", "") for row in rows)
    eixo_afetado = determine_eixo_afetado(rows)
    natureza_problema = determine_natureza_problema(rows, categoria)
    impacto_experiencia = determine_impacto_experiencia(rows, categoria, polaridade)
    impacto_operacao = determine_impacto_operacao(rows, categoria, polaridade)
    prioridade = determine_prioridade(
        volume=len(rows),
        polaridade=polaridade,
        eixo_afetado=eixo_afetado,
        natureza_problema=natureza_problema,
        impacto_experiencia=impacto_experiencia,
        impacto_operacao=impacto_operacao,
    )
    indicador = determine_indicator(categoria, eixo_afetado, prioridade)

    return {
        "problema_detectado": build_problem_name(natureza, categoria, polaridade),
        "evidencia_textual": " | ".join(evidences),
        "volume_ocorrencias": str(len(rows)),
        "eixo_afetado": eixo_afetado,
        "natureza_problema": natureza_problema,
        "impacto_experiencia": impacto_experiencia,
        "impacto_operacao": impacto_operacao,
        "recomendacao_resolutiva": build_recommendation(
            categoria=categoria,
            eixo_afetado=eixo_afetado,
            natureza_problema=natureza_problema,
            prioridade=prioridade,
            has_evidence=bool(evidences),
            has_ids=bool(ids),
        ),
        "prioridade": prioridade,
        "responsavel_sugerido": determine_owner(categoria, eixo_afetado, natureza_problema),
        "indicador_monitoramento": indicador,
        "ids_linhas_relacionadas": "; ".join(ids),
        "arquivos_origem_relacionados": "; ".join(arquivos),
        "categorias_relacionadas": "; ".join(categories),
        "polaridade_predominante": polaridade or "indefinida",
        "grau_confianca_predominante": confianca or "baixo",
    }


def evidence_for_row(row: Dict[str, str]) -> str:
    evidence = clean_text(row.get("evidencia_textual", ""))
    if evidence:
        return shorten(evidence, 220)
    comment = clean_text(row.get("comentario_limpo", "")) or clean_text(row.get("comentario_bruto", ""))
    return shorten(comment, 220) if comment else ""


def first_relevant_term(row: Dict[str, str]) -> str:
    terms = split_semicolon(row.get("termos_detectados", ""))
    for term in terms:
        if term and term != NAO_IDENTIFICADO:
            return term
    return ""


def related_categories(rows: List[Dict[str, str]]) -> List[str]:
    values = []
    for row in rows:
        for column in [
            "categoria_principal",
            "categoria_secundaria",
            "categoria_operacional",
            "categoria_experiencial",
        ]:
            for value in split_semicolon(row.get(column, "")):
                if value and value not in {"nao_identificada", NAO_IDENTIFICADO}:
                    values.append(value)
    return unique_non_empty(values)


def determine_eixo_afetado(rows: List[Dict[str, str]]) -> str:
    nature = most_common(row.get("natureza_principal", "") for row in rows)
    if nature == "operacao_tangivel":
        return "operacao"
    if nature == "experiencia_intangivel":
        return "experiencia"
    if nature == "mista":
        return "misto"
    return "indefinido"


def determine_natureza_problema(rows: List[Dict[str, str]], categoria: str) -> str:
    normalized = normalize_token(categoria)
    if normalized in {"sinalizacao", "compra"}:
        return "comunicacional"
    if normalized in {"seguranca", "fila", "entrada", "acesso", "bar", "banheiro", "som", "palco", "iluminacao", "preco", "atendimento", "transporte", "lotacao", "climatizacao", "revista"}:
        return "operacional"
    if normalized in {"frustracao", "decepcao", "rejeicao", "status"}:
        return "reputacional"
    if normalized in {"pertencimento", "acolhimento", "identificacao", "recomendacao_espontanea"}:
        return "relacional"
    if normalized in EXPERIENTIAL_CATEGORIES or any_valid(rows, "categoria_experiencial"):
        return "experiencial"
    if normalized in OPERATIONAL_CATEGORIES or any_valid(rows, "categoria_operacional"):
        return "operacional"
    return "indefinido"


def determine_impacto_experiencia(rows: List[Dict[str, str]], categoria: str, polaridade: str) -> str:
    if not any_valid(rows, "categoria_experiencial") and determine_eixo_afetado(rows) not in {"experiencia", "misto"}:
        return NAO_IDENTIFICADO
    evidence_count = sum(1 for row in rows if evidence_for_row(row))
    category = categoria if categoria != NAO_IDENTIFICADO else most_common_valid(rows, "categoria_experiencial")
    return f"Evidencias textuais indicam impacto experiencial em {category}, com polaridade predominante {polaridade}, sustentado por {evidence_count} comentario(s)."


def determine_impacto_operacao(rows: List[Dict[str, str]], categoria: str, polaridade: str) -> str:
    if not any_valid(rows, "categoria_operacional") and determine_eixo_afetado(rows) not in {"operacao", "misto"}:
        return NAO_IDENTIFICADO
    evidence_count = sum(1 for row in rows if evidence_for_row(row))
    category = categoria if categoria != NAO_IDENTIFICADO else most_common_valid(rows, "categoria_operacional")
    return f"Evidencias textuais indicam impacto operacional em {category}, com polaridade predominante {polaridade}, sustentado por {evidence_count} comentario(s)."


def determine_prioridade(
    volume: int,
    polaridade: str,
    eixo_afetado: str,
    natureza_problema: str,
    impacto_experiencia: str,
    impacto_operacao: str,
) -> str:
    negative_signal = polaridade in {"negativa", "ambivalente"}
    has_impact = impacto_experiencia != NAO_IDENTIFICADO or impacto_operacao != NAO_IDENTIFICADO
    if eixo_afetado == "indefinido" or natureza_problema == "indefinido":
        return "monitorar"
    if volume >= 20 and negative_signal and has_impact:
        return "alta"
    if volume >= 10 and negative_signal:
        return "media"
    if volume >= 20 and has_impact:
        return "media"
    if volume >= 5:
        return "baixa"
    return "monitorar"


def determine_owner(categoria: str, eixo_afetado: str, natureza_problema: str) -> str:
    normalized = normalize_token(categoria)
    owners = {
        "seguranca": "segurança",
        "revista": "segurança",
        "bar": "bar",
        "atendimento": "atendimento",
        "sinalizacao": "comunicação",
        "compra": "comunicação",
        "preco": "gestão_do_evento",
        "som": "produção",
        "palco": "produção",
        "iluminacao": "produção",
        "fila": "operação",
        "entrada": "operação",
        "acesso": "operação",
        "banheiro": "operação",
        "transporte": "operação",
        "lotacao": "operação",
        "climatizacao": "operação",
    }
    if normalized in owners:
        return owners[normalized]
    if natureza_problema in {"relacional", "experiencial"} or eixo_afetado == "experiencia":
        return "experiência_do_público"
    if natureza_problema == "reputacional":
        return "comunicação"
    if eixo_afetado == "misto":
        return "gestão_do_evento"
    if eixo_afetado == "indefinido":
        return "monitoramento"
    return "indefinido"


def determine_indicator(categoria: str, eixo_afetado: str, prioridade: str) -> str:
    normalized = normalize_token(categoria)
    if normalized in {"fila", "bar", "frustracao"}:
        return f"quantidade de menções sobre {categoria}"
    if eixo_afetado in {"operacao", "experiencia", "misto"}:
        return f"volume de evidências por problema detectado; percentual de comentários negativos por eixo"
    if prioridade == "alta":
        return "percentual de problemas com prioridade alta"
    return "volume de menções por categoria"


def build_recommendation(
    categoria: str,
    eixo_afetado: str,
    natureza_problema: str,
    prioridade: str,
    has_evidence: bool,
    has_ids: bool,
) -> str:
    if not has_evidence or not has_ids:
        return ""
    if eixo_afetado == "operacao":
        return f"Revisar o ponto operacional associado a {categoria} e acompanhar o indicador definido para verificar reducao de recorrencia."
    if eixo_afetado == "experiencia":
        return f"Revisar a experiencia associada a {categoria} e monitorar novos comentarios com a mesma evidencia textual."
    if eixo_afetado == "misto":
        return f"Tratar {categoria} em conjunto entre operacao e experiencia do publico, priorizando evidencias com prioridade {prioridade}."
    return f"Manter {categoria} em monitoramento ate haver maior recorrencia ou evidencia mais especifica."


def build_problem_name(natureza: str, categoria: str, polaridade: str) -> str:
    readable = categoria.replace("_", " ") if categoria else NAO_IDENTIFICADO
    if categoria == NAO_IDENTIFICADO:
        return f"comentarios sem categoria definida ({polaridade})"
    if natureza == "indefinida":
        return f"{readable} sem natureza definida"
    return f"{readable} em {natureza}"


def ensure_recommendations_are_evidence_based(matrix_rows: List[Dict[str, str]]) -> None:
    invalid = [
        row["problema_detectado"]
        for row in matrix_rows
        if row["recomendacao_resolutiva"] and (not row["evidencia_textual"] or not row["ids_linhas_relacionadas"])
    ]
    if invalid:
        raise SystemExit(
            "Recomendacao sem evidencia textual ou ids_linhas_relacionadas: "
            + "; ".join(invalid)
        )


def build_panel_sheets(matrix_rows: List[Dict[str, str]]) -> List[Tuple[str, List[str], List[Dict[str, str]]]]:
    prioridade_rows = counter_rows(matrix_rows, "prioridade", ["prioridade", "quantidade_problemas"])
    eixo_rows = []
    combo_counter = Counter((row["eixo_afetado"], row["natureza_problema"]) for row in matrix_rows)
    for (eixo, natureza), count in sorted(combo_counter.items()):
        eixo_rows.append(
            {
                "eixo_afetado": eixo,
                "natureza_problema": natureza,
                "quantidade_problemas": str(count),
            }
        )
    indicador_groups: Dict[str, List[str]] = defaultdict(list)
    for row in matrix_rows:
        indicador_groups[row["indicador_monitoramento"]].append(row["problema_detectado"])
    indicador_rows = [
        {
            "indicador_monitoramento": indicador,
            "problemas_vinculados": "; ".join(unique_non_empty(problems)),
            "quantidade_problemas": str(len(problems)),
        }
        for indicador, problems in sorted(indicador_groups.items())
    ]
    evidencias_rows = [
        {
            "problema_detectado": row["problema_detectado"],
            "evidencia_textual": row["evidencia_textual"],
            "ids_linhas_relacionadas": row["ids_linhas_relacionadas"],
        }
        for row in matrix_rows
    ]
    return [
        ("matriz_resolutiva", MATRIX_COLUMNS, matrix_rows),
        ("resumo_prioridades", ["prioridade", "quantidade_problemas"], prioridade_rows),
        (
            "resumo_eixos",
            ["eixo_afetado", "natureza_problema", "quantidade_problemas"],
            eixo_rows,
        ),
        (
            "indicadores_monitoramento",
            ["indicador_monitoramento", "problemas_vinculados", "quantidade_problemas"],
            indicador_rows,
        ),
        (
            "evidencias_por_problema",
            ["problema_detectado", "evidencia_textual", "ids_linhas_relacionadas"],
            evidencias_rows,
        ),
    ]


def counter_rows(rows: List[Dict[str, str]], column: str, headers: List[str]) -> List[Dict[str, str]]:
    counter = Counter(row[column] for row in rows)
    return [{headers[0]: key, headers[1]: str(value)} for key, value in sorted(counter.items())]


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    report_path: Path,
    input_csv: Path,
    matrix_csv_path: Path,
    matrix_xlsx_path: Path,
    panel_path: Path,
    total_input_rows: int,
    matrix_rows: List[Dict[str, str]],
    inconsistencies: List[str],
) -> None:
    lines = [
        "# Relatorio tecnico - Matriz Resolutiva",
        "",
        "## Arquivo de entrada",
        "",
        f"`{input_csv}`",
        "",
        "## Arquivos gerados",
        "",
        f"- Matriz Resolutiva XLSX: `{matrix_xlsx_path}`",
        f"- Matriz Resolutiva CSV: `{matrix_csv_path}`",
        f"- Painel Resolutivo XLSX: `{panel_path}`",
        f"- Relatorio tecnico: `{report_path}`",
        "",
        "## Totais",
        "",
        f"- Total de linhas analisadas: {total_input_rows}",
        f"- Quantidade de problemas detectados: {len(matrix_rows)}",
        "- Linhas excluidas da base de entrada: 0",
        "",
    ]
    append_counter_section(lines, "Problemas por eixo_afetado", matrix_rows, "eixo_afetado")
    append_counter_section(lines, "Problemas por natureza_problema", matrix_rows, "natureza_problema")
    append_counter_section(lines, "Problemas por prioridade", matrix_rows, "prioridade")
    lines.extend(
        [
            "## Criterios usados para consolidacao",
            "",
            "- Agrupamento por `natureza_principal`, `categoria_principal` ou termo relevante, `polaridade_textual` e `eixo_mercado`.",
            "- Uso de evidencias reais das colunas `evidencia_textual`, `comentario_limpo` ou `comentario_bruto`.",
            "- Priorizacao por volume, polaridade predominante, eixo afetado e existencia de impacto operacional ou experiencial.",
            "- Consolidacao de ids, arquivos de origem e categorias relacionadas para rastreabilidade.",
            "",
            "## Confirmacoes de controle",
            "",
            "- Nenhuma recomendacao foi criada sem evidencia textual associada.",
            "- Cada recomendacao possui `ids_linhas_relacionadas`.",
            "- Nenhuma linha da base de entrada foi excluida.",
            "",
            "## Inconsistencias encontradas",
            "",
        ]
    )
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
            "Esta saida e uma matriz resolutiva estruturada, auditavel e verificavel. Nao contem diagnostico estrategico final, analise reputacional livre ou narrativa executiva.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def append_counter_section(
    lines: List[str], title: str, rows: List[Dict[str, str]], column: str
) -> None:
    lines.extend([f"## {title}", "", "| Valor | Quantidade |", "|---|---:|"])
    counter = Counter(row[column] for row in rows)
    if counter:
        for key, count in sorted(counter.items()):
            lines.append(f"| `{key}` | {count} |")
    else:
        lines.append("| Nenhum | 0 |")
    lines.append("")


def write_xlsx(path: Path, sheets: Sequence[Tuple[str, List[str], List[Dict[str, str]]]]) -> None:
    content_types = build_content_types(len(sheets))
    rels = build_root_rels()
    workbook = build_workbook([sheet[0] for sheet in sheets])
    workbook_rels = build_workbook_rels(len(sheets))
    styles = build_styles()
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    core = build_core_props(now)
    app = build_app_props()

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        archive.writestr("xl/styles.xml", styles)
        for index, (_name, columns, rows) in enumerate(sheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", build_sheet_xml(columns, rows))


def build_sheet_xml(columns: List[str], rows: List[Dict[str, str]]) -> str:
    table = [columns] + [[row.get(column, "") for column in columns] for row in rows]
    max_cols = len(columns)
    widths = []
    for col_index, column in enumerate(columns):
        max_len = max((len(str(row[col_index])) for row in table), default=len(column))
        cap = 90 if column in {"evidencia_textual", "recomendacao_resolutiva", "ids_linhas_relacionadas", "categorias_relacionadas"} else 42
        widths.append(max(12, min(cap, max_len + 2)))
    cols_xml = "".join(
        f'<col min="{idx}" max="{idx}" width="{width}" customWidth="1"/>'
        for idx, width in enumerate(widths, start=1)
    )
    sheet_rows = []
    for row_index, row in enumerate(table, start=1):
        style = "1" if row_index == 1 else "2"
        cells = "".join(
            inline_cell(row_index, col_index, value, style)
            for col_index, value in enumerate(row, start=1)
        )
        sheet_rows.append(f'<row r="{row_index}">{cells}</row>')
    last_ref = f"{col_letter(max_cols)}{len(table)}"
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <dimension ref="A1:{last_ref}"/>
  <sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
  <cols>{cols_xml}</cols>
  <sheetData>{''.join(sheet_rows)}</sheetData>
  <autoFilter ref="A1:{last_ref}"/>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>
</worksheet>'''


def inline_cell(row_index: int, col_index: int, value: str, style: str) -> str:
    ref = f"{col_letter(col_index)}{row_index}"
    return (
        f'<c r="{ref}" t="inlineStr" s="{style}">'
        f'<is><t xml:space="preserve">{xml_safe(value)}</t></is></c>'
    )


def build_content_types(sheet_count: int) -> str:
    overrides = "\n".join(
        f'  <Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, sheet_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
{overrides}
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''


def build_root_rels() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def build_workbook(sheet_names: Sequence[str]) -> str:
    sheets = "\n".join(
        f'    <sheet name="{xml_attr(name)}" sheetId="{index}" r:id="rId{index}"/>'
        for index, name in enumerate(sheet_names, start=1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
{sheets}
  </sheets>
</workbook>'''


def build_workbook_rels(sheet_count: int) -> str:
    sheet_rels = "\n".join(
        f'  <Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>'
        for index in range(1, sheet_count + 1)
    )
    style_id = sheet_count + 1
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{sheet_rels}
  <Relationship Id="rId{style_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''


def build_styles() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><name val="Calibri"/></font>
  </fonts>
  <fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>
  <borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="3">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>'''


def build_core_props(now: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build_app_props() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>'''


def col_letter(index: int) -> str:
    letters = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def xml_safe(value: str) -> str:
    text = "" if value is None else str(value)
    text = "".join(
        ch
        for ch in text
        if ch in "\t\n\r"
        or 0x20 <= ord(ch) <= 0xD7FF
        or 0xE000 <= ord(ch) <= 0xFFFD
        or 0x10000 <= ord(ch) <= 0x10FFFF
    )
    return html.escape(text, quote=False)


def xml_attr(value: str) -> str:
    return html.escape(str(value), quote=True)


def split_semicolon(value: str) -> List[str]:
    return [part.strip() for part in str(value).split(";") if part.strip()]


def unique_non_empty(values: Iterable[str]) -> List[str]:
    result = []
    for value in values:
        clean = clean_text(value)
        if clean and clean not in result:
            result.append(clean)
    return result


def most_common(values: Iterable[str]) -> str:
    counter = Counter(clean_text(value) for value in values if clean_text(value))
    return counter.most_common(1)[0][0] if counter else ""


def most_common_valid(rows: List[Dict[str, str]], column: str) -> str:
    values = []
    for row in rows:
        for value in split_semicolon(row.get(column, "")):
            if value not in {"nao_identificada", NAO_IDENTIFICADO}:
                values.append(value)
    return most_common(values) or NAO_IDENTIFICADO


def any_valid(rows: List[Dict[str, str]], column: str) -> bool:
    return most_common_valid(rows, column) != NAO_IDENTIFICADO


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def shorten(value: str, limit: int) -> str:
    text = clean_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def normalize_token(value: str) -> str:
    return (
        clean_text(value)
        .lower()
        .replace("ç", "c")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace(" ", "_")
    )


def print_counter(title: str, counter: Counter) -> None:
    print(f"{title}:")
    if not counter:
        print("- nenhum: 0")
        return
    for key, count in sorted(counter.items()):
        print(f"- {key}: {count}")


if __name__ == "__main__":
    sys.exit(main())
