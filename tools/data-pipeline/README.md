# Geographic data pipeline

Builds the canonical offline dataset for the Android app from **INE Nomenclátor** files.

## Setup

```bash
cd tools/data-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Download INE national file (2025 reference)

From repository root:

```bash
python -c "
from pathlib import Path
from spanish_villages_pipeline.download_ine import download_national_zip, write_source_metadata
zip_path = Path('data/raw/ine/nomenclator_nacional_2025.zip')
download_national_zip(2025, zip_path)
write_source_metadata(Path('data/raw/ine/source-metadata.json'), year=2025, zip_path=zip_path, reference_date='2025-01-01')
"
```

## Build canonical outputs

```bash
python build_dataset.py
```

Outputs under `data/processed/2025-01-01/`:

- `canonical_places.jsonl` — entidades singulares (`isEligible` flag)
- `municipalities.jsonl`
- `nuclei.jsonl`
- `summary.json`
- `validation-report.json`

## Tests

```bash
pytest
```

## Next step

Merge IGN NGMEP coordinates into `canonical_places.jsonl` by `ineCode` after downloading to `data/raw/ign/` (see `docs/data-sources.md`).
