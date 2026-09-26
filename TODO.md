# TODO — Spanish Villages

This file is the active development roadmap.

Status:

* `[ ]` Not started
* `[~]` In progress
* `[x]` Complete
* `[!]` Blocked / requires decision

---

# PHASE 0 — Product & Geographic Definition

## Geographic research

* [ ] Review INE Nomenclátor methodology.
* [ ] Review definitions of municipio, entidad singular, núcleo and diseminado.
* [ ] Review IGN Nomenclátor Geográfico.
* [ ] Determine the canonical user-facing geographic unit.
* [ ] Determine whether entity singular, nucleus or a combination should represent a "village".
* [ ] Define treatment of diseminados.
* [ ] Define treatment of municipalities that have only one population entity.
* [ ] Define treatment of population centres with zero/very small populations.
* [ ] Define treatment of duplicate names.
* [ ] Document geographic decision in `docs/geographic-model.md`.

## Population definition

* [ ] Confirm population threshold: `< 10,000`.
* [ ] Confirm population reference date.
* [ ] Confirm source version.
* [ ] Document population methodology.
* [ ] Define how annual dataset updates affect eligibility.

---

# PHASE 1 — Data Pipeline

## Raw data

* [ ] Obtain latest INE Nomenclátor dataset available at implementation time.
* [ ] Obtain appropriate IGN geographic dataset.
* [ ] Store source metadata.
* [ ] Record download/reference dates.
* [ ] Document licenses/usage requirements.

## Normalization

* [ ] Normalize identifiers.
* [ ] Normalize names.
* [ ] Normalize administrative relationships.
* [ ] Normalize coordinates.
* [ ] Normalize population fields.
* [ ] Identify entity/nucleus relationships.
* [ ] Identify diseminados.

## Validation

* [ ] Check duplicate IDs.
* [ ] Check missing identifiers.
* [ ] Check invalid coordinates.
* [ ] Check invalid populations.
* [ ] Check broken administrative relationships.
* [ ] Check duplicate names.
* [ ] Check threshold calculation.
* [ ] Generate validation report.

## Canonical dataset

* [ ] Define canonical schema.
* [ ] Generate canonical dataset.
* [ ] Assign dataset version.
* [ ] Produce summary statistics.
* [ ] Manually inspect representative samples from multiple autonomous communities.

---

# PHASE 2 — Android Foundation

* [ ] Create Android project.
* [ ] Configure Kotlin.
* [ ] Configure Compose.
* [ ] Configure Gradle.
* [ ] Configure lint.
* [ ] Configure testing.
* [ ] Establish package structure.
* [ ] Establish dependency injection approach.
* [ ] Establish navigation.
* [ ] Create base theme.
* [ ] Create application-level error handling.
* [ ] Create initial CI/build validation if appropriate.

---

# PHASE 3 — Local Database

* [ ] Define final domain models.
* [ ] Define Room entities.
* [ ] Define DAOs.
* [ ] Define database.
* [ ] Define migrations.
* [ ] Define indices.
* [ ] Define foreign keys.
* [ ] Implement dataset import.
* [ ] Validate imported record counts.
* [ ] Validate representative records.

---

# PHASE 4 — Browse

* [ ] Create home screen.
* [ ] Create village list.
* [ ] Create place card.
* [ ] Display visited status.
* [ ] Add basic filtering.
* [ ] Implement pagination/lazy loading if required.
* [ ] Test large dataset performance.

---

# PHASE 5 — Search

* [ ] Implement normalized search.
* [ ] Test accent-insensitive search.
* [ ] Test duplicate place names.
* [ ] Test municipality-qualified searches.
* [ ] Evaluate SQLite FTS.
* [ ] Add search UI.
* [ ] Add empty state.
* [ ] Add offline search tests.

---

# PHASE 6 — Place Details

* [ ] Create detail screen.
* [ ] Display population.
* [ ] Display population reference date.
* [ ] Display municipality.
* [ ] Display province.
* [ ] Display autonomous community.
* [ ] Display coordinates.
* [ ] Display visited state.
* [ ] Add mark-visited action.

---

# PHASE 7 — Visits

* [ ] Create Visit entity.
* [ ] Create Visit DAO.
* [ ] Implement manual visit creation.
* [ ] Implement visit removal.
* [ ] Store timestamp.
* [ ] Store visit method.
* [ ] Support multiple visits.
* [ ] Test persistence after app restart.
* [ ] Test duplicate visits.

---

# PHASE 8 — Progress

* [ ] Calculate total eligible places.
* [ ] Calculate visited places.
* [ ] Calculate percentage.
* [ ] Calculate progress by province.
* [ ] Calculate progress by autonomous community.
* [ ] Build progress screen.
* [ ] Test calculations against known datasets.

---

# PHASE 9 — Map

## Provider decision

* [ ] Evaluate Google Maps.
* [ ] Evaluate MapLibre.
* [ ] Evaluate licensing.
* [ ] Evaluate offline options.
* [ ] Evaluate cost.
* [ ] Document decision.

## Implementation

* [ ] Integrate map.
* [ ] Display places.
* [ ] Display visited state.
* [ ] Add marker clustering if necessary.
* [ ] Add map → place navigation.
* [ ] Add viewport filtering.
* [ ] Test performance with full dataset.

---

# PHASE 10 — Offline Experience

* [ ] Verify browsing offline.
* [ ] Verify search offline.
* [ ] Verify place details offline.
* [ ] Verify visit creation offline.
* [ ] Verify progress offline.
* [ ] Verify history offline.
* [ ] Define map offline behaviour.
* [ ] Test airplane mode.

---

# PHASE 11 — Location

MVP does not require automatic visit detection.

Future preparation:

* [ ] Define location permission UX.
* [ ] Implement location abstraction.
* [ ] Implement distance calculations.
* [ ] Design candidate visit detection.
* [ ] Define dwell-time requirements.
* [ ] Design confirmation UX.
* [ ] Test battery implications.
* [ ] Test background restrictions.

---

# PHASE 12 — Quality

* [ ] Unit tests.
* [ ] DAO tests.
* [ ] Repository tests.
* [ ] ViewModel tests.
* [ ] UI tests.
* [ ] Accessibility review.
* [ ] Performance profiling.
* [ ] Memory profiling.
* [ ] Offline testing.
* [ ] Database migration testing.
* [ ] Large dataset testing.

---

# PHASE 13 — Release Preparation

* [ ] Application icon.
* [ ] App name.
* [ ] Package/application ID.
* [ ] Versioning strategy.
* [ ] Release signing.
* [ ] Privacy policy requirements.
* [ ] Data-source attribution.
* [ ] Map attribution/licensing.
* [ ] Store screenshots.
* [ ] Store description.
* [ ] Internal testing build.
* [ ] Production release build.

---

# Current Priority

The current highest-priority tasks are:

1. Geographic definition
2. Canonical data model
3. Authoritative dataset
4. Dataset validation
5. Android foundation

Do NOT skip these steps to build the UI prematurely.
