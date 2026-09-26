"""Validate canonical dataset outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def validate_dataset(processed_dir: Path) -> dict[str, Any]:
    places = _read_jsonl(processed_dir / "canonical_places.jsonl")
    municipalities = _read_jsonl(processed_dir / "municipalities.jsonl")
    nuclei = _read_jsonl(processed_dir / "nuclei.jsonl")

    errors: list[str] = []
    warnings: list[str] = []

    place_ids = set()
    for place in places:
        pid = place["id"]
        if pid in place_ids:
            errors.append(f"Duplicate place id: {pid}")
        place_ids.add(pid)
        if len(pid) != 11 or not pid.isdigit():
            errors.append(f"Invalid place id: {pid}")
        if place["placeType"] != "singular_entity":
            errors.append(f"Unexpected placeType for {pid}")
        if place["population"] < 0:
            errors.append(f"Negative population for {pid}")
        if place["isEligible"] and place["population"] >= 10_000:
            errors.append(f"Eligible place at or above threshold: {pid}")
        if place["municipalityId"] not in {m["id"] for m in municipalities}:
            errors.append(f"Missing municipality for place {pid}")

    municipality_ids = {m["id"] for m in municipalities}
    if len(municipality_ids) != len(municipalities):
        errors.append("Duplicate municipality ids")

    for nucleus in nuclei:
        parent = nucleus.get("parentEntityCode")
        if parent and parent not in place_ids:
            errors.append(f"Nucleus {nucleus['id']} references unknown parent {parent}")

    report = {
        "ok": len(errors) == 0,
        "errorCount": len(errors),
        "warningCount": len(warnings),
        "errors": errors[:100],
        "warnings": warnings[:100],
        "counts": {
            "places": len(places),
            "eligible": sum(1 for p in places if p["isEligible"]),
            "municipalities": len(municipalities),
            "nuclei": len(nuclei),
        },
    }
    (processed_dir / "validation-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report
