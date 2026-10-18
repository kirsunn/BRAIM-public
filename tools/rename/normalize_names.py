#!/usr/bin/env python3
"""Normalize normative/project filenames to ASCII naming contract.

Canonical naming contract:
  TYPE-NUMBER[-YEAR][-IZM-N | -REV-N].ext

Examples (target form):
  SP-252.13330-2022.pdf
  SP-252.13330-2022-IZM-3.pdf
  SP-252.13330-2022-REV-3.pdf
  GOST-R-21.1101-2023.pdf
  FZ-384-2009.pdf
  PDF-2026-10-18-<slug>.pdf      (unrecognized, kept unique by download date)
  IFC-2026-10-18-<slug>.ifc      (unrecognized, non-PDF keeps its type prefix)
  <original_name>                (needs_review: type detected but canonical name cannot be derived)

Rules:
- Dots inside normative number are kept.
- Year is the document's designation year, not download year and not a relevance claim.
- IZM-N is a separate change document; REV-N is a consolidated text through change N.
- Order number/date, URL, download date, relevance: metadata, not in filename.
- Full original name is preserved in the journal (CSV).
- Missing requisites are never guessed.

Behavior:
- A: identification by relative path (forward slashes in CSV).
- B, H: CSV is a journal, not an unconditional "already processed" list.
        Only status in {renamed, already_normalized} blocks re-processing.
- C, D: full number, year, and change preserved.
- E: FZ number is extracted from "Federalnyy-Zakon..._N_FZ..." patterns;
      year is taken only if it follows the FZ token in structured form.
- F: extension is checked first; unsupported extensions are skipped
      with empty doc_type and empty new_name.
- G: plan is built fully first; on any collision, NO renames start, and
      all conflicting paths land in the journal as status=error, reason=collision.

Usage:
  python normalize_names.py --source TN_DOWNLOADS --map tools/rename/doc_type_map.csv --dry-run
  python normalize_names.py --source TN_DOWNLOADS --map tools/rename/doc_type_map.csv

Safety:
- Never deletes files.
- Refuses to overwrite an existing target name.
- Skips hidden files, __pycache__, the script, and the map itself.
- Re-runnable: dry_run, pending, error, needs_review records do not block re-processing.
- Already-normalized names are detected and left unchanged.
"""
import argparse
import csv
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

CSV_FIELDS = ["old_name", "new_name", "doc_type", "source_folder", "status", "reason"]

# Terminal statuses: file is "done" and should not be re-processed.
SEEN_STATUSES = {"renamed", "already_normalized"}

# Supported file extensions (lowercase, with leading dot).
EXTS = {".pdf", ".ifc", ".dwg", ".docx", ".xlsx"}

# Recognized type prefixes in canonical form, ordered most specific first.
TYPE_PREFIXES = ("GOST-R", "GOST", "SP", "SNiP", "SanPiN", "FZ")


