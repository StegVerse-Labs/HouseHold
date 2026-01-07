# HouseHold

HouseHold is a **real-world incident + projects repository** used to track home and consumer events with:
- structured timelines
- findings and constraints
- evidence organization
- escalation-ready letter packets (HEE-style)

It is designed to work *with* the **Household Escalation Engine (HEE)** templates so that any incident can be packaged into a predictable “send-ready” packet with links to supporting documentation.

---

## How to use this repo

Each incident (water heater, automotive, etc.) gets its own folder with a consistent layout:
- `photos/`, `estimates/`, `contract/`, `attachments/`
- `findings/` (what we know + what constraints exist)
- `timeline/` (dated entries)
- `warranty/` (excerpts + claim logic + buyout letters)
- optional `escalation/` folders for send-ready packets

The goal: **reduce mental fatigue** and make escalation easy, repeatable, and provable.

---

## Repository Structure (current)

### `HEE/`
The local Household Escalation Engine workspace for templates/specs.

- `HEE/engine/packet-spec.md`  
  Defines what a “packet” is and what it must include.

- `HEE/intake/intake_questionnaire.md`  
  A standard intake form to capture facts once.

- `HEE/templates/automotive/`
  Reusable templates for automotive escalations:
  - `escalation-profile.md`
  - `evidence-manifest.yml`
  - `definition.md`
  - `level-1-letter.md`
  - `level-2-letter.md`
  - (template scaffold file(s) as shown in repo)

> This structure can be replicated for other domains (home warranty, appliances, contractors, insurance, etc.).

---

### `_new-incident-template/`
Starter template for creating new incidents quickly:
- `timeline/initial-observations.md`

---

## Incidents

### `water-heater-replacement/`
Tracks the water heater failure, warranty interaction, estimates, and replacement constraints.

Key subfolders:
- `attachments/comms/` — appointment emails, reminders, receipts, messages
- `contract/` — policy documents (e.g., `Choice.Home.Warranty-2022.pdf`)
- `estimates/` — independent estimates (e.g., screenshot `IMG_1471.png`)
- `photos/` — images of plumbing/sinks/conditions

Key working docs:
- `findings/`
  - `alternative-replacement-plan.md`
  - `replacement-constraints.md`
  - `safety-assessment.md`
  - `system-configuration.md`
  - `warranty-resolution-options.md`
- `timeline/`
  - `2025-01-02__photos-index.md`
  - `2025-01-02__user-observations.md`
  - `2025-01-03__plumber-estimate-1.md`
  - `2025-01-03__warranty-communication.md`
  - `2025-01-04__permit-office-notes.md`
  - `2025-01-04__reddit-community-feedback.md`
- `warranty/`
  - `choice-home-warranty-excerpts.md`
  - `choice-buyout-request.md`

---

### `corvette-c8-transmission/`
Tracks the C8 transmission failure timeline, custody, discrepancies, and escalation letters.

Key subfolders:
- `custody/`
  - `custody-ledger.md`
- `findings/`
  - `impacts-and-losses.md`
  - `loss-of-use-worksheet.md`
  - `questions-for-dealer-and-gm.md`
  - `remedy-goals.md`
- `provenance/`
  - `service-history-carfax.md`
  - `storage-conditions.md`
  - `transmission-replacement-discrepancy.md`
  - `vehicle-identity-and-serials.md`
- `timeline/`
  - `2022-12__purchase.md`
  - `2023-03__failure-and-tow.md`
  - `2023-03__to_2023-08__dealer-custody.md`
  - `2023-08__pickup.md`
  - `evidence-index.md`

Escalation packet folders:
- `escalation/level-1-dealer-gm/` (README + attachments + letter)
- `escalation/level-2-gm-corporate/` (README + attachments + letter)
- `escalation/level-3-state/` (README + letter)

---

## What belongs where

### Put facts in:
- `timeline/YYYY-MM-DD__<event>.md`

### Put “what we think it means” in:
- `findings/`

### Put supporting evidence in:
- `photos/`, `estimates/`, `attachments/`, `contract/`

### Put send-ready materials in:
- `escalation/level-X-*/`
  - `letter.md` — the message being sent
  - `README.md` — “packet index” with links
  - `attachments.md` — explicit list of what’s included and why

---

## Recommended small improvements (non-breaking)

1. **Add an `index.md`** in each incident root that links to:
   - latest timeline entry
   - the “current ask” (e.g., buyout request)
   - the current escalation packet folder

2. **Standardize naming for escalation folders**
   - `level-1-<target>/`, `level-2-<target>/`, etc. (already mostly done)

3. **Keep evidence pointers stable**
   - Avoid renaming photos after referenced in timelines/letters.
   - Prefer an `evidence-index.md` (already present in Corvette incident).

---

## Safety / Privacy Notes

HouseHold is often “real life” and can include private data.
If this repo is public:
- redact addresses, phone numbers, email headers, account numbers
- avoid full PDFs unless scrubbed
- consider moving sensitive artifacts into a private companion repo

---

## Why this matters

HouseHold is the proving ground for HEE:
- real incidents
- real fatigue constraints
- real escalation pressure

If we can make this workflow easy and repeatable here, it generalizes into a marketable engine for warranties, contractors, automotive disputes, appliances, and more.

---
