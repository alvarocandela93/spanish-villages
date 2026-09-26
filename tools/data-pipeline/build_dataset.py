#!/usr/bin/env python3
"""CLI: build canonical dataset from local INE XLSX."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from spanish_villages_pipeline.build import DEFAULT_REFERENCE_DATE, build_canonical
from spanish_villages_pipeline.validate import validate_dataset


def _extract_xlsx(zip_path: Path, extract_dir: Path) -> Path:
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        xlsx_name = next(n for n in archive.namelist() if n.lower().endswith(".xlsx"))
        archive.extract(xlsx_name, extract_dir)
        return extract_dir / xlsx_name


def main() -> None:
    parser = argparse.ArgumentParser(description="Build canonical Spanish Villages dataset")
    parser.add_argument(
        "--xlsx",
        type=Path,
        help="Path to INE nomdef XLSX (default: extract from --zip)",
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=Path("data/raw/ine/nomenclator_nacional_2025.zip"),
        help="Path to INE national ZIP",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/2025-01-01"),
    )
    parser.add_argument(
        "--reference-date",
        default=DEFAULT_REFERENCE_DATE,
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    xlsx_path = args.xlsx
    if xlsx_path is None:
        zip_path = args.zip if args.zip.is_absolute() else repo_root / args.zip
        xlsx_path = _extract_xlsx(zip_path, repo_root / "data/raw/ine/extracted")
    output_dir = args.output if args.output.is_absolute() else repo_root / args.output

    summary = build_canonical(xlsx_path, output_dir, reference_date=args.reference_date)
    report = validate_dataset(output_dir)
    print("Summary:", summary["counts"])
    if not report["ok"]:
        raise SystemExit(f"Validation failed with {report['errorCount']} errors")
    print("Validation OK")


if __name__ == "__main__":
    main()
