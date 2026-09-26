# Project Assessment — Spanish Villages

Assessment date: 2026-09-25

## 1. Current project assessment

The repository is a **documentation-first greenfield project**. It contains product requirements, technical specification, TODO roadmap, and a partial README. There is **no Android application code**, Gradle project, or database yet.

| Asset | Status |
| --- | --- |
| `PRODUCT_REQUIREMENTS.md` | Complete, internally consistent |
| `TECHNICAL_SPEC.md` | Complete; defers map provider and final Room schema |
| `TODO.md` | Phased roadmap aligned with specs |
| `README.md` | Truncated (technology section incomplete) |
| `docs/geographic-model.md` | Created in Phase 0 (this sprint) |
| Data pipeline | Phase 1 increment started under `tools/data-pipeline/` |
| Tests | Pipeline unit tests only (Android tests not yet applicable) |

**Contradictions / gaps**

- README is truncated and still references placeholder package `com.example.spanishvillages` from the technical spec example.
- Product requires coordinates on place detail, but INE Nomenclátor files are **population-only**; coordinates require a separate IGN/CNIG merge (Phase 1 documents dependency; merge script stubbed for full NGMEP download).
- TODO “Phase 1” is the **data pipeline**, while the user prompt’s “Phase 1” in a later MVP sense maps to **Android foundation** (TODO Phase 2). This assessment follows `TODO.md` numbering.

## 2. Proposed architecture

Layered **offline-first** Android app (future):

```text
Compose UI (screens: browse, search, map, detail, history, progress)
        ↓ StateFlow
ViewModels
        ↓
Domain use cases (eligibility, search normalize, progress, visits)
        ↓
Repositories (PlaceRepository, VisitRepository, DatasetRepository)
        ↓
Room (places, admin hierarchy, visits, dataset_metadata)
        ↑
Asset import / bundled canonical dataset (from data pipeline)
```

**DI:** Hilt when the Android module exists (justified once multiple repositories and test fakes are needed).

**No backend** in MVP. Optional location layer sits behind interfaces and is not required for core flows.

## 3. Recommended geographic model

See [geographic-model.md](./geographic-model.md) and [adr/ADR-001-geographic-unit.md](./adr/ADR-001-geographic-unit.md).

**Summary:** The user-facing “village” for MVP is an **INE entidad singular de población**, keyed by the **11-digit INE unit code** at entity level (`NN = 00`, `SS ≠ 00`). Eligibility uses **entity population** from the Nomenclátor, with **`population < 10_000`**, excluding **diseminados** (`NN = 99`) and non-place rows (municipal totals, entidades colectivas). **Núcleos** are stored as related units for future use but are not the primary visit target in MVP.

**Municipio** is administrative context only; **municipio capital** (seat) is not equated with the visitable place unless it coincides with an eligible entidad singular record.

## 4. Recommended initial database / domain model

**Domain**

- `PopulationPlace` — eligible entidad singular (canonical visit target)
- `PopulationNucleus` — optional child of entity (not visited separately in MVP UI)
- `Municipality`, `Province`, `AutonomousCommunity` — admin hierarchy
- `Visit` — `populationPlaceId`, `visitedAt`, `method` (`MANUAL` only in MVP)
- `DatasetMetadata` — version, source, population reference date, imported at

**Stable IDs:** `populationPlaceId` = INE 11-digit code at entity-singular level (deterministic, authoritative).

**Visited state:** derived from `EXISTS visit WHERE placeId = …` (supports multiple visits).

Room schema should be finalized after validating canonical JSON from Phase 1 (Phase 3 in TODO).

## 5. External data dependencies

| Source | Purpose | License / terms |
| --- | --- | --- |
| [INE Nomenclátor — Población por unidad poblacional](https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177010&menu=resultados&idp=1254735572981) | Population, INE codes, names, unit types | [INE aviso legal](https://www.ine.es/aviso_legal) |
| [IGN/CNIG NGMEP](https://centrodedescargas.cnig.es/) | Coordinates, capital flags, geometries | CNIG download terms (document per file) |
| Map tiles (TBD) | Map UI | Provider-specific; ADR required |

Details: [data-sources.md](./data-sources.md).

## 6. Major technical risks

1. **Wrong geographic grain** — Using municipio or núcleo would skew eligibility and UX; mitigated by ADR-001 and pipeline unit-type classification.
2. **Large dataset on device** — ~61k eligible entities; needs indexed Room, lazy lists, map viewport queries, possible clustering.
3. **Coordinate join** — INE and IGN keys must align on 11-digit INE code; IGN includes non-INE entities; join validation required.
4. **Name encoding / duplicates** — Latin-1 INE files vs UTF-8 app; many homonymous place names; UI must show municipality/province.
5. **Dataset updates** — Visits must remain keyed by stable INE codes when populations or names change.
6. **Map offline** — Full Spain vector/raster offline is heavy; MVP may use online tiles with list/search fully offline.

## 7. MVP implementation phases (recommended)

Aligned with `TODO.md`:

| Phase | Focus |
| --- | --- |
| 0 | Geographic definition — **done (docs + ADR)** |
| 1 | Data pipeline — **in progress (INE ingest + canonical export)** |
| 2 | Android foundation (Compose, navigation, theme, DI) |
| 3 | Room + dataset import |
| 4–8 | Browse, search, detail, visits, progress |
| 9 | Map (after provider ADR) |
| 10–13 | Offline verification, location prep, quality, release |

## 8. Requirements needing clarification

1. **Entidad singular vs núcleo for “visited”** — Recommended: visit marks the **entidad singular**; confirm before map pin placement if IGN gives nucleus-only coordinates.
2. **Places with population 0** — Include as eligible (user may visit ruins/hamlets) or exclude? Pipeline currently **includes** entity rows with `population >= 0` under threshold; zero-population entities exist.
3. **Ceuta/Melilla and single-entity municipios** — Included like other entities; confirm product copy for “Spain” scope.
4. **Threshold boundary** — Spec says `< 10_000` (not `<=`); entities at exactly 10_000 are excluded.
5. **Map provider** — Google vs MapLibre affects offline story and Play policy; decide before Phase 9.
6. **Bundled vs downloadable dataset** — MVP likely **bundled** canonical SQLite/JSON in APK with optional future updates; confirm size budget (~61k rows acceptable).
