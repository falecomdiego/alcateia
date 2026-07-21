from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from pipeline_mdn_v2.mdn_pipeline.classification import build_validation_sample, classify_lot
from pipeline_mdn_v2.mdn_pipeline.consolidation import consolidate
from pipeline_mdn_v2.mdn_pipeline.core import (
    PipelineError,
    load_config,
    read_csv,
    record_id,
    sha256_file,
    verify_run_manifest,
    verify_taxonomy,
)
from pipeline_mdn_v2.mdn_pipeline.ingest import ingest_lot
from pipeline_mdn_v2.mdn_pipeline.publication import build_public_candidate
from pipeline_mdn_v2.mdn_pipeline.treatment import _technical_status, clean_lot


REAL_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REAL_ROOT / "20_rodada_prospectiva_padronizada_01/config/MDN-RPP01-CONF-001-V0.1.json"
TAXONOMY = REAL_ROOT / "00_contexto_mestre/TAXONOMIA_MESTRE_MAPA_DA_NOITE_V1_1.md"
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


class CoreTests(unittest.TestCase):
    def test_default_config_is_safe_and_taxonomy_is_frozen(self) -> None:
        config, _ = load_config(DEFAULT_CONFIG)
        self.assertFalse(config["gates"]["G0_protocol"])
        self.assertEqual(verify_taxonomy(config), config["taxonomy"]["sha256"])

    def test_record_id_is_stable(self) -> None:
        self.assertEqual(
            record_id("01", "MDN-RPP01-FON-007", 2, 31),
            "MDN-RPP01-L01-F007-A02-R000031",
        )

    def test_treatment_preserves_emoji_as_non_textual(self) -> None:
        self.assertEqual(
            _technical_status("💜"),
            ("fora_classificacao_textual", "comentario_apenas_emoji_preservado"),
        )
        self.assertEqual(_technical_status("A fila demorou"), ("mantido", ""))

    def test_static_fixture_has_no_direct_identifiers(self) -> None:
        fixture_path = Path(__file__).parent / "fixtures/sample_work.csv"
        fixture = fixture_path.read_text(encoding="utf-8")
        self.assertNotIn("instagram.com", fixture.casefold())
        self.assertNotIn("http://", fixture.casefold())
        self.assertNotIn("https://", fixture.casefold())
        self.assertNotIn("@", fixture)
        rows, _ = read_csv(fixture_path)
        expected = json.loads(
            (Path(__file__).parent / "fixtures/expected_summary.json").read_text(encoding="utf-8")
        )
        statuses = [_technical_status(row["comentario_trabalho"])[0] for row in rows]
        self.assertEqual(len(rows), expected["input_rows"])
        self.assertEqual(statuses.count("mantido"), expected["kept_rows"])
        self.assertEqual(statuses.count("excluido_tecnico"), expected["technical_exclusions"])
        self.assertEqual(
            statuses.count("fora_classificacao_textual"),
            expected["outside_text_classification"],
        )


class EndToEndSyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        taxonomy_target = self.root / "00_contexto_mestre/TAXONOMIA_MESTRE_MAPA_DA_NOITE_V1_1.md"
        taxonomy_target.parent.mkdir(parents=True)
        shutil.copyfile(TAXONOMY, taxonomy_target)

        config = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"))
        config["period"] = {
            "start": "2026-07-01",
            "end": "2026-07-31",
            "timezone": "America/Sao_Paulo",
        }
        config["lots"] = ["lote_01"]
        config["gates"].update(
            {
                "G0_protocol": True,
                "G1_collection": True,
                "G2_analysis": True,
                "G3_consolidation": True,
                "G4_publication": False,
                "G5_reapplication": False,
            }
        )
        self.config_path = (
            self.root
            / "20_rodada_prospectiva_padronizada_01/config/MDN-RPP01-CONF-001-V0.1.json"
        )
        self.config_path.parent.mkdir(parents=True)
        self.config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

        self.raw_dir = (
            self.root
            / "20_rodada_prospectiva_padronizada_01/02_dados_brutos_protegidos/dados/lote_01"
        )
        self.raw_dir.mkdir(parents=True)
        self.xlsx = self.raw_dir / "fixture.xlsx"
        _write_minimal_xlsx(self.xlsx)
        file_hash = sha256_file(self.xlsx)

        controls = self.root / "20_rodada_prospectiva_padronizada_01/01_fontes_e_coleta/preenchidos"
        controls.mkdir(parents=True)
        self.sources = controls / "fontes.csv"
        _write_csv(
            self.sources,
            ["fonte_id", "status_planejado", "motivo_inclusao"],
            [
                {
                    "fonte_id": "MDN-RPP01-FON-001",
                    "status_planejado": "aprovada",
                    "motivo_inclusao": "fixture sintética de teste",
                }
            ],
        )
        self.collections = controls / "coletas.csv"
        _write_csv(
            self.collections,
            [
                "coleta_id",
                "fonte_id",
                "ferramenta",
                "versao_ferramenta",
                "resultado",
                "arquivo_gerado",
                "hash_sha256",
            ],
            [
                {
                    "coleta_id": "MDN-RPP01-COL-001",
                    "fonte_id": "MDN-RPP01-FON-001",
                    "ferramenta": "fixture",
                    "versao_ferramenta": "1",
                    "resultado": "sucesso",
                    "arquivo_gerado": self.xlsx.name,
                    "hash_sha256": file_hash,
                }
            ],
        )
        self.lot_manifest = controls / "lote.csv"
        _write_csv(
            self.lot_manifest,
            [
                "lote",
                "fonte_id",
                "coleta_id",
                "arquivo_gerado",
                "hash_sha256",
                "status_autorizacao",
                "decisao_id",
            ],
            [
                {
                    "lote": "lote_01",
                    "fonte_id": "MDN-RPP01-FON-001",
                    "coleta_id": "MDN-RPP01-COL-001",
                    "arquivo_gerado": self.xlsx.name,
                    "hash_sha256": file_hash,
                    "status_autorizacao": "autorizado",
                    "decisao_id": "MDN-RPP01-DEC-TESTE",
                }
            ],
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_synthetic_round_through_relational_consolidation(self) -> None:
        ingest_dir = ingest_lot(
            lot="lote_01",
            input_dir=self.raw_dir,
            source_inventory=self.sources,
            collection_log=self.collections,
            lot_manifest=self.lot_manifest,
            config_path=self.config_path,
            root=self.root,
            run_id="MDN-RPP01-EXE-20260716-010101",
            pseudonym_key="fixture-secret-at-least-16-bytes",
        )
        work_path = ingest_dir / "base_trabalho_pseudonimizada.csv"
        work_text = work_path.read_text(encoding="utf-8-sig")
        self.assertNotIn("pessoa_teste", work_text)
        self.assertNotIn("perfil.example", work_text)
        work_rows, _ = read_csv(work_path)
        self.assertEqual(len(work_rows), 6)

        clean_dir = clean_lot(
            lot="lote_01",
            input_csv=work_path,
            config_path=self.config_path,
            root=self.root,
            run_id="MDN-RPP01-EXE-20260716-010102",
        )
        treated_path = clean_dir / "registros_tratados.csv"
        treated, _ = read_csv(treated_path)
        self.assertEqual(len(treated), 6)
        self.assertEqual(
            sum(row["status_tratamento"] == "fora_classificacao_textual" for row in treated),
            1,
        )

        classification_dir = classify_lot(
            lot="lote_01",
            input_csv=treated_path,
            config_path=self.config_path,
            root=self.root,
            run_id="MDN-RPP01-EXE-20260716-010103",
        )
        classification_path = classification_dir / "classificacao_taxonomica.csv"
        classified, _ = read_csv(classification_path)
        self.assertEqual(len(classified), 6)
        self.assertGreaterEqual(
            sum(row["status_classificacao"] == "nao_determinado" for row in classified),
            1,
        )

        sample_dir = build_validation_sample(
            lot="lote_01",
            input_csv=classification_path,
            config_path=self.config_path,
            root=self.root,
            run_id="MDN-RPP01-EXE-20260716-010104",
        )
        sample, _ = read_csv(sample_dir / "amostra_validacao.csv")
        self.assertEqual(len(sample), 5)

        review_dir = (
            self.root
            / "20_rodada_prospectiva_padronizada_01/04_validacao_humana/preenchidos"
        )
        review_dir.mkdir(parents=True, exist_ok=True)
        reviews_path = review_dir / "reviews.csv"
        review_rows = []
        for index, row in enumerate(
            [item for item in classified if item["requer_validacao_humana"] == "true"],
            start=1,
        ):
            candidates = [value for value in row["frentes_candidatas"].split(";") if value]
            chosen = (
                "saude_seguranca_reducao_danos"
                if "saude_seguranca_reducao_danos" in candidates
                else "operacao_infraestrutura"
            )
            review_rows.append(
                {
                    "decisao_humana_id": f"MDN-RPP01-DEC-TESTE-{index:03d}",
                    "registro_id": row["registro_id"],
                    "revisor_id": "REVISOR-TESTE",
                    "decisao": "ajustada",
                    "frente_validada": chosen,
                    "justificativa": "Decisão sintética exclusiva da fixture.",
                }
            )
        _write_csv(
            reviews_path,
            [
                "decisao_humana_id",
                "registro_id",
                "revisor_id",
                "decisao",
                "frente_validada",
                "justificativa",
            ],
            review_rows,
        )
        consolidated_dir = consolidate(
            classification_files=[classification_path],
            reviews_csv=reviews_path,
            config_path=self.config_path,
            root=self.root,
            run_id="MDN-RPP01-EXE-20260716-010105",
        )
        groups, _ = read_csv(consolidated_dir / "grupos.csv")
        links, _ = read_csv(consolidated_dir / "grupo_registro.csv")
        self.assertGreaterEqual(len(groups), 1)
        self.assertEqual(
            len(links),
            sum(int(group["volume_registros"]) for group in groups),
        )
        verified = verify_run_manifest(consolidated_dir / "manifesto_execucao.json")
        self.assertGreaterEqual(verified["entradas_verificadas"], 2)
        self.assertEqual(verified["saidas_verificadas"], 6)

        with self.assertRaises(PipelineError):
            build_public_candidate(
                groups_csv=consolidated_dir / "grupos.csv",
                evidence_csv=consolidated_dir / "evidencias.csv",
                metrics_csv=Path("inexistente.csv"),
                authorization_csv=Path("inexistente.csv"),
                release_record_json=Path("inexistente.json"),
                config_path=self.config_path,
                root=self.root,
            )

        public_root = (
            self.root
            / "20_rodada_prospectiva_padronizada_01/07_publicacao_sanitizada"
        )
        public_root.mkdir(parents=True, exist_ok=True)
        largest_group = max(groups, key=lambda row: int(row["volume_registros"]))
        metrics_path = public_root / "metrics.csv"
        _write_csv(
            metrics_path,
            ["frente_taxonomica", "precisao", "n_referencia", "aprovada_publicacao"],
            [
                {
                    "frente_taxonomica": largest_group["frente_taxonomica"],
                    "precisao": "0.90",
                    "n_referencia": "10",
                    "aprovada_publicacao": "true",
                }
            ],
        )
        authorization_path = public_root / "authorization.csv"
        _write_csv(
            authorization_path,
            ["grupo_id", "uso_publico_autorizado", "decisao_humana_id", "justificativa"],
            [
                {
                    "grupo_id": largest_group["grupo_id"],
                    "uso_publico_autorizado": "true",
                    "decisao_humana_id": "MDN-RPP01-DEC-PUB-TESTE",
                    "justificativa": "Autorização sintética exclusiva da fixture.",
                }
            ],
        )
        release_path = public_root / "release.json"
        release_path.write_text(
            json.dumps(
                {
                    "round_id": "MDN-RPP01",
                    "candidate_version": "teste",
                    "approved": True,
                    "approval_date": "2026-07-16",
                    "round_owner": "RESPONSAVEL-TESTE",
                    "sanitization_owner": "RESPONSAVEL-TESTE",
                    "second_reviewer": "REVISOR-TESTE-2",
                    "source_execution_id": consolidated_dir.name,
                    "decision_id": "MDN-RPP01-DEC-LIB-TESTE",
                }
            ),
            encoding="utf-8",
        )
        enabled_config = json.loads(self.config_path.read_text(encoding="utf-8"))
        enabled_config["gates"]["G4_publication"] = True
        self.config_path.write_text(
            json.dumps(enabled_config, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        with self.assertRaises(PipelineError):
            build_public_candidate(
                groups_csv=consolidated_dir / "grupos.csv",
                evidence_csv=consolidated_dir / "evidencias.csv",
                metrics_csv=metrics_path,
                authorization_csv=authorization_path,
                release_record_json=release_path,
                config_path=self.config_path,
                root=self.root,
                run_id="MDN-RPP01-EXE-20260716-010106",
            )

        enabled_config["public_safety"]["minimum_cell_size"] = 2
        self.config_path.write_text(
            json.dumps(enabled_config, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        public_dir = build_public_candidate(
            groups_csv=consolidated_dir / "grupos.csv",
            evidence_csv=consolidated_dir / "evidencias.csv",
            metrics_csv=metrics_path,
            authorization_csv=authorization_path,
            release_record_json=release_path,
            config_path=self.config_path,
            root=self.root,
            run_id="MDN-RPP01-EXE-20260716-010107",
        )
        public_text = (public_dir / "temas_agregados_publicos.csv").read_text(encoding="utf-8-sig")
        self.assertNotIn("comentario_trabalho", public_text)
        self.assertNotIn("MDN-AUTOR-", public_text)
        self.assertNotIn("http", public_text.casefold())

    def test_taxonomy_change_blocks_execution(self) -> None:
        taxonomy_path = self.root / "00_contexto_mestre/TAXONOMIA_MESTRE_MAPA_DA_NOITE_V1_1.md"
        taxonomy_path.write_text("alterada", encoding="utf-8")
        config, _ = load_config(self.config_path, self.root)
        with self.assertRaises(PipelineError):
            verify_taxonomy(config, self.root)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _write_minimal_xlsx(path: Path) -> None:
    rows = [
        ORIGINAL_COLUMNS,
        ["1", "1", "u1", "https://avatar.example/1", "https://perfil.example/1", "pessoa_teste", "A fila na entrada estava enorme", "2026-07-01"],
        ["2", "2", "u2", "", "", "pessoa_2", "Banheiro e bar com muita demora", "2026-07-01"],
        ["3", "3", "u3", "", "", "pessoa_3", "💜", "2026-07-01"],
        ["4", "4", "u4", "", "", "pessoa_4", "Amei demais", "2026-07-01"],
        ["5", "5", "u5", "", "", "pessoa_5", "Precisamos de acesso a água e redução de danos", "2026-07-01"],
        ["6", "6", "u6", "", "", "pessoa_6", "Melhor que outra festa, mas a pista estava lotada", "2026-07-01"],
    ]
    sheet_rows = []
    for row_index, values in enumerate(rows, start=1):
        cells = []
        for column_index, value in enumerate(values, start=1):
            ref = f"{_column_letter(column_index)}{row_index}"
            escaped = (
                str(value)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escaped}</t></is></c>')
        sheet_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')
    sheet_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(sheet_rows)}</sheetData></worksheet>'
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '</Types>',
        )
        archive.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>',
        )
        archive.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Comentários" sheetId="1" r:id="rId1"/></sheets></workbook>',
        )
        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '</Relationships>',
        )
        archive.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def _column_letter(index: int) -> str:
    value = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        value = chr(65 + remainder) + value
    return value


if __name__ == "__main__":
    unittest.main()
