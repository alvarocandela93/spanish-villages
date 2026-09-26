# Monetization Strategy

## 1. Philosophy

Spanish Villages should remain a free application.

The purpose of monetization is to help cover development, data, infrastructure and maintenance costs without compromising the core user experience.

The application should not require payment to:

* Discover villages
* Search villages
* View villages
* Mark villages as visited
* View visit history
* View core statistics
* Use the core offline functionality

---

# 2. Monetization Model

The initial monetization model consists of:

1. Advertising
2. Optional user donations

There will be no:

* Subscription
* Premium tier
* Paywall
* Paid village dataset
* Paid visit tracking
* Paid account
* Required registration

---

# 3. Advertising

Advertising may be used to generate revenue from users who do not make donations.

Ads should be implemented in a way that minimizes disruption.

Potential locations:

* Village browsing/list screens
* Non-critical informational screens
* Statistics screen where appropriate

Avoid placing advertisements:

* On top of active map navigation
* Immediately after marking a village visited
* During location detection
* Between critical visit-tracking actions
* In situations where the user may be driving
* In a way that interferes with geographic information

The exact ad placement should be tested with real usage before release.

---

# 4. Ad Technology

The implementation should use a reputable Android-compatible advertising SDK.

The advertising provider must be evaluated based on:

* Android support
* Google Play compliance
* Privacy requirements
* Consent requirements
* Performance
* Ad formats
* Revenue potential
* Ability to disable ads if required in the future

The advertising SDK must remain isolated from core application logic.

Do not reference ad SDK classes from:

* Domain models
* Domain use cases
* Village repositories
* Visit repositories
* Geographic data processing
* Core business logic

---

# 5. Ad Abstraction

Where practical, use an application-level abstraction.

Conceptually:

```text
AdService
    |
    ├── showBanner()
    ├── showInterstitial()
    └── isAvailable()
```

The rest of the application should not need to know which advertising provider is being used.

This allows the advertising provider to be replaced without modifying core application functionality.

---

# 6. Donations

Users may voluntarily support the project.

The donation system must not unlock essential functionality.

A donation is an optional contribution rather than a purchase of application functionality.

Possible future donation amounts may include:

* Small contribution
* Medium contribution
* Large contribution

The exact amounts and implementation will be decided before release.

---

# 7. Donation UX

A support option may appear in:

* Settings
* About
* App information
* A dedicated "Support the project" section

It should not interrupt normal village exploration.

Suggested messaging:

> Enjoying Spanish Villages?
> If the app helps you discover more of Spain, you can support its continued development.

The user should never be repeatedly prompted to donate after declining.

---

# 8. Donation Technology

The donation mechanism should use a platform-supported and policy-compliant payment mechanism.

Before implementation, evaluate:

* Google Play Billing
* External donation platforms
* Associated Google Play policies
* Fees
* User experience
* Regional availability
* Tax/legal requirements

Do not implement a payment provider until the requirements and Google Play policies have been verified.

---

# 9. Privacy

Advertising must not compromise the application's privacy-first principle.

The application should minimize data collection.

In particular:

* Do not send visit history to advertising providers.
* Do not send precise user location to advertising providers.
* Do not use village visits as advertising-targeting data.
* Do not make the user's personal travel history part of an advertising profile.

Any consent requirements associated with personalized advertising must be handled explicitly.

---

# 10. Offline Behaviour

The core application must work offline regardless of advertising availability.

If advertisements cannot be loaded:

```text
App continues normally.
```

There should be no requirement to have an active internet connection simply to:

* Search villages
* Mark a visit
* View visit history
* Calculate progress

---

# 11. Architecture

Monetization is an infrastructure concern and must remain separate from the core domain.

Conceptually:

```text
UI
 │
 ├── Core application functionality
 │
 └── Monetization UI
       │
       ├── AdService
       │
       └── DonationService
```

The domain layer must not depend on advertising or donations.

---

# 12. Future Flexibility

The architecture should allow future changes such as:

* Removing ads
* Changing advertising provider
* Adding a "remove ads" purchase
* Adding optional premium functionality
* Changing donation provider

without redesigning:

* Village data
* Visit data
* Geographic model
* Database
* Core domain logic

These possibilities should not be implemented unless explicitly required.

---

# 13. Product Principle

Monetization must never change the fundamental promise of the application:

> Users should be able to freely discover and record the Spanish villages they have visited.
