# Product Requirements — Spanish Villages

## 1. Product Definition

Spanish Villages is an Android application that allows users to discover Spanish villages and population centres and maintain a personal record of places they have physically visited.

The primary user outcome is:

> "I can see which Spanish villages I have visited, which I haven't, and explore what remains."

---

# 2. Core User Loop

```text
Discover
   ↓
Explore
   ↓
Visit
   ↓
Mark as visited
   ↓
Track progress
   ↓
Discover next place
```

Every MVP feature should support this loop.

---

# 3. Target User

The primary user is someone interested in travelling around Spain and progressively visiting smaller towns, villages and population centres.

Potential motivations include:

* Exploring rural Spain
* Road trips
* Personal travel history
* Geographic exploration
* Completing a personal list
* Discovering less-known places

The product does not need to assume competitive behaviour.

---

# 4. Geographic Definition

## 4.1 Problem

"Village" is not a sufficiently precise Spanish statistical/geographic concept.

A municipality can contain:

* One settlement
* Multiple settlements
* Multiple entities
* Multiple nuclei
* Dispersed population

Therefore:

```text
municipio != village
```

The product must not use municipality population as a proxy for village population.

---

## 4.2 Candidate Units

The product must evaluate:

### Municipio

Administrative local-government unit.

Useful for:

* Administrative filtering
* Municipality relationships
* Geographic hierarchy

Not necessarily equivalent to a village.

### Entidad singular de población

An area within a municipality that is clearly differentiated and has a specific name.

This is a strong candidate for the application's conceptual "place".

### Núcleo de población

A more physically concentrated settlement within an entity singular.

This may be more appropriate when the product intends to represent an actual physical settlement rather than a broader named population entity.

### Diseminado

Dispersed buildings/houses that do not form a population nucleus.

The default product should NOT treat a diseminado as a village.

---

## 4.3 Initial Product Decision

The canonical model should support both:

```text
Population Entity
    └── Population Nucleus
```

rather than prematurely collapsing them.

The initial eligible-place dataset should be derived from authoritative INE population-unit data.

The product team must explicitly decide whether the user-facing "village" corresponds to:

1. Entity singular
2. Nucleus
3. A normalized combination of entity + nucleus

This decision must be recorded in `docs/geographic-model.md` before the production dataset is frozen.

---

# 5. Eligibility

An eligible place is initially defined as:

```text
Spanish population centre
AND
population < 10,000
AND
not a diseminado
```

The population reference date must be stored.

Example:

```text
population: 4,283
populationReferenceDate: 2025-01-01
```

The threshold is configurable at the data-processing level, but the initial product value is:

```text
10,000 inhabitants
```

---

# 6. Administrative Hierarchy

The application should represent:

```text
Autonomous Community
    ↓
Province
    ↓
Municipality
    ↓
Population Entity
    ↓
Population Nucleus
```

Not every geographic unit will necessarily have every level.

The model must support regional differences in Spanish administrative/geographic structures.

---

# 7. MVP Features

## 7.1 Browse

Users can browse eligible places.

Each place should display at minimum:

* Name
* Municipality
* Province
* Autonomous community
* Population
* Visited status

---

## 7.2 Search

Users can search by:

* Place name
* Municipality
* Province
* Autonomous community

Search should work offline against the local database.

Search must tolerate:

* Upper/lower case
* Accents
* Common spelling variations where appropriate

Do not silently merge distinct geographic entities solely because their names match.

---

## 7.3 Map

Users can see eligible places geographically.

Map functionality should support:

* Place markers
* Visited/unvisited visual distinction
* Selecting a place
* Opening place details
* Filtering visible places

The map must not be the only way to access the dataset.

---

## 7.4 Place Detail

A place detail screen should show:

* Name
* Population
* Population reference date
* Municipality
* Province
* Autonomous community
* Coordinates where available
* Visited status
* Visit history

Future fields may include:

* Elevation
* Photos
* Notes
* External references

These are not MVP requirements.

---

# 8. Mark as Visited

Users must be able to manually mark a place as visited.

The primary interaction should be simple:

```text
Mark as visited
```

