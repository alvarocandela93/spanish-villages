# Geographic model — Spanish Villages

This document records the official Spanish statistical geography relevant to the product and the **canonical unit** used in the app and data pipeline.

Sources (authoritative):

- INE — [Nomenclátor: metodología](https://www.ine.es/nomenclator/metodologia.htm)
- INE — [Glosario: Entidad singular](https://www.ine.es/DEFIne/es/concepto.htm?c=4928)
- INE — [Glosario: Núcleo de población](https://www.ine.es/DEFIne/concepto.htm?c=4930)
- IGN — [NGMEP description (INE code PPMMMCCSSNN)](https://www.ign.es/resources/IGR/Poblaciones/IGN_descripcionBDEP_IGR-P0v0.pdf)

Population reference for the current pipeline snapshot: **2025-01-01** (INE Nomenclátor national file, published 2026-01-28).

---

## Concepts (do not conflate)

### Municipio

Administrative local-government unit. One municipio may contain:

- One or several **entidades singulares**
- Optional **entidades colectivas** (historical groupings, mainly in northern Spain)
- Within each entidad singular: one or more **núcleos**, plus **diseminado**

**Product rule:** municipio ≠ village. Do not use municipio population for eligibility.

### Entidad colectiva de población

Grouping of entidades singulares (parroquias, concejos, etc.). Used for statistics and coding (`CC` in the INE code). Not the MVP visit target.

### Entidad singular de población

> Área habitable del término municipal, claramente diferenciada, conocida por una denominación específica.

Strong match for the product phrase “population centre / village”. Population is published at this level in the Nomenclátor (row with nucleus code `00` within the entity).

**Entidad única:** If a municipio has no clearly differentiated areas, the municipio is treated as a **single entidad singular** (same name as the municipio).

### Núcleo de población

Physically concentrated built-up area (street pattern, ≥10 buildings, etc.). An entidad singular may have **0, 1, or many** núcleos. Population is also published per núcleo.

Useful when representing a **physical settlement** on a map; may split one “village” into several núcleos.

### Diseminado

Buildings in an entidad singular **not** assigned to any núcleo (`NN = 99` in the INE code). **Not** a village for this product.

### Municipio capital (seat)

The main town where the ayuntamiento sits. It is a **role** within a municipio, not a separate INE unit type. IGN NGMEP exposes capital flags. The seat is usually an entidad singular (often the largest); the app should not treat “capital” as a substitute for entidad singular records.

---

## INE 11-digit code (`PPMMMCCSSNN`)

| Segment | Meaning |
| --- | --- |
| `PP` | Province |
| `MMM` | Municipio within province |
| `CC` | Entidad colectiva (`00` if none) |
| `SS` | Entidad singular (`00` = not at entity/nucleus level below collective) |
| `NN` | Núcleo (`00` = entity-level aggregate row), `99` = diseminado |

Examples (Álava, Alegria-Dulantzi):

| Code | Type |
| --- | --- |
| `01001000100` | Entidad singular (aggregate) |
| `01001000101` | Núcleo |
| `01001000199` | Diseminado |

---

## Product decision (canonical unit)

**User-facing place (MVP):** **Entidad singular de población**

**Primary key:** INE code with `SS ≠ 00` and `NN = 00` (entity aggregate row).

**Eligibility:**

```text
unit type = entidad singular
AND population < 10_000
AND NOT diseminado
```

Population is taken from the **entity aggregate** row (`NN = 00`), not from municipio totals and not from individual núcleos (a núcleo may be small while the entity exceeds 10_000).

**Núcleos:** Retained in the canonical dataset as related records (`parentEntityCode`) for future map precision and optional sub-place UX; **MVP visit actions target the entidad singular**.

**Diseminados:** Excluded from eligible places; may appear in raw data for audit.

---

## Edge cases

| Case | Treatment |
| --- | --- |
| Single-entity municipio | One eligible entidad singular; name often equals municipio name |
| Multi-nucleus entity | One visit target (entity); map may later show núcleos |
| Entity population ≥ 10_000 | Not eligible; even if núcleos are smaller |
| Entity population 0 | Retained if type is entidad singular; product may hide in UI later |
| Duplicate names | Distinct INE codes; UI must show municipio/province |
| Renamed / deleted entities | Visits keyed by INE code; dataset updates need migration rules (future ADR) |

---

## Relation to IGN

IGN **NGMEP** uses the same 11-digit INE code for INE entities. Coordinates and `capital` flags come from IGN, merged in the pipeline by `ineCode`. Places without IGN coordinates remain in the dataset with null coordinates until geocoding is available.