def ascii_slug(text: str) -> str:
    """Convert arbitrary text to an ASCII slug suitable for filenames."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-.")


def detect_type_prefix(stem: str) -> str | None:
    """Return the recognized type prefix at the start of the stem, or None.

    Case-insensitive. Looks for TYPE- or TYPE_ at the very start.
    GOST-R is matched before GOST to keep the 'R' suffix.
    """
    upper = stem.upper()
    for prefix in TYPE_PREFIXES:
        # Match prefix followed by - or _ (case-insensitive on the prefix too).
        if upper.startswith(prefix.upper() + "-") or upper.startswith(prefix.upper() + "_"):
            return prefix
    return None


def parse_canonical(stem: str) -> tuple | None:
    """Parse stem as canonical name (optionally with trailing description).

    Returns (doc_type, number, year, change) where change is "IZM-N" or "REV-N" or None.
    Returns None if the stem does not start with a known type prefix in the
    canonical form TYPE-NUMBER[-YEAR][-CHANGE].
    Year is required in the canonical form; absence of year means the file
    is not canonical and the caller should fall through to needs_review.
    """
    s = stem

    # SP: TYPE-NUMBER[.NUMBER]....YEAR[-CHANGE][-trailing description]
    # The official SP designation uses dots throughout (e.g. "СП 252.13330.2022"),
    # so the canonical form keeps dots between the number segments AND
    # between the number and the year. A dash between number and year is
    # NOT canonical: it would mean the source deviates from the official
    # designation, and such files are routed to needs_review.
    # A dash is only accepted as a separator for our IZM/REV suffixes.
    m = re.match(
        r"^SP[-_](\d{1,4}(?:\.\d+)+)\.(\d{4})"
        r"(?:[-_](IZM|REV)[-_](\d+))?"
        r"(?:[-_].*)?$",
        s, re.I,
    )
    if m:
        number, year, change_type, change_num = m.groups()
        change = f"{change_type.upper()}-{change_num}" if change_type else None
        return ("SP", number, year, change)

    # GOST-R: TYPE-NUMBER[.DECIMAL]-YYYY[-trailing description]
    m = re.match(
        r"^GOST[-_]R[-_](\d{1,6}(?:\.\d+)?)[-_](\d{4})"
        r"(?:[-_].*)?$",
        s, re.I,
    )
    if m:
        return ("GOST-R", m.group(1), m.group(2), None)

    # GOST (without R): TYPE-NUMBER[.DECIMAL]-YYYY[-trailing description]
    m = re.match(
        r"^GOST[-_](\d{1,6}(?:\.\d+)?)[-_](\d{4})"
        r"(?:[-_].*)?$",
        s, re.I,
    )
    if m:
        return ("GOST", m.group(1), m.group(2), None)

    # FZ: TYPE-NUMBER[-YYYY][-trailing description]
    m = re.match(
        r"^FZ[-_](\d{1,4})(?:[-_](\d{4}))?"
        r"(?:[-_].*)?$",
        s, re.I,
    )
    if m:
        number, year = m.group(1), m.group(2)
        if year is None:
            return None  # year required in canonical form
        return ("FZ", number, year, None)

    # SNiP
    m = re.match(
        r"^SNiP[-_](\d{1,3}(?:\.\d+)*)[-_](\d{4})"
        r"(?:[-_].*)?$",
        s, re.I,
    )
    if m:
        return ("SNiP", m.group(1), m.group(2), None)

    # SanPiN
    m = re.match(
        r"^SanPiN[-_](\d(?:\.\d+)*)[-_](\d{4})"
        r"(?:[-_].*)?$",
        s, re.I,
    )
    if m:
        return ("SanPiN", m.group(1), m.group(2), None)

    return None


def parse_federalnyy(stem: str) -> tuple | None:
    """Extract FZ number from "Federalnyy-Zakon…N_FZ…" style names.

    Returns (number, year) where year may be None. The year is only taken
    if it appears in structured form right after the FZ token; otherwise
    the caller should mark the file as needs_review.
    """
    m = re.search(r"[-_](\d{1,4})[-_]FZ(?:[-_](\d{4}))?", stem, re.I)
    if m:
        return (m.group(1), m.group(2))
    return None


def build_canonical_name(doc_type: str, number: str, year: str | None,
                        change: str | None, ext: str,
                        year_sep: str = "-") -> str:
    """Build canonical filename.

    The TYPE-NUMBER pair is always joined with "-".
    The NUMBER-YEAR pair is joined with year_sep:
      "." for SP (matches the official "СП 252.13330.2022" designation);
      "-" for GOST, GOST-R, FZ, SNiP, SanPiN.
    The optional IZM/REV change is always joined with "-".
    """
    base = f"{doc_type}-{number}"
    if year:
        base = f"{base}{year_sep}{year}"
    if change:
        base = f"{base}-{change}"
    return f"{base}{ext}"


# SP uses "." between number and year (matches official designation);
# all other types use "-".
YEAR_SEP_BY_TYPE = {
    "SP": ".",
    "GOST-R": "-",
    "GOST": "-",
    "FZ": "-",
    "SNiP": "-",
    "SanPiN": "-",
}


def plan_rename(p: Path, source: Path, today: str) -> dict:
    """Plan rename for a single file. Returns a dict with all journal fields.

    Does NOT touch the filesystem.
    """
    rel_path = p.relative_to(source).as_posix()
    ext = p.suffix.lower()
    stem = p.stem

    # F: extension check is first, so unsupported extensions get
    # empty doc_type and empty new_name regardless of any detected prefix.
    if ext not in EXTS:
        return {
            "old_name": rel_path,
            "new_name": "",
            "doc_type": "",
            "status": "skipped",
            "reason": "unsupported_extension",
        }

    parsed = parse_canonical(stem)
    if parsed is not None:
        doc_type, number, year, change = parsed
        year_sep = YEAR_SEP_BY_TYPE.get(doc_type, "-")
        canonical_name = build_canonical_name(
            doc_type, number, year, change, ext, year_sep=year_sep,
        )
        if stem == Path(canonical_name).stem:
            return {
                "old_name": rel_path,
                "new_name": canonical_name,
                "doc_type": doc_type,
                "status": "already_normalized",
                "reason": "already_normalized",
            }
        return {
            "old_name": rel_path,
            "new_name": canonical_name,
            "doc_type": doc_type,
            "status": "dry_run",
            "reason": "recognized",
        }

    # E: Federalnyy-Zakon with embedded FZ number.
    fed = parse_federalnyy(stem)
    if fed is not None:
        number, year = fed
        if year is not None:
            year_sep = YEAR_SEP_BY_TYPE.get("FZ", "-")
            return {
                "old_name": rel_path,
                "new_name": build_canonical_name(
                    "FZ", number, year, None, ext, year_sep=year_sep,
                ),
                "doc_type": "FZ",
                "status": "dry_run",
                "reason": "recognized",
            }
        return {
            "old_name": rel_path,
            "new_name": p.name,  # keep original
            "doc_type": "FZ",
            "status": "skipped",
            "reason": "needs_review",
        }

    type_prefix = detect_type_prefix(stem)
    if type_prefix is not None:
        return {
            "old_name": rel_path,
            "new_name": p.name,
            "doc_type": type_prefix,
            "status": "skipped",
            "reason": "needs_review",
        }

    # Unrecognized: produce <TYPE>-<DATE>-<SLUG>.<ext> using the file's
    # own extension prefix (PDF, IFC, XLSX, DWG, DOCX), not always PDF.
    prefix = ext.lstrip(".").upper()
    slug = ascii_slug(stem)[:24]
    return {
        "old_name": rel_path,
        "new_name": f"{prefix}-{today}-{slug}{ext}",
        "doc_type": prefix,
        "status": "dry_run",
        "reason": "unrecognized_pdf",
    }


def _is_skippable(p: Path, source: Path, map_path: Path | None = None) -> bool:
    if not p.is_file():
        return True
    if p.name.startswith("."):
        return True
    rel_parts = p.relative_to(source).parts
    if any(part.startswith(".") or part == "__pycache__" for part in rel_parts):
        return True
    if p.name in {"normalize_names.py", "doc_type_map.csv",
                  "doc_type_map.example.csv"}:
        return True
    # Skip the journal itself if it lives inside the source folder.
    if map_path is not None:
        try:
            p.resolve().relative_to(map_path.resolve().parent)
        except ValueError:
            pass
        else:
            if p.resolve() == map_path.resolve():
                return True
    return False


def _build_seen(map_path: Path) -> dict:
    """Build {rel_path: status} from existing journal, terminal statuses only."""
    seen: dict[str, str] = {}
    if not map_path.exists():
        return seen
    with map_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            status = row.get("status", "")
            if status in SEEN_STATUSES:
                seen[row["old_name"]] = status
    return seen


def _detect_collisions(plans: list, source: Path) -> None:
    """In-place: mark colliding plans as error/collision and clear new_name."""
    proposers: dict[str, list[str]] = {}
    for plan in plans:
        if plan["status"] in ("dry_run", "renamed") and plan["new_name"]:
            proposers.setdefault(plan["new_name"], []).append(plan["old_name"])
    for new_name, old_names in proposers.items():
        if len(old_names) > 1:
            for plan in plans:
                if plan["old_name"] in old_names:
                    plan["status"] = "error"
                    plan["reason"] = "collision"
                    plan["new_name"] = ""


def _detect_target_exists(plans: list, source: Path) -> None:
    """In-place: mark plans whose target already exists in source as error."""
    for plan in plans:
        if plan["status"] in ("dry_run", "renamed") and plan["new_name"]:
            target = source / plan["new_name"]
            source_path = source / plan["old_name"]
            if target.exists() and target != source_path:
                plan["status"] = "error"
                plan["reason"] = "target_exists"
                plan["new_name"] = ""


def _execute_renames(plans: list, source: Path) -> None:
    """In-place: rename files for plans still in status=dry_run."""
    for plan in plans:
        if plan["status"] == "dry_run" and plan["new_name"]:
            old_path = source / plan["old_name"]
            new_path = source / plan["new_name"]
            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)
                plan["status"] = "renamed"


def _write_journal(plans: list, map_path: Path, source: Path) -> None:
    write_header = not map_path.exists()
    mode = "w" if write_header else "a"
    with map_path.open(mode, encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            writer.writeheader()
        for plan in plans:
            writer.writerow({
                "old_name": plan["old_name"],
                "new_name": plan["new_name"],
                "doc_type": plan["doc_type"],
                "source_folder": str(source),
                "status": plan["status"],
                "reason": plan["reason"],
            })


def _summary(plans: list, has_blocking_errors: bool) -> dict:
    s = {
        "total_planned": len(plans),
        "renamed": sum(1 for p in plans if p["status"] == "renamed"),
        "dry_run": sum(1 for p in plans if p["status"] == "dry_run"),
        "already_normalized": sum(
            1 for p in plans if p["status"] == "already_normalized"
        ),
        "needs_review": sum(
            1 for p in plans
            if p["status"] == "skipped" and p["reason"] == "needs_review"
        ),
        "unsupported_extension": sum(
            1 for p in plans
            if p["status"] == "skipped" and p["reason"] == "unsupported_extension"
        ),
        "collision": sum(
            1 for p in plans
            if p["status"] == "error" and p["reason"] == "collision"
        ),
        "target_exists": sum(
            1 for p in plans
            if p["status"] == "error" and p["reason"] == "target_exists"
        ),
        "has_blocking_errors": has_blocking_errors,
    }
    return s


def run(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Normalize filenames to ASCII naming contract."
    )
    ap.add_argument("--source", required=True, help="Source folder to scan")
    ap.add_argument("--map", default="tools/rename/doc_type_map.csv",
                    help="Path to the journal CSV (created/appended)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Plan renames without touching files")
    args = ap.parse_args(argv)

    source = Path(args.source)
    if not source.is_dir():
        sys.exit(f"Source folder not found: {source}")

    today = date.today().isoformat()
    map_path = Path(args.map)
    map_path.parent.mkdir(parents=True, exist_ok=True)

    seen = _build_seen(map_path)

    plans: list[dict] = []
    for p in sorted(source.rglob("*")):
        if _is_skippable(p, source, map_path):
            continue
        rel = p.relative_to(source).as_posix()
        if rel in seen:
            # Already terminally processed; do not add to journal again.
            continue
        plans.append(plan_rename(p, source, today))

    _detect_collisions(plans, source)
    _detect_target_exists(plans, source)

    has_blocking_errors = any(
        plan["status"] == "error" for plan in plans
    )

    if not args.dry_run and not has_blocking_errors:
        _execute_renames(plans, source)

    _write_journal(plans, map_path, source)

    summary = _summary(plans, has_blocking_errors)
    print(f"Completed. Map: {map_path}; dry-run={args.dry_run}; "
          f"has_blocking_errors={has_blocking_errors}")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    return 0


def main() -> int:
    return run()


if __name__ == "__main__":
    sys.exit(main())
