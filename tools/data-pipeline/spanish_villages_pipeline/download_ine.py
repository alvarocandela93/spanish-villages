"""Download INE Nomenclátor national ZIP."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

INE_DOWNLOAD_URL = "https://www.ine.es/nomen2/Descarga"


def download_national_zip(year: int, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    body = f"anioNacional={year}".encode("utf-8")
    request = Request(
        INE_DOWNLOAD_URL,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urlopen(request, timeout=120) as response:
        data = response.read()
    if data[:2] != b"PK":
        raise RuntimeError("Expected ZIP from INE; check response body")
    output_path.write_bytes(data)
    return output_path


def write_source_metadata(
    metadata_path: Path,
    *,
    year: int,
    zip_path: Path,
    reference_date: str,
) -> None:
    metadata = {
        "source": "INE_NOMENCLATOR",
        "operation": "30261",
        "referenceDate": reference_date,
        "downloadYearSelector": year,
        "downloadedAt": datetime.now(timezone.utc).isoformat(),
        "downloadUrl": INE_DOWNLOAD_URL,
        "localZip": str(zip_path),
        "license": "https://www.ine.es/aviso_legal",
        "resultsPage": "https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177010&menu=resultados&idp=1254735572981",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