The application should record:

* Visit timestamp
* Visit method = MANUAL
* Place identifier

The user should be able to undo/remove a visit.

---

# 9. Multiple Visits

The data model should support multiple visits to the same place even if the MVP UI initially focuses on visited/unvisited status.

Example:

```text
Albarracín
    Visit 1 — 2026-05-12
    Visit 2 — 2027-08-21
```

The place's visited state is:

```text
visited = true
```

as long as at least one valid visit exists.

---

# 10. Location-Based Visits

Location-based visit detection is a future feature.

Potential future behaviour:

```text
User enters geographic area
        ↓
Application detects proximity
        ↓
Potential visit generated
        ↓
User confirms
        ↓
Visit recorded
```

The application must NOT automatically declare a visit simply because the device passed near a location unless that behaviour is explicitly designed and tested.

Location permissions must remain optional.

---

# 11. Filters

The application should eventually support:

* Visited / unvisited
* Autonomous community
* Province
* Municipality
* Population range
* Distance from current location
* Map viewport

MVP filters should be implemented incrementally.

---

# 12. Progress

The application should provide personal statistics such as:

### Overall

```text
Visited: 152
Eligible: 4,281
Progress: 3.55%
```

### By province

```text
Madrid: 23 / 91
Ávila: 18 / 143
...
```

### By autonomous community

```text
Castilla y León: 84 / 1,200
Aragón: 21 / 523
...
```

Statistics must always use the same dataset version and eligibility rules.

---

# 13. Visit History

Users should be able to view their visits chronologically.

Example:

```text
12 September 2026
  Albarracín
  Teruel

10 September 2026
  Chinchón
  Madrid
```

History must remain available independently of whether the device is online.

---

# 14. Offline Requirements

The following must work offline:

* Browse
* Search
* Filter
* View place details
* Mark visited
* Remove visit
* View visit history
* View progress

Internet may be required for:

* Initial dataset download, if applicable
* Map tiles not stored locally
* Future external information
* Dataset updates

---

# 15. Privacy Requirements

The MVP should not require an account.

User data should be stored locally.

The application must not transmit:

* Visit history
* Current location
* Location history

to a backend unless a future requirement explicitly introduces such functionality.

Location permission must be requested only when necessary.

---

# 16. Data Updates

The geographic dataset will change over time.

Changes may include:

* Population
* Names
* Administrative relationships
* Added places
* Removed places
* Geographic corrections

User visits must be linked to stable geographic identifiers wherever possible.

A dataset update must not wipe user history.

---

# 17. Non-Goals for MVP

The following are explicitly out of scope:

* Social network
* Public profiles
* User accounts
* Friends
* Following
* Comments
* Messaging
* Leaderboards
* Competitive rankings
* Achievements
* Advertising
* Subscription system
* Cloud synchronization
* User-generated village creation
* Automatic background tracking

These can be reconsidered later.

---

# 18. UX Principles

The application should:

* Require minimal taps
* Make visited state immediately obvious
* Work well outdoors
* Remain useful with poor connectivity
* Avoid unnecessary onboarding
* Avoid aggressive gamification
* Make geographic context obvious
* Use clear Spanish geographic terminology

---

# 19. Accessibility

The app should support:

* Dynamic text sizing
* Adequate touch targets
* Screen readers
* Sufficient contrast
* Meaningful content descriptions
* Non-colour-only visited indicators

---

# 20. Acceptance Criteria for MVP

The MVP is complete when a new user can:

1. Open the application.
2. Browse Spanish eligible places.
3. Search for a place.
4. Open its details.
5. See its geographic context.
6. Mark it visited.
7. Close and reopen the application.
8. See that it remains visited.
9. View their visit history.
10. View overall progress.
11. Use the core functionality without an internet connection.

---

# 21. Product Decision Log

Important product decisions must be documented here or in `docs/`.

Decisions should include:

* Definition of village
* Eligibility threshold
* Treatment of entities vs nuclei
* Treatment of diseminados
* Population reference date
* Treatment of deleted/renamed places
* Multiple-visit behaviour
* Automatic visit detection rules
