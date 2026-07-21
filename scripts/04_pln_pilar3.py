from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


NAO_IDENTIFICADA = "nao_identificada"

REQUIRED_INPUT_COLUMNS = [
    "id_linha",
    "lote",
    "arquivo_origem",
    "perfil_alvo",
    "usuario_comentario",
    "comentario_bruto",
    "comentario_limpo",
    "eixo_mercado",
    "categoria_operacional",
    "categoria_experiencial",
    "entidade_monitorada",
    "status_relevancia",
    "justificativa_vinculo",
    "grau_confianca",
]

MAIN_OUTPUT_COLUMNS = [
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

TERM_FREQUENCY_COLUMNS = [
    "termo",
    "frequencia",
    "quantidade_comentarios",
    "natureza_associada_predominante",
    "categoria_associada_predominante",
]

TOPIC_COLUMNS = [
    "topico",
    "natureza_principal",
    "categoria_principal",
    "termos_associados",
    "quantidade_comentarios",
    "exemplos_evidencia_textual",
    "grau_recorrencia",
]

POSITIVE_TERMS = {
    "adorei",
    "amei",
    "bom",
    "boa",
    "otimo",
    "otima",
    "excelente",
    "incrivel",
    "maravilhoso",
    "maravilhosa",
    "perfeito",
    "perfeita",
    "lindo",
    "linda",
    "recomendo",
    "vale",
    "encantado",
    "encantada",
    "top",
    "massa",
}

NEGATIVE_TERMS = {
    "ruim",
    "pessimo",
    "pessima",
    "horrivel",
    "caro",
    "cara",
    "demora",
    "demorado",
    "demorada",
    "fila",
    "frustrado",
    "frustrada",
    "frustracao",
    "decepcao",
    "decepcionado",
    "decepcionada",
    "nao volto",
    "nunca mais",
    "odiei",
    "problema",
    "confuso",
    "confusa",
    "lotado",
    "lotada",
    "sujo",
    "suja",
}

STOPWORDS = {
    "a",
    "o",
    "os",
    "as",
    "um",
    "uma",
    "uns",
    "umas",
    "de",
    "do",
    "da",
    "dos",
    "das",
    "em",
    "no",
    "na",
    "nos",
    "nas",
    "por",
    "para",
    "pra",
    "pro",
    "com",
    "sem",
    "sobre",
    "entre",
    "e",
    "ou",
    "mas",
    "que",
    "se",
    "eu",
    "tu",
    "ele",
    "ela",
    "nos",
    "voces",
    "eles",
    "elas",
    "me",
    "te",
    "se",
    "foi",
    "ser",
    "ter",
    "tem",
    "tinha",
    "estar",
    "estava",
    "estavam",
    "muito",
    "muita",
    "muitos",
    "muitas",
    "mais",
    "menos",
    "isso",
    "esse",
    "essa",
    "esses",
    "essas",
    "aquele",
    "aquela",
    "ali",
    "la",
    "ja",
    "tambem",
    "so",
    "sao",
    "era",
    "como",
    "quando",
    "onde",
    "porque",
    "por que",
    "nao",
    "sim",
}


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    input_csv = resolve_input_csv(args.tabela_pilar2, project_root)
    output_dir = project_root / "08_pln_pilar3_por_lote"
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, fieldnames = read_csv(input_csv)
    validate_input_columns(fieldnames)
    lote = identify_lote(rows, input_csv)

    refined_rows = build_refined_rows(rows)
    if len(refined_rows) != len(rows):
        raise SystemExit("Falha de controle: a Camada 3 nao preservou todas as linhas.")

    term_rows = build_term_frequency_rows(refined_rows)
    topic_rows = build_topic_rows(refined_rows)

    frequency_path = output_dir / f"{lote}_frequencia_termos.csv"
    topics_path = output_dir / f"{lote}_topicos_recorrentes.csv"
    refined_path = output_dir / f"{lote}_classificacao_operacional_experiencial.csv"
    report_path = output_dir / f"{lote}_relatorio_pln_pilar3.md"

    write_csv(frequency_path, TERM_FREQUENCY_COLUMNS, term_rows)
    write_csv(topics_path, TOPIC_COLUMNS, topic_rows)
    write_csv(refined_path, MAIN_OUTPUT_COLUMNS, refined_rows)
    write_report(
        report_path=report_path,
        input_csv=input_csv,
        frequency_path=frequency_path,
        topics_path=topics_path,
        refined_path=refined_path,
        refined_rows=refined_rows,
        term_rows=term_rows,
        topic_rows=topic_rows,
        inconsistencies=[],
    )

    print(f"Frequencia de termos: {frequency_path}")
    print(f"Topicos recorrentes: {topics_path}")
    print(f"Classificacao operacional e experiencial: {refined_path}")
    print(f"Relatorio tecnico: {report_path}")
    print(f"Linhas processadas: {len(refined_rows)}")
    print_counter("Distribuicao por natureza_principal", Counter(row["natureza_principal"] for row in refined_rows))
    print_counter("Distribuicao por polaridade_textual", Counter(row["polaridade_textual"] for row in refined_rows))
    print(f"Comentarios indefinidos: {count_value(refined_rows, 'natureza_principal', 'indefinida')}")
    print("Linhas excluidas: 0")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Executa a Camada 3: PLN, separacao analitica e refinamento tecnico "
            "sobre uma tabela Pilar 2 por lote."
        )
    )
    parser.add_argument(
        "tabela_pilar2",
        help=(
            "Caminho de uma tabela Pilar 2 em 07_classificacao_pilar2_por_lote, "
            "por exemplo 07_classificacao_pilar2_por_lote/lote_01_tabela_pilar2.csv."
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
        raise SystemExit(f"Tabela Pilar 2 de entrada nao encontrada: {input_csv}")

    allowed_dir = (project_root / "07_classificacao_pilar2_por_lote").resolve()
    if input_csv.parent != allowed_dir:
        raise SystemExit(
            "A Camada 3 deve usar exclusivamente tabelas Pilar 2 diretamente em "
            f"{allowed_dir}. Processamento interrompido."
        )

    forbidden_dirs = [
        (project_root / "02_xlsx_brutos_extensao_chrome").resolve(),
        (project_root / "03_lotes_processamento").resolve(),
        (project_root / "04_bases_tratadas_por_lote").resolve(),
        (project_root / "06_bases_limpas_por_lote").resolve(),
    ]
    for forbidden_dir in forbidden_dirs:
        if input_csv == forbidden_dir or forbidden_dir in input_csv.parents:
            raise SystemExit("Entrada invalida para Camada 3. Use somente a tabela Pilar 2.")

    if input_csv.suffix.lower() != ".csv":
        raise SystemExit("A entrada da Camada 3 deve ser um arquivo CSV.")
    return input_csv


def read_csv(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    return rows, fieldnames


def validate_input_columns(fieldnames: List[str]) -> None:
    missing = [column for column in REQUIRED_INPUT_COLUMNS if column not in fieldnames]
    if missing:
        raise SystemExit(
            "Tabela Pilar 2 com estrutura divergente. Colunas ausentes: "
            + ", ".join(missing)
        )


def identify_lote(rows: List[Dict[str, str]], input_csv: Path) -> str:
    lotes = sorted({row.get("lote", "").strip() for row in rows if row.get("lote", "").strip()})
    if len(lotes) == 1:
        return lotes[0]
    if len(lotes) > 1:
        raise SystemExit(
            "Tabela Pilar 2 contem mais de um lote. A Camada 3 deve ser executada por lote. "
            f"Lotes encontrados: {', '.join(lotes)}"
        )

    match = re.match(r"^(lote_\d+)_tabela_pilar2\.csv$", input_csv.name, re.IGNORECASE)
    if match:
        return match.group(1)
    raise SystemExit("Nao foi possivel identificar o lote a partir da tabela Pilar 2.")


def build_refined_rows(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    refined_rows = []
    for row in rows:
        comentario_bruto = row.get("comentario_bruto", "")
        comentario_limpo = row.get("comentario_limpo", "").strip()
        if not comentario_limpo:
            comentario_limpo = clean_comment_for_pln(comentario_bruto)

        operacional = split_semicolon(row.get("categoria_operacional", ""))
        experiencial = split_semicolon(row.get("categoria_experiencial", ""))
        entidade = split_semicolon(row.get("entidade_monitorada", ""))
        operacional_valid = [item for item in operacional if item != "nao_identificado"]
        experiencial_valid = [item for item in experiencial if item != "nao_identificado"]
        entidade_valid = [item for item in entidade if item != "nao_identificado"]

        natureza = determine_natureza(operacional_valid, experiencial_valid)
        categoria_principal, categoria_secundaria = determine_categories(
            natureza, operacional_valid, experiencial_valid
        )
        if natureza == "indefinida":
            categoria_principal = NAO_IDENTIFICADA
            categoria_secundaria = NAO_IDENTIFICADA

        terms_detected = detect_terms(
            comentario_limpo=comentario_limpo,
            justificativa=row.get("justificativa_vinculo", ""),
            categorias=operacional_valid + experiencial_valid + entidade_valid,
        )
        polaridade, polarity_evidence = infer_polarity(comentario_limpo)
        evidence = build_evidence_text(
            comentario_limpo=comentario_limpo,
            terms_detected=terms_detected,
            polarity_evidence=polarity_evidence,
        )

        confidence = normalize_confidence(row.get("grau_confianca", ""))
        if natureza == "indefinida" and polaridade == "indefinida":
            confidence = "baixo"

        refined_rows.append(
            {
                "id_linha": row.get("id_linha", ""),
                "lote": row.get("lote", ""),
                "arquivo_origem": row.get("arquivo_origem", ""),
                "perfil_alvo": row.get("perfil_alvo", ""),
                "usuario_comentario": row.get("usuario_comentario", ""),
                "comentario_bruto": comentario_bruto,
                "comentario_limpo": comentario_limpo,
                "natureza_principal": natureza,
                "categoria_principal": categoria_principal,
                "categoria_secundaria": categoria_secundaria,
                "termos_detectados": "; ".join(terms_detected),
                "polaridade_textual": polaridade,
                "evidencia_textual": evidence,
                "grau_confianca": confidence,
                "eixo_mercado": row.get("eixo_mercado", ""),
                "categoria_operacional": row.get("categoria_operacional", ""),
                "categoria_experiencial": row.get("categoria_experiencial", ""),
                "entidade_monitorada": row.get("entidade_monitorada", ""),
                "status_relevancia": row.get("status_relevancia", ""),
                "justificativa_vinculo": row.get("justificativa_vinculo", ""),
            }
        )
    return refined_rows


def clean_comment_for_pln(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def split_semicolon(value: str) -> List[str]:
    parts = [part.strip() for part in str(value).split(";") if part.strip()]
    return [part for part in parts if part]


def determine_natureza(operacional: List[str], experiencial: List[str]) -> str:
    has_operational = bool(operacional)
    has_experiential = bool(experiencial)
    if has_operational and has_experiential:
        return "mista"
    if has_operational:
        return "operacao_tangivel"
    if has_experiential:
        return "experiencia_intangivel"
    return "indefinida"


def determine_categories(
    natureza: str, operacional: List[str], experiencial: List[str]
) -> Tuple[str, str]:
    if natureza == "operacao_tangivel":
        return first_or_default(operacional), second_or_default(operacional)
    if natureza == "experiencia_intangivel":
        return first_or_default(experiencial), second_or_default(experiencial)
    if natureza == "mista":
        principal = first_or_default(operacional) if operacional else first_or_default(experiencial)
        secundaria = first_or_default(experiencial) if experiencial else second_or_default(operacional)
        return principal, secundaria
    return NAO_IDENTIFICADA, NAO_IDENTIFICADA


def first_or_default(values: List[str]) -> str:
    return values[0] if values else NAO_IDENTIFICADA


def second_or_default(values: List[str]) -> str:
    return values[1] if len(values) > 1 else NAO_IDENTIFICADA


def detect_terms(
    comentario_limpo: str, justificativa: str, categorias: List[str]
) -> List[str]:
    terms: List[str] = []
    for quoted in re.findall(r"'([^']+)'", justificativa):
        append_unique(terms, quoted)
    for category in categorias:
        if category and category != "nao_identificado":
            normalized_comment = normalize_text(comentario_limpo)
            normalized_category = normalize_text(category.replace("_", " "))
            if normalized_category and normalized_category in normalized_comment:
                append_unique(terms, category.replace("_", " "))
    for token in tokenize(comentario_limpo):
        if len(terms) >= 12:
            break
        append_unique(terms, token)
    return terms


def append_unique(values: List[str], value: str) -> None:
    clean_value = str(value).strip()
    if clean_value and clean_value not in values:
        values.append(clean_value)


def infer_polarity(comentario_limpo: str) -> Tuple[str, List[str]]:
    normalized = normalize_text(comentario_limpo)
    positive = find_lexical_matches(normalized, POSITIVE_TERMS)
    negative = find_lexical_matches(normalized, NEGATIVE_TERMS)

    if positive and negative:
        return "ambivalente", positive[:2] + negative[:2]
    if positive:
        return "positiva", positive[:3]
    if negative:
        return "negativa", negative[:3]
    if normalized:
        return "neutra", []
    return "indefinida", []


def find_lexical_matches(normalized_text: str, lexicon: Set[str]) -> List[str]:
    matches = []
    for term in sorted(lexicon, key=lambda item: (-len(item), item)):
        normalized_term = normalize_text(term)
        if not normalized_term:
            continue
        if " " in normalized_term:
            found = normalized_term in normalized_text
        else:
            found = bool(re.search(r"(?<![\w])" + re.escape(normalized_term) + r"(?![\w])", normalized_text))
        if found:
            matches.append(term)
    return matches


def build_evidence_text(
    comentario_limpo: str, terms_detected: List[str], polarity_evidence: List[str]
) -> str:
    evidence_terms = terms_detected + polarity_evidence
    for term in evidence_terms:
        snippet = extract_snippet(comentario_limpo, term)
        if snippet:
            return snippet
    return ""


def extract_snippet(text: str, term: str, window: int = 80) -> str:
    if not text or not term:
        return ""
    normalized_text = normalize_text(text)
    normalized_term = normalize_text(term)
    index = normalized_text.find(normalized_term)
    if index < 0:
        return ""
    start = max(0, index - window // 2)
    end = min(len(text), index + len(term) + window // 2)
    return re.sub(r"\s+", " ", text[start:end]).strip()


def normalize_confidence(value: str) -> str:
    normalized = normalize_text(value)
    if normalized in {"alto", "medio", "baixo"}:
        return normalized
    return "baixo"


def build_term_frequency_rows(refined_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    term_frequency: Counter = Counter()
    term_comment_ids: Dict[str, Set[str]] = defaultdict(set)
    term_nature: Dict[str, Counter] = defaultdict(Counter)
    term_category: Dict[str, Counter] = defaultdict(Counter)

    for row in refined_rows:
        tokens = tokenize(row.get("comentario_limpo", ""))
        for token in tokens:
            term_frequency[token] += 1
            term_comment_ids[token].add(row.get("id_linha", ""))
            term_nature[token][row.get("natureza_principal", "indefinida")] += 1
            term_category[token][row.get("categoria_principal", NAO_IDENTIFICADA)] += 1

    output = []
    for term, frequency in term_frequency.most_common():
        output.append(
            {
                "termo": term,
                "frequencia": str(frequency),
                "quantidade_comentarios": str(len(term_comment_ids[term])),
                "natureza_associada_predominante": most_common_value(term_nature[term]),
                "categoria_associada_predominante": most_common_value(term_category[term]),
            }
        )
    return output


def build_topic_rows(refined_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    grouped: Dict[Tuple[str, str], List[Dict[str, str]]] = defaultdict(list)
    for row in refined_rows:
        category = row.get("categoria_principal", NAO_IDENTIFICADA)
        nature = row.get("natureza_principal", "indefinida")
        topic_key = (nature, category)
        grouped[topic_key].append(row)

    output = []
    for (nature, category), rows in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        if category == NAO_IDENTIFICADA and nature == "indefinida":
            topic = "indefinido"
        else:
            topic = category
        associated_terms = top_terms_for_rows(rows, limit=10)
        examples = [row.get("evidencia_textual", "") for row in rows if row.get("evidencia_textual", "")]
        output.append(
            {
                "topico": topic,
                "natureza_principal": nature,
                "categoria_principal": category,
                "termos_associados": "; ".join(associated_terms),
                "quantidade_comentarios": str(len(rows)),
                "exemplos_evidencia_textual": " | ".join(examples[:3]),
                "grau_recorrencia": recurrence_degree(len(rows)),
            }
        )
    return output


def top_terms_for_rows(rows: List[Dict[str, str]], limit: int) -> List[str]:
    counter: Counter = Counter()
    for row in rows:
        counter.update(tokenize(row.get("comentario_limpo", "")))
    return [term for term, _count in counter.most_common(limit)]


def recurrence_degree(count: int) -> str:
    if count >= 20:
        return "alto"
    if count >= 5:
        return "medio"
    return "baixo"


def tokenize(text: str) -> List[str]:
    text = re.sub(r"https?://\S+|www\.\S+", " ", text, flags=re.IGNORECASE)
    raw_tokens = re.findall(r"[@#]?\w[\w.-]*", text, flags=re.UNICODE)
    tokens = []
    for token in raw_tokens:
        if token.startswith("@"):
            continue
        token = token.lstrip("#")
        normalized = normalize_text(token)
        if not normalized or len(normalized) <= 1:
            continue
        if normalized in STOPWORDS:
            continue
        if normalized.isdigit():
            continue
        tokens.append(normalized)
    return tokens


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.lower()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def most_common_value(counter: Counter) -> str:
    if not counter:
        return NAO_IDENTIFICADA
    return counter.most_common(1)[0][0]


def write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_report(
    report_path: Path,
    input_csv: Path,
    frequency_path: Path,
    topics_path: Path,
    refined_path: Path,
    refined_rows: List[Dict[str, str]],
    term_rows: List[Dict[str, str]],
    topic_rows: List[Dict[str, str]],
    inconsistencies: List[str],
) -> None:
    lines = [
        "# Relatorio tecnico PLN Pilar 3",
        "",
        "## Arquivo de entrada",
        "",
        f"`{input_csv}`",
        "",
        "## Arquivos gerados",
        "",
        f"- Frequencia de termos: `{frequency_path}`",
        f"- Topicos recorrentes: `{topics_path}`",
        f"- Classificacao operacional e experiencial: `{refined_path}`",
        f"- Relatorio tecnico: `{report_path}`",
        "",
        "## Totais",
        "",
        f"- Total de linhas processadas: {len(refined_rows)}",
        f"- Total de termos unicos identificados: {len(term_rows)}",
        f"- Comentarios indefinidos: {count_value(refined_rows, 'natureza_principal', 'indefinida')}",
        "- Linhas excluidas: 0",
        "- Confirmacao: nenhuma linha foi excluida nesta etapa.",
        "",
    ]
    append_counter_section(lines, "Quantidade por natureza_principal", refined_rows, "natureza_principal")
    append_counter_section(lines, "Quantidade por polaridade_textual", refined_rows, "polaridade_textual")
    append_counter_section(lines, "Quantidade por categoria_principal", refined_rows, "categoria_principal")
    append_counter_section(lines, "Quantidade por grau_confianca", refined_rows, "grau_confianca")

    lines.extend(["## Principais termos recorrentes", ""])
    if term_rows:
        lines.extend(["| Termo | Frequencia | Comentarios |", "|---|---:|---:|"])
        for row in term_rows[:20]:
            lines.append(
                f"| `{row['termo']}` | {row['frequencia']} | {row['quantidade_comentarios']} |"
            )
    else:
        lines.append("- Nenhum termo identificado.")
    lines.append("")

    lines.extend(["## Principais topicos recorrentes", ""])
    if topic_rows:
        lines.extend(["| Topico | Natureza | Comentarios | Grau |", "|---|---|---:|---|"])
        for row in topic_rows[:20]:
            lines.append(
                f"| `{row['topico']}` | `{row['natureza_principal']}` | {row['quantidade_comentarios']} | `{row['grau_recorrencia']}` |"
            )
    else:
        lines.append("- Nenhum topico identificado.")
    lines.append("")

    lines.extend(["## Inconsistencias encontradas", ""])
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
            "Esta etapa gera processamento textual estruturado e auditavel. Nao contem diagnostico estrategico, analise reputacional, conclusao interpretativa ou recomendacao de acao.",
            "",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def append_counter_section(
    lines: List[str], title: str, rows: List[Dict[str, str]], column: str
) -> None:
    counter = Counter(row.get(column, "") for row in rows)
    lines.extend([f"## {title}", "", "| Valor | Quantidade |", "|---|---:|"])
    if counter:
        for value, count in sorted(counter.items()):
            lines.append(f"| `{value}` | {count} |")
    else:
        lines.append("| Nenhum | 0 |")
    lines.append("")


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
