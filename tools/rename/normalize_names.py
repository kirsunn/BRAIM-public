#!/usr/bin/env python3
"""Normalize normative/project filenames to ASCII naming contract.

Usage:
  python normalize_names.py --source TN_DOWNLOADS --map tools/rename/doc_type_map.csv --dry-run
  python normalize_names.py --source download --map tools/rename/doc_type_map.csv
  python normalize_names.py --source _library/normative/sp_extracted --map tools/rename/doc_type_map.csv

Safety:
- Creates or appends a CSV audit trail.
- Never deletes files.
- Refuses to overwrite an existing target name.
- Does not process hidden files or the script/map itself.
"""
import argparse, csv, re, sys, unicodedata
from pathlib import Path
from datetime import date

CSV_FIELDS=["old_name","new_name","doc_type","source_folder","status","reason"]
TYPE_PATTERNS=[
    (r"^SP[-_ ]?(\d{1,4}(?:\.\d{1,6})?)(?:[-_ ]?(\d{4}))?", "SP"),
    (r"^GOST[-_ ]?R[-_ ]?(\d{1,6}(?:\.\d+)?)", "GOST-R"),
    (r"^GOST[-_ ]?(\d{1,6}(?:\.\d+)?)", "GOST"),
    (r"^SNiP[-_ ]?(\d{1,3}(?:\.\d+)*)", "SNiP"),
    (r"^SanPiN[-_ ]?(\d(?:\.\d+)*)", "SanPiN"),
    (r"^FZ[-_ ]?(\d{1,4})", "FZ"),
]
EXTS={".pdf",".ifc",".dwg",".docx",".xlsx"}

def ascii_slug(text):
    text=unicodedata.normalize("NFKD", text)
    text="".join(c for c in text if not unicodedata.combining(c))
    text=re.sub(r"[^A-Za-z0-9._-]+","-",text)
    return re.sub(r"-{2,}","-",text).strip("-.")

def detect(old_name):
    stem=Path(old_name).stem
    for pattern, doc_type in TYPE_PATTERNS:
        m=re.search(pattern, stem, re.I)
        if m:
            return doc_type, m.group(0)
    return None, None

def normalize(old_name, today):
    ext=Path(old_name).suffix.lower()
    if ext not in EXTS:
        return None, "unsupported_extension"
    doc_type, matched=detect(old_name)
    if not doc_type:
        return f"PDF-{today}-{ascii_slug(Path(old_name).stem)[:24]}{ext}", "unrecognized_pdf"
    base=ascii_slug(matched)
    return f"{base}{ext}", "recognized"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--map", default="tools/rename/doc_type_map.csv")
    ap.add_argument("--dry-run", action="store_true")
    args=ap.parse_args()
    source=Path(args.source)
    if not source.is_dir():
        sys.exit(f"Source folder not found: {source}")
    today=date.today().isoformat()
    map_path=Path(args.map); map_path.parent.mkdir(parents=True, exist_ok=True)
    exists=map_path.exists()
    seen=set()
    if exists:
        with map_path.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f): seen.add(row["old_name"])
    mode="a" if exists else "w"
    with map_path.open(mode, encoding="utf-8-sig", newline="") as f:
        writer=csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not exists: writer.writeheader()
        for p in sorted(source.rglob("*")):
            if not p.is_file() or p.name.startswith(".") or p.name in {"normalize_names.py","doc_type_map.csv"}:
                continue
            if p.name in seen: continue
            new_name, reason=normalize(p.name, today)
            status="skipped" if new_name is None else ("dry_run" if args.dry_run else "renamed")
            target=p.with_name(new_name) if new_name else None
            if target and target.exists() and target!=p:
                status="error"; reason="target_exists"
                new_name=""
            elif target and not args.dry_run and status=="renamed":
                p.rename(target)
            writer.writerow({"old_name":str(p.relative_to(source)), "new_name":new_name, "doc_type":reason if reason=="unrecognized_pdf" else (new_name.split("-")[0] if new_name else ""), "source_folder":str(source), "status":status, "reason":reason})
    print(f"Completed. Map: {map_path}; dry-run={args.dry_run}")

if __name__=="__main__":
    main()
