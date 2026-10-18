"""Regression tests for tools/rename/normalize_names.py.

Run with:
    python -m unittest tests.test_rename_normalize
or
    python tests/test_rename_normalize.py
"""
import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "tools" / "rename"
sys.path.insert(0, str(SCRIPT_DIR))

import normalize_names  # noqa: E402


class TestParseCanonical(unittest.TestCase):
    """Pure parser tests, no filesystem."""

    def test_sp_with_number_and_year(self):
        # Official SP designation uses dots throughout, so canonical is dot.
        self.assertEqual(
            normalize_names.parse_canonical("SP-252.13330.2022"),
            ("SP", "252.13330", "2022", None),
        )

    def test_sp_with_izm(self):
        self.assertEqual(
            normalize_names.parse_canonical("SP-252.13330.2022-IZM-3"),
            ("SP", "252.13330", "2022", "IZM-3"),
        )

    def test_sp_with_rev(self):
        self.assertEqual(
            normalize_names.parse_canonical("SP-252.13330.2022-REV-3"),
            ("SP", "252.13330", "2022", "REV-3"),
        )

    def test_sp_with_trailing_description(self):
        # Description after the canonical part is accepted and ignored.
        # Number has multiple dot segments; year is the final 4-digit segment.
        self.assertEqual(
            normalize_names.parse_canonical(
                "SP-555.1325800.2025-Systema-normativnyh-dokumentov"
            ),
            ("SP", "555.1325800", "2025", None),
        )

    def test_sp_dash_before_year_is_not_canonical(self):
        # A dash between number and year deviates from the official SP
        # designation; the parser must not accept it as canonical.
        self.assertIsNone(
            normalize_names.parse_canonical("SP-252.13330-2022")
        )

    def test_sp_no_year_returns_none(self):
        # No invented year: parse fails.
        self.assertIsNone(normalize_names.parse_canonical("SP-252.13330"))

    def test_sp_no_dot_in_number_returns_none(self):
        self.assertIsNone(normalize_names.parse_canonical("SP-252-2022"))

    def test_gost_r_with_number_and_year(self):
        self.assertEqual(
            normalize_names.parse_canonical("GOST-R-21.1101-2023"),
            ("GOST-R", "21.1101", "2023", None),
        )

    def test_gost_r_no_year_returns_none(self):
        self.assertIsNone(normalize_names.parse_canonical("GOST-R-21.1101"))

    def test_gost_with_number_and_year(self):
        self.assertEqual(
            normalize_names.parse_canonical("GOST-12345-2020"),
            ("GOST", "12345", "2020", None),
        )

    def test_fz_with_number_and_year(self):
        self.assertEqual(
            normalize_names.parse_canonical("FZ-384-2009"),
            ("FZ", "384", "2009", None),
        )

    def test_fz_no_year_returns_none(self):
        self.assertIsNone(normalize_names.parse_canonical("FZ-384"))

    def test_snip(self):
        self.assertEqual(
            normalize_names.parse_canonical("SNiP-2.01.07-2020"),
            ("SNiP", "2.01.07", "2020", None),
        )

    def test_sanpin(self):
        self.assertEqual(
            normalize_names.parse_canonical("SanPiN-1.2.3-2020"),
            ("SanPiN", "1.2.3", "2020", None),
        )

    def test_unrecognized_returns_none(self):
        self.assertIsNone(normalize_names.parse_canonical("random-words-here"))


class TestParseFederalnyy(unittest.TestCase):

    def test_extracts_fz_number_no_year(self):
        self.assertEqual(
            normalize_names.parse_federalnyy(
                "Federalnyy-Zakon-ot-30.12.2009-_384_FZ-_red.-ot-25.12.2023"
            ),
            ("384", None),
        )

    def test_extracts_fz_number_with_year(self):
        self.assertEqual(
            normalize_names.parse_federalnyy(
                "Federalnyy-Zakon-ot-30.12.2009-_384_FZ-2009"
            ),
            ("384", "2009"),
        )

    def test_no_fz_token_returns_none(self):
        self.assertIsNone(
            normalize_names.parse_federalnyy("Federalnyy-Zakon-bez-FZ")
        )


