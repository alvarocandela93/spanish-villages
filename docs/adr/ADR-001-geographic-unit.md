# ADR-001: Canonical geographic unit for “village”

## Status

Accepted — 2026-09-25

## Context

Spanish “village” is not a single official administrative type. Municipios can contain multiple settlements. INE publishes population for **entidades singulares**, **núcleos**, and **diseminados** under a unified 11-digit code.

The product requires:

- Population centres under 10_000 inhabitants
- Distinction from municipio and from dispersed housing
- Stable identifiers for visit history across dataset updates

## Decision

1. **Canonical visit target (MVP):** INE **entidad singular de población**, identified by the 11-digit INE code on the **entity aggregate** row (`NN = 00`, `SS ≠ 00`).
2. **Eligibility:** entity population **strictly less than** 10_000; exclude diseminados and non-entity rows.
3. **Núcleos** are stored as related data but are not separate visit targets in MVP.
4. **Municipio** is administrative context only.

## Consequences

- Progress denominators count eligible entidades singulares (~61k for 2025-01-01 snapshot).
- Map pins should prefer IGN coordinates for the entity; if only núcleo points exist, merge logic must pick a representative point (future ADR).
- Users visiting one núcleo of a multi-nucleus entity still mark the **entity** visited unless product changes.

## Alternatives considered

| Alternative | Rejected because |
| --- | --- |
| Municipio | Conflates multiple settlements; violates core product rule |
| Núcleo | Splits one named village; wrong denominator for “Albarracín”-style places |
| Entity + nucleus combined row | Over-complicates MVP; duplicates parent/child visits |
