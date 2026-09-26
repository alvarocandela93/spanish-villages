# Technical Specification — Spanish Villages

## 1. Technical Goals

Build a production-quality Android application that is:

* Offline-first
* Fast
* Testable
* Maintainable
* Privacy-preserving
* Geospatially capable
* Able to handle a large Spanish population dataset
* Able to receive future geographic dataset updates without destroying user data

---

# 2. Recommended Android Stack

## Language

Kotlin

## UI

Jetpack Compose

## Architecture

Layered architecture with:

```text
UI
 ↓
Domain
 ↓
Data
 ↓
Local / Network / Geographic sources
```

Use unidirectional data flow.

---

# 3. Architectural Principles

## Single direction of state

```text
User action
    ↓
ViewModel
    ↓
Use case / Repository
    ↓
Database
    ↓
Flow
    ↓
ViewModel
    ↓
Compose UI
```

UI should not directly access repositories or databases.

---

# 4. Offline-First Architecture

Room should be the primary local source of truth for structured application data.

The UI should read from local data.

Network operations should update local data rather than bypassing it.

Conceptually:

```text
             ┌──────────────┐
             │ Network/API  │
             └──────┬───────┘
                    ↓
              Repository
                    ↓
             ┌──────────────┐
             │    Room      │
             │ Local Source │
             └──────┬───────┘
                    ↓
               Domain/UI
```

This follows Android's offline-first architecture guidance.

---

# 5. Suggested Package Structure

A possible initial structure:

```text
app/
└── src/main/java/com/example/spanishvillages/

    ├── data/
    │   ├── local/
    │   │   ├── dao/
    │   │   ├── database/
    │   │   └── entity/
    │   │
    │   ├── remote/
    │   │   ├── api/
    │   │   └── model/
    │   │
    │   ├── repository/
    │   └── mapper/
    │
    ├── domain/
    │   ├── model/
    │   ├── repository/
    │   └── usecase/
    │
    ├── ui/
    │   ├── navigation/
    │   ├── home/
    │   ├── map/
    │   ├── search/
    │   ├── place/
    │   ├── history/
    │   └── progress/
    │
    ├── location/
    ├── map/
    ├── di/
    └── MainActivity.kt
```

The structure can change if justified.

---

# 6. Core Domain Model

The domain should distinguish geographic places from user visits.

Conceptually:

```text
PopulationPlace
    |
    | 1
    |
    | *
Visit
```

A place exists independently of whether the user visited it.

---

# 7. Population Place

Recommended conceptual fields:

```text
PopulationPlace
-------------------------
id
name
normalizedName
placeType
population
populationReferenceDate

municipalityId
provinceId
autonomousCommunityId

latitude
longitude

source
sourceVersion

isEligible
createdAt
updatedAt
```

The `id` must preferably be based on an authoritative geographic identifier rather than a generated name-based ID.

---

# 8. Geographic Hierarchy

Recommended entities:

```text
AutonomousCommunity
Province
Municipality
PopulationEntity
PopulationNucleus
```

The exact implementation depends on the outcome of the geographic research phase.

Do not assume every region uses the same conceptual hierarchy.

---

# 9. Geographic Identifiers

Identifiers should be stored separately from names.

Never use:

```text
place.name
```

as the primary key.

Names are not unique.

Prefer authoritative identifiers such as:

```text
provinceCode
municipalityCode
entityCode
nucleusCode
```

where available.

If a source does not provide a stable identifier, create a documented deterministic identifier based on authoritative source fields.

---

# 10. Visit Model

Recommended structure:

```text
Visit
-------------------------
id
populationPlaceId
visitedAt
method
latitude
longitude
createdAt
```

Where:

```text
method =
    MANUAL
    LOCATION_CONFIRMED
    FUTURE_AUTOMATIC
```

The MVP only requires:

```text
MANUAL
```

---

# 11. Multiple Visits

Do not enforce:

```text
one place = one visit
```

at the database level.

Instead:

```text
one place = zero or more visits
```

Visited state can be derived:

```sql
EXISTS(visit WHERE populationPlaceId = place.id)
```

This preserves future functionality.

---

# 12. Dataset Versioning

Geographic data must be versioned.

Example:

```text
datasetVersion:
    2025-01-01

populationReferenceDate:
    2025-01-01

source:
    INE_NOMENCLATOR

importedAt:
    2026-09-25
```

The app should be able to determine which dataset version produced a place.

---

# 13. Dataset Import Pipeline

The canonical dataset should NOT be manually embedded into Kotlin.

Use an external processing/import pipeline:

```text
INE source
     +
IGN geographic source
     ↓
Raw data
     ↓
Normalization
     ↓
Validation
     ↓
Eligibility filtering
     ↓
Canonical dataset
     ↓
Android import
     ↓
Room
```

The raw source files should not be treated as application data.

---

# 14. Data Validation

The import process should validate:

### Identity

* Required identifiers exist.
* No duplicate canonical IDs.

### Population

* Population is numeric.
* Population is non-negative.
* Population reference date exists.

### Geography

* Coordinates are valid.
* Latitude is approximately between -90 and 90.
* Longitude is approximately between -180 and 180.

### Relationships

* Every place references a valid municipality.
* Municipality references valid province/community where applicable.

### Eligibility

* Diseminados are excluded unless explicitly supported.
* Population threshold is applied consistently.

---

# 15. Population Threshold

Initial rule:

```text
population < 10,000
```

