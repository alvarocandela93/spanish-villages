# Spanish Villages

An Android application for discovering, exploring and recording Spanish villages and population centres that the user has physically visited.

The core idea is simple:

> **Find a village → visit it → mark it visited → track your progress across Spain.**

The application is designed to be geographic, personal, privacy-first and useful even without an internet connection.

---

## 1. Product Vision

Spanish Villages helps users build a personal map and history of the places they have physically visited.

The application should make it easy to:

* Discover eligible Spanish population centres.
* Search for places by name.
* Explore places on a map.
* See visited and unvisited places.
* Mark a place as visited.
* Review visit history.
* Filter places geographically.
* Understand personal progress across Spain.
* Optionally use device location to help identify visits.

The MVP should remain deliberately simple.

There should be no requirement for:

* User accounts
* Social networks
* Public profiles
* Followers
* Messaging
* Leaderboards
* Complex gamification
* Backend infrastructure
* Cloud synchronization

unless explicitly introduced as a future product requirement.

---

## 2. Geographic Definition

The application must NOT equate "village" with "municipality".

The Spanish geographic model contains several relevant concepts:

* Municipio
* Entidad colectiva de población
* Entidad singular de población
* Núcleo de población
* Diseminado

The initial product concept is:

> A Spanish population centre with fewer than 10,000 inhabitants.

The exact canonical geographic unit must be determined from authoritative Spanish data before the production dataset is created.

The application should primarily use the INE Nomenclátor as the population authority and the IGN geographic nomenclators as an important source for geospatial information.

Do not invent geographic entities, population figures or coordinates.

---

## 3. Product Principles

### Geographic first

The application should feel like a geographic exploration tool rather than a conventional list/database application.

### Offline first

The core experience should remain useful without an internet connection.

Users should be able to:

* Browse the local village dataset.
* Search locally.
* View visited status.
* Mark places visited.
* View progress.
* Review visit history.

### Privacy first

Visit history belongs to the user.

The MVP should store user data locally.

Location access must be optional.

### Simple

Prefer simple functionality that solves the core problem over additional features.

### Data integrity

Official geographic identifiers should be preferred over names.

Names can change, duplicate or exist in multiple municipalities.

### Maintainability

The geographic dataset will eventually need to be updated.

User visit history must survive geographic dataset updates whenever the underlying place remains identifiable.

---

## 4. Technology Direction

The project is intended to use modern Android development practices.

Primary technologies:

* Kotlin
* Jetpack Compose
* Android Jetpack
* Room
* Kotlin Coroutines
* Flow / StateFlow
* Navigation Compose
* DataStore where appropriate
* Dependency injection where justified

Map provider, application ID, and final package name are not fixed yet.

---

## 5. Repository layout

```text
docs/                  Product/architecture notes, ADRs, data source registry
tools/data-pipeline/   INE ingest, canonical JSONL export, validation
data/raw/              Authoritative downloads (large files gitignored)
data/processed/        Versioned canonical dataset for app import
PRODUCT_REQUIREMENTS.md
TECHNICAL_SPEC.md
TODO.md
```

The Android application module will be added under Phase 2 (see `TODO.md`).

---

## 6. Geographic data

Do not treat **municipio** as a village. The canonical MVP unit is an **INE entidad singular de población** with population **under 10_000**, documented in `docs/geographic-model.md`.

Dataset build:

```bash
cd tools/data-pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build_dataset.py
```

---

## 7. Development status

| Area | Status |
| --- | --- |
| Product / tech docs | Draft complete |
| Geographic model (Phase 0) | Documented |
| INE data pipeline (Phase 1) | Initial implementation |
| Android app | Not started |

See `docs/PROJECT_ASSESSMENT.md` for architecture, risks, and open questions.

---

## 8. License and data attribution

Application license TBD. Geographic data subject to [INE legal notice](https://www.ine.es/aviso_legal) and future IGN/CNIG terms when coordinates are merged.