class TestDetectTypePrefix(unittest.TestCase):

    def test_gost_r_comes_first(self):
        # GOST-R must be detected as GOST-R, not just GOST.
        self.assertEqual(normalize_names.detect_type_prefix("GOST-R-21.1101"), "GOST-R")
        # GOST_R (underscore) is not a canonical separator in our contract;
        # detect_type_prefix only recognizes the canonical '-'.
        self.assertEqual(normalize_names.detect_type_prefix("GOST_R-21.1101"), "GOST")

    def test_gost(self):
        self.assertEqual(normalize_names.detect_type_prefix("GOST-12345-2020"), "GOST")

    def test_sp(self):
        # detect_type_prefix only checks the leading token; it does not
        # care whether the rest is canonical.
        self.assertEqual(normalize_names.detect_type_prefix("SP-anything"), "SP")

    def test_snip(self):
        self.assertEqual(normalize_names.detect_type_prefix("SNiP-2.01.07-2020"), "SNiP")

    def test_sanpin(self):
        self.assertEqual(
            normalize_names.detect_type_prefix("SanPiN-1.2.3-2020"), "SanPiN"
        )

    def test_fz(self):
        self.assertEqual(normalize_names.detect_type_prefix("FZ-384-2009"), "FZ")

    def test_unknown_prefix(self):
        self.assertIsNone(normalize_names.detect_type_prefix("XYZ-123"))


