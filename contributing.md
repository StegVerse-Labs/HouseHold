# Contributing to HouseHold

HouseHold is a **real-world incident repository**.
It is designed to reduce cognitive load during stressful situations by enforcing structure and traceability.

This repo values **clarity over cleverness**.

---

## What This Repo Is

- A timeline-driven record of events
- A place to store findings and constraints
- A staging ground for escalation packets
- A proving ground for the Household Escalation Engine (HEE)

---

## What This Repo Is NOT

- A legal filing system
- A replacement for professional advice
- A dumping ground for unorganized files

---

## Adding a New Incident

1. Copy `_new-incident-template/`
2. Rename it to a descriptive incident folder
3. Populate:
   - `timeline/initial-observations.md`
   - evidence folders as applicable
4. Add a short `README.md` summarizing the incident

---

## Writing Timeline Entries

Timeline entries must:
- Be dated in filename (`YYYY-MM-DD__description.md`)
- Contain only observed facts
- Avoid conclusions or accusations

Interpretation belongs in `findings/`.

---

## Findings vs Evidence

### Evidence
- Photos
- PDFs
- Receipts
- Messages

Stored in:
- `photos/`
- `attachments/`
- `contract/`
- `estimates/`

### Findings
- Analysis
- Constraints
- Risks
- Options

Stored in:
- `findings/`

---

## Escalation Packets

Escalation folders are **send-ready** bundles.

Each level must include:
- `letter.md`
- `README.md` (packet index)
- `attachments.md` (explicit evidence list)

Nothing enters escalation without being traceable to evidence.

---

## Privacy & Safety

Before committing:
- Redact personal identifiers
- Remove metadata if necessary
- Avoid publishing sensitive PDFs unless scrubbed

HouseHold can be public or private — structure must work either way.

---

## Philosophy

When stress is high, structure is mercy.

If something feels confusing:
- Split it
- Date it
- Link it

---