Do not use:

```text
population <= 10,000
```

unless the product requirement is explicitly changed.

The filtering rule belongs in the data-processing/domain layer rather than being duplicated throughout the UI.

---

# 16. Database

Use Room for structured local persistence.

Likely tables:

```text
population_places
autonomous_communities
provinces
municipalities
visits
dataset_metadata
```

Additional tables may be introduced if justified.

---

# 17. Room Design

Use:

* Foreign keys where appropriate
* Indices for frequently searched/filterable fields
* Migrations
* Transactions for multi-table updates
* Flow-returning DAO queries for observable state

Potential indices:

```text
population_places.name
population_places.normalizedName
population_places.municipalityId
population_places.provinceId
population_places.autonomousCommunityId
population_places.latitude
population_places.longitude

visits.populationPlaceId
visits.visitedAt
```

Actual indexing should be validated against query patterns.

---

# 18. Search

Search should operate locally.

The application should normalize search input:

```text
Ávila
avIla
AVILA
```

to a comparable representation.

Accent-insensitive search should be considered.

For a large dataset, investigate SQLite FTS rather than loading the complete dataset into memory.

Do not prematurely optimize before measuring.

---

# 19. Progress Calculations

Overall progress:

```text
visitedEligiblePlaces / totalEligiblePlaces
```

Example:

```text
152 / 4,281
= 3.55%
```

The numerator and denominator must use the same dataset version and eligibility rule.

Progress queries should be implemented in the repository/domain layer rather than directly in UI code.

---

# 20. Map Architecture

The map provider is intentionally not hard-coded into the product requirements.

Before implementation, evaluate:

* Google Maps
* MapLibre
* Other suitable providers

Criteria:

* Android support
* Licensing
* Offline support
* Cost
* Marker performance
* Clustering
* Spain coverage
* Long-term viability
* Ability to avoid mandatory user accounts

The final decision must be documented.

---

# 21. Map Performance

Do not render thousands of individual Compose markers without investigating performance.

Consider:

* Marker clustering
* Viewport-based querying
* Spatial filtering
* Database bounding-box queries
* Simplified map representations

Only load places relevant to the visible map area where appropriate.

---

# 22. Location

Location is optional.

Potential Android architecture:

```text
Location Provider
       ↓
Location Repository
       ↓
Domain
       ↓
UI / Visit confirmation
```

Do not make location a requirement for basic application functionality.

The app must work without location permission.

---

# 23. Location Visit Detection

Future architecture should support:

```text
candidate place
+
device location
+
distance calculation
+
minimum dwell time
+
user confirmation
```

Avoid implementing automatic visit detection based only on a simple radius check.

A future implementation must consider:

* GPS accuracy
* Urban density
* Roads passing near villages
* Highways
* Brief drive-throughs
* Background execution
* Battery consumption
* Permission restrictions

---

# 24. Privacy

MVP user data:

```text
Visits
Preferences
Optional location evidence
```

should remain local.

No server-side user profile is required.

Do not introduce analytics that collect precise location or visit history without an explicit product decision.

---

# 25. Preferences

Use DataStore for small application preferences.

Examples:

```text
map style
population threshold
default filters
theme
onboarding completed
```

Do not use DataStore as the primary store for the village dataset or visits.

---

# 26. Error Handling

The UI should distinguish between:

```text
Loading
Success
Empty
Error
Offline
```

Do not expose raw exceptions directly to users.

Repositories should convert technical failures into appropriate domain-level states.

---

# 27. Testing Strategy

## Unit tests

Test:

* Eligibility calculation
* Search normalization
* Progress calculation
* Visit creation
* Duplicate visit handling
* Filtering
* Geographic distance calculations
* Dataset validation

## Database tests

Test:

* Insert
* Query
* Search
* Filtering
* Visit persistence
* Migrations
* Foreign keys

## UI tests

Test critical flows:

```text
Open app
Search
Open place
Mark visited
Return
Verify visited state
```

---

# 28. Build Quality

Before considering a feature complete:

```text
./gradlew test
./gradlew lint
./gradlew assembleDebug
```

The exact commands may vary according to the Gradle configuration.

No feature should be considered complete with known compilation errors.

---

# 29. Security

Do not store secrets in the repository.

API keys must never be hard-coded into source code.

If a map provider requires a key:

* Use appropriate Android configuration.
* Do not commit private secrets.
* Document required setup.
* Evaluate key restrictions.

---

# 30. Architecture Decision Records

Major decisions should be recorded.

Examples:

```text
ADR-001 Geographic unit
ADR-002 Map provider
ADR-003 Database structure
ADR-004 Dataset update strategy
ADR-005 Automatic visit detection
```

These can eventually live under:

```text
docs/adr/
```

---

# 31. Current Authoritative Data Strategy

Primary population source:

```text
INE Nomenclátor: Población por Unidad Poblacional
```

Primary geographic/reference source:

```text
Instituto Geográfico Nacional
Nomenclátor Geográfico
```

The exact source files, download dates, transformations and validation results must be recorded in:

```text
docs/data-sources.md
```

Never silently replace authoritative data with an unofficial list.

---

# 32. Important Constraint

Do not begin by creating a final Room schema based on assumptions about "village".

First complete:

```text
Geographic research
        ↓
Canonical unit decision
        ↓
Sample dataset
        ↓
Validation
        ↓
Database design
```

This is one of the highest-risk decisions in the project.