class TestPlanRename(unittest.TestCase):
    """Per-file plan tests with a temp source folder."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.today = "2026-10-18"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _make(self, name: str) -> Path:
        p = self.tmp / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return p

    # --- already_normalized ---

    def test_sp_canonical_is_already_normalized(self):
        p = self._make("SP-252.13330.2022.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "already_normalized")
        self.assertEqual(plan["reason"], "already_normalized")
        self.assertEqual(plan["new_name"], "SP-252.13330.2022.pdf")
        self.assertEqual(plan["doc_type"], "SP")
        self.assertEqual(plan["old_name"], "SP-252.13330.2022.pdf")

    def test_gost_r_canonical_is_already_normalized(self):
        p = self._make("GOST-R-21.1101-2023.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "already_normalized")
        self.assertEqual(plan["reason"], "already_normalized")
        self.assertEqual(plan["new_name"], "GOST-R-21.1101-2023.pdf")

    def test_fz_canonical_is_already_normalized(self):
        p = self._make("FZ-384-2009.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "already_normalized")
        self.assertEqual(plan["reason"], "already_normalized")
        self.assertEqual(plan["new_name"], "FZ-384-2009.pdf")

    # --- recognized (propose rename, drop description) ---

    def test_sp_with_trailing_description_recognized(self):
        # Canonical form: SP-NUMBER.YEAR-description (dots throughout the
        # designation part).
        p = self._make("SP-555.1325800.2025-Sistema-normativnyh-dokumentov.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["reason"], "recognized")
        self.assertEqual(plan["new_name"], "SP-555.1325800.2025.pdf")
        self.assertEqual(plan["doc_type"], "SP")
        # Original name preserved in old_name.
        self.assertEqual(
            plan["old_name"],
            "SP-555.1325800.2025-Sistema-normativnyh-dokumentov.pdf",
        )

    def test_sp_with_izm_recognized(self):
        p = self._make("SP-252.13330.2022-IZM-3-extra-stuff.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["reason"], "recognized")
        self.assertEqual(plan["new_name"], "SP-252.13330.2022-IZM-3.pdf")

    def test_preservation_of_dots_year_izm(self):
        p = self._make("SP-252.13330.2022-IZM-3.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["new_name"], "SP-252.13330.2022-IZM-3.pdf")
        self.assertEqual(plan["doc_type"], "SP")

    # --- needs_review: type known but canonical name cannot be derived ---

    def test_sp_with_order_requisites_needs_review(self):
        # Per spec: do not guess the SP number or year from order requisites.
        p = self._make("SP-252-IZM-3-887pr-2024-12-20.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "skipped")
        self.assertEqual(plan["reason"], "needs_review")
        self.assertEqual(plan["doc_type"], "SP")
        # Original name preserved in both fields.
        self.assertEqual(plan["new_name"], p.name)
        self.assertEqual(plan["old_name"], p.name)

    def test_federalnyy_zakon_no_year_needs_review(self):
        p = self._make(
            "Federalnyy-Zakon-ot-30.12.2009-_384_FZ-_red.-ot-25.12.2023.pdf"
        )
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "skipped")
        self.assertEqual(plan["reason"], "needs_review")
        self.assertEqual(plan["doc_type"], "FZ")
        self.assertEqual(plan["new_name"], p.name)

    def test_federalnyy_zakon_with_year_recognized(self):
        p = self._make("Federalnyy-Zakon-ot-30.12.2009-_384_FZ-2009.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["reason"], "recognized")
        self.assertEqual(plan["new_name"], "FZ-384-2009.pdf")
        self.assertEqual(plan["doc_type"], "FZ")

    def test_no_invented_year_sp_no_year(self):
        # SP without a year must NOT be auto-completed with a guessed year.
        p = self._make("SP-252.13330.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "skipped")
        self.assertEqual(plan["reason"], "needs_review")
        self.assertEqual(plan["new_name"], p.name)

    def test_no_invented_year_gost_r_no_year(self):
        p = self._make("GOST-R-21.1101.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "skipped")
        self.assertEqual(plan["reason"], "needs_review")

    # --- unrecognized ---

    def test_unrecognized_pdf_gets_prefix(self):
        p = self._make("random-scan-2024.pdf")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "dry_run")
        self.assertEqual(plan["reason"], "unrecognized_pdf")
        self.assertEqual(plan["doc_type"], "PDF")
        self.assertTrue(plan["new_name"].startswith("PDF-2026-10-18-"))
        self.assertTrue(plan["new_name"].endswith(".pdf"))

    def test_unrecognized_ifc_keeps_ifc_prefix(self):
        p = self._make("building-001.ifc")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["doc_type"], "IFC")
        self.assertTrue(plan["new_name"].startswith("IFC-2026-10-18-"))
        self.assertTrue(plan["new_name"].endswith(".ifc"))

    def test_unrecognized_dwg_keeps_dwg_prefix(self):
        p = self._make("plan-A-001.dwg")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["doc_type"], "DWG")
        self.assertTrue(plan["new_name"].endswith(".dwg"))

    # --- F: unsupported extension first ---

    def test_unsupported_extension_empty_doc_type(self):
        p = self._make("foo.twin")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "skipped")
        self.assertEqual(plan["reason"], "unsupported_extension")
        self.assertEqual(plan["new_name"], "")
        self.assertEqual(plan["doc_type"], "")

    def test_unsupported_extension_even_if_prefix_looks_canonical(self):
        # .twin must NOT get a doc_type even though the stem starts with SP-.
        p = self._make("SP-252.13330.2022.pdf.twin")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["status"], "skipped")
        self.assertEqual(plan["reason"], "unsupported_extension")
        self.assertEqual(plan["new_name"], "")
        self.assertEqual(plan["doc_type"], "")

    def test_unsupported_extension_txt(self):
        p = self._make("notes.txt")
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["reason"], "unsupported_extension")
        self.assertEqual(plan["doc_type"], "")

    # --- A: path-based identification, forward slashes ---

    def test_relative_path_with_forward_slashes(self):
        sub = self.tmp / "sub"
        sub.mkdir()
        p = sub / "SP-252.13330.2022.pdf"
        p.touch()
        plan = normalize_names.plan_rename(p, self.tmp, self.today)
        self.assertEqual(plan["old_name"], "sub/SP-252.13330.2022.pdf")


class TestFullWorkflow(unittest.TestCase):
    """End-to-end tests with a temp source and journal CSV."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.map_path = self.tmp / "journal.csv"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _make(self, rel: str) -> Path:
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return p

    def _read_journal(self) -> list:
        with self.map_path.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    def _args(self, dry: bool):
        return ["--source", str(self.tmp), "--map", str(self.map_path)] + (
            ["--dry-run"] if dry else []
        )

    # --- Test 1: dry-run does not change files ---

    def test_dry_run_does_not_change_files(self):
        self._make("SP-252.13330.2022.pdf")
        self._make("random.pdf")

        normalize_names.run(self._args(dry=True))

        # Files unchanged.
        self.assertTrue((self.tmp / "SP-252.13330.2022.pdf").exists())
        self.assertTrue((self.tmp / "random.pdf").exists())
        # PDF-{date}-{slug}.pdf NOT yet present.
        self.assertFalse(
            any(
                p.name.startswith("PDF-2026-")
                for p in self.tmp.iterdir()
            )
        )
        # Journal has entries; SP file is already_normalized,
        # random file is dry_run.
        rows = self._read_journal()
        self.assertEqual(len(rows), 2)
        by_old = {r["old_name"]: r for r in rows}
        self.assertEqual(by_old["SP-252.13330.2022.pdf"]["status"], "already_normalized")
        self.assertEqual(by_old["SP-252.13330.2022.pdf"]["reason"], "already_normalized")
        self.assertEqual(by_old["random.pdf"]["status"], "dry_run")
        self.assertEqual(by_old["random.pdf"]["reason"], "unrecognized_pdf")

    # --- Test 2: pending examples in journal don't block real files ---

    def test_pending_in_journal_does_not_block(self):
        # First, seed journal with pending and example rows that overlap
        # the real file names that will be processed next.
        with self.map_path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=normalize_names.CSV_FIELDS)
            w.writeheader()
            w.writerow({
                "old_name": "SP-252.13330.2022.pdf",
                "new_name": "SP-252.13330.2022-IZM-3.pdf",
                "doc_type": "SP",
                "source_folder": "x",
                "status": "pending",
                "reason": "example",
            })
            w.writerow({
                "old_name": "random.pdf",
                "new_name": "PDF-2026-01-15-random.pdf",
                "doc_type": "PDF",
                "source_folder": "x",
                "status": "pending",
                "reason": "example",
            })

        self._make("SP-252.13330.2022.pdf")
        self._make("random.pdf")

        normalize_names.run(self._args(dry=True))

        rows = self._read_journal()
        # The 2 pending rows are kept; 2 new rows are added (one for each file
        # that the next run actually processes). Pending rows do NOT block
        # re-processing: the new rows are NOT marked seen.
        self.assertEqual(len(rows), 4)
        # The 2 new (non-pending) records are the actual plan output.
        new_records = [
            r for r in rows
            if r["status"] in {"dry_run", "renamed", "already_normalized",
                               "error"}
        ]
        self.assertEqual(len(new_records), 2)
        # One is already_normalized, the other is dry_run.
        statuses = sorted(r["status"] for r in new_records)
        self.assertEqual(statuses, ["already_normalized", "dry_run"])

    # --- Test 3: same names in different subfolders are independent ---

    def test_same_name_in_different_subfolders_independent(self):
        (self.tmp / "sub1").mkdir()
        (self.tmp / "sub2").mkdir()
        self._make("sub1/SP-252.13330.2022.pdf")
        self._make("sub2/SP-252.13330.2022.pdf")

        normalize_names.run(self._args(dry=False))

        # Both files were canonical and remain in place under their subfolders.
        self.assertTrue((self.tmp / "sub1" / "SP-252.13330.2022.pdf").exists())
        self.assertTrue((self.tmp / "sub2" / "SP-252.13330.2022.pdf").exists())

        rows = self._read_journal()
        rel_names = sorted(r["old_name"] for r in rows)
        self.assertEqual(
            rel_names,
            ["sub1/SP-252.13330.2022.pdf", "sub2/SP-252.13330.2022.pdf"],
        )

    # --- Test 4: preservation of dots, year, IZM ---

    def test_preservation_of_dots_year_izm(self):
        self._make("SP-252.13330.2022-IZM-3-with-extra.pdf")

        normalize_names.run(self._args(dry=False))

        self.assertTrue(
            (self.tmp / "SP-252.13330.2022-IZM-3.pdf").exists()
        )
        rows = self._read_journal()
        self.assertEqual(rows[0]["new_name"], "SP-252.13330.2022-IZM-3.pdf")
        self.assertEqual(rows[0]["doc_type"], "SP")

    # --- Test 5: order requisites removed, original kept in journal ---

    def test_order_removed_original_kept(self):
        self._make("SP-252-IZM-3-887pr-2024-12-20.pdf")

        normalize_names.run(self._args(dry=False))

        # File is not renamed.
        self.assertTrue(
            (self.tmp / "SP-252-IZM-3-887pr-2024-12-20.pdf").exists()
        )
        rows = self._read_journal()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "skipped")
        self.assertEqual(rows[0]["reason"], "needs_review")
        # Original name preserved in both old_name and new_name.
        self.assertEqual(
            rows[0]["old_name"], "SP-252-IZM-3-887pr-2024-12-20.pdf"
        )
        self.assertEqual(
            rows[0]["new_name"], "SP-252-IZM-3-887pr-2024-12-20.pdf"
        )

    # --- Test 6: absence of invented year ---

    def test_no_invented_year(self):
        # SP without year must not be auto-completed.
        self._make("SP-252.13330.pdf")

        normalize_names.run(self._args(dry=False))

        self.assertTrue((self.tmp / "SP-252.13330.pdf").exists())
        rows = self._read_journal()
        self.assertEqual(rows[0]["reason"], "needs_review")
        # new_name is the original (no invented year).
        self.assertEqual(rows[0]["new_name"], "SP-252.13330.pdf")

    # --- Test 7: preservation of GOST-R ---

    def test_preservation_of_gost_r(self):
        self._make("GOST-R-21.1101-2023.pdf")

        normalize_names.run(self._args(dry=False))

        self.assertTrue((self.tmp / "GOST-R-21.1101-2023.pdf").exists())
        rows = self._read_journal()
        self.assertEqual(rows[0]["doc_type"], "GOST-R")
        self.assertEqual(rows[0]["reason"], "already_normalized")

    # --- Test 8: collision blocks ALL renames, recorded as error ---

    def test_collision_blocks_all_renames(self):
        # Two source files would both rename to the same target.
        self._make("SP-252.13330.2022.pdf")  # already canonical, no rename
        self._make("SP-252.13330.2022-IZM-3.pdf")  # already canonical, no rename
        # Add two files that both propose SP-FOO-2022.pdf
        (self.tmp / "SP-252.13330.2022-old.pdf").touch()
        (self.tmp / "SP-252.13330.2022-newer.pdf").touch()

        normalize_names.run(self._args(dry=False))

        # Neither of the two new files was renamed.
        self.assertTrue((self.tmp / "SP-252.13330.2022-old.pdf").exists())
        self.assertTrue((self.tmp / "SP-252.13330.2022-newer.pdf").exists())
        self.assertFalse((self.tmp / "SP-252.13330.2022.pdf.twin").exists())

        rows = self._read_journal()
        colliding = [r for r in rows if r["status"] == "error"]
        self.assertEqual(len(colliding), 2)
        for r in colliding:
            self.assertEqual(r["reason"], "collision")
            self.assertEqual(r["new_name"], "")

    # --- Test 9: unsupported extension ---

    def test_unsupported_extension(self):
        self._make("foo.twin")
        self._make("notes.txt")

        normalize_names.run(self._args(dry=False))

        rows = self._read_journal()
        self.assertEqual(len(rows), 2)
        for r in rows:
            self.assertEqual(r["status"], "skipped")
            self.assertEqual(r["reason"], "unsupported_extension")
            self.assertEqual(r["new_name"], "")
            self.assertEqual(r["doc_type"], "")

    # --- Test 10: re-run does not change already-normalized files ---

    def test_rerun_keeps_normalized_files(self):
        self._make("SP-252.13330.2022.pdf")

        normalize_names.run(self._args(dry=False))
        first_rows = self._read_journal()
        self.assertEqual(len(first_rows), 1)
        self.assertEqual(first_rows[0]["reason"], "already_normalized")

        # Re-run; no new journal entry should be added for the same file.
        normalize_names.run(self._args(dry=False))
        second_rows = self._read_journal()
        self.assertEqual(len(second_rows), 1)

        # The file is still in place.
        self.assertTrue((self.tmp / "SP-252.13330.2022.pdf").exists())

    # --- Test 11: re-run after real rename does not duplicate work ---

    def test_rerun_after_real_rename_does_not_duplicate(self):
        # Use an IZM variant that does NOT collide with another file.
        self._make("SP-252.13330.2022-IZM-3-extra.pdf")

        normalize_names.run(self._args(dry=False))
        first_rows = self._read_journal()
        self.assertEqual(len(first_rows), 1)
        self.assertEqual(first_rows[0]["status"], "renamed")
        self.assertEqual(first_rows[0]["new_name"], "SP-252.13330.2022-IZM-3.pdf")
        # File was actually renamed on disk.
        self.assertTrue((self.tmp / "SP-252.13330.2022-IZM-3.pdf").exists())
        self.assertFalse(
            (self.tmp / "SP-252.13330.2022-IZM-3-extra.pdf").exists()
        )

        # Re-run: the source now contains the canonical name, which is
        # already in canonical form and gets one fresh journal row
        # (status=already_normalized). The original old_name is not
        # re-processed because the file with that name no longer exists
        # on disk.
        normalize_names.run(self._args(dry=False))
        second_rows = self._read_journal()
        self.assertEqual(len(second_rows), 2)
        # The new row corresponds to the file under its new (canonical) name.
        new_row = second_rows[1]
        self.assertEqual(new_row["old_name"], "SP-252.13330.2022-IZM-3.pdf")
        self.assertEqual(new_row["status"], "already_normalized")

    # --- Test 12: target_exists recorded as error ---

    def test_target_exists_recorded_as_error(self):
        # File A would rename to B; but B already exists in source.
        self._make("SP-252.13330.2022-with-extra.pdf")  # wants to become canonical
        self._make("SP-252.13330.2022.pdf")  # already canonical, occupies the target

        normalize_names.run(self._args(dry=False))

        # The non-canonical file is NOT renamed.
        self.assertTrue(
            (self.tmp / "SP-252.13330.2022-with-extra.pdf").exists()
        )

        rows = self._read_journal()
        # Find the row for the with-extra file.
        target_exists = [
            r for r in rows
            if r["old_name"] == "SP-252.13330.2022-with-extra.pdf"
        ]
        self.assertEqual(len(target_exists), 1)
        self.assertEqual(target_exists[0]["status"], "error")
        self.assertEqual(target_exists[0]["reason"], "target_exists")

    # --- Test 13: dry-run + real-run pipeline (already_normalized stays put) ---

    def test_dry_run_then_real_run(self):
        # No target collision: each rename target is unique.
        self._make("SP-252.13330.2022.pdf")  # already canonical
        self._make("SP-252.13330.2022-IZM-3-extra.pdf")  # wants SP-252.13330.2022-IZM-3.pdf
        self._make("foo-bar.pdf")  # wants PDF-{date}-foo-bar.pdf

        # 1. dry-run
        normalize_names.run(self._args(dry=True))
        # Files not yet changed.
        self.assertTrue(
            (self.tmp / "SP-252.13330.2022-IZM-3-extra.pdf").exists()
        )
        self.assertTrue((self.tmp / "foo-bar.pdf").exists())
        first_rows = self._read_journal()
        self.assertEqual(len(first_rows), 3)
        # All three are planned; the canonical file has status=already_normalized,
        # the others have status=dry_run.
        statuses = sorted(r["status"] for r in first_rows)
        self.assertEqual(statuses, ["already_normalized", "dry_run", "dry_run"])

        # 2. real run
        normalize_names.run(self._args(dry=False))
        # Two files were actually renamed; canonical one was untouched.
        self.assertFalse(
            (self.tmp / "SP-252.13330.2022-IZM-3-extra.pdf").exists()
        )
        self.assertFalse((self.tmp / "foo-bar.pdf").exists())
        self.assertTrue((self.tmp / "SP-252.13330.2022.pdf").exists())
        self.assertTrue(
            (self.tmp / "SP-252.13330.2022-IZM-3.pdf").exists()
        )
        self.assertTrue(
            any(p.name.startswith("PDF-2026-10-18-foo-bar")
                for p in self.tmp.iterdir())
        )
        second_rows = self._read_journal()
        # Journal grew: 2 new entries. The canonical file from run 1 is
        # already in `seen` and is not re-recorded. The two renamed files
        # appear with status=renamed under their original (pre-rename) names;
        # they would be re-recorded as already_normalized only on a third
        # run after the file system has settled under the new names.
        self.assertEqual(len(second_rows), 5)
        new_run = second_rows[3:]
        statuses = sorted(r["status"] for r in new_run)
        self.assertEqual(statuses, ["renamed", "renamed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
