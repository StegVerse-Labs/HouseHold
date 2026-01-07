# New Incident Template (HouseHold)

This folder defines the **canonical structure** for any real-world incident
tracked in the HouseHold repository.

⚠️ **This folder is a TEMPLATE.**
It is never modified for a specific incident.
It is copied to create new incident folders.

---

## Purpose

- Enforce consistency across incidents
- Reduce cognitive load during stressful events
- Ensure escalation packets are complete and defensible
- Keep HouseHold aligned with StegDB / HEE protocols

---

## How to Use

1. Copy `_new-incident-template/`
2. Rename it to a descriptive incident name (kebab-case)

Example:
```txt
   water-heater-replacement/
```
3.	Populate files incrementally as information becomes available
4.	Do not alter folder names or meanings

##Canonical Incident Layout
```txt
incident-name/
├── attachments/
│   ├── comms/            # Emails, texts, call summaries
│   └── .gitkeep
├── photos/               # Photos/videos (referenced, not interpreted)
│   └── .gitkeep
├── estimates/            # Contractor or vendor estimates
│   └── .gitkeep
├── contract/             # Warranty, purchase, service contracts
│   └── .gitkeep
├── findings/             # Analysis, constraints, risk, conclusions
│   ├── safety-assessment.md
│   ├── system-configuration.md
│   └── .gitkeep
├── timeline/             # Date-stamped factual records
│   └── YYYY-MM-DD_event.md
├── escalation/           # Send-ready escalation packets
│   ├── level-1/
│   ├── level-2/
│   └── level-3/
├── README.md              # Incident overview + navigation
```

Folder Rules (Non-Negotiable)

One Incident = One Folder
	•	Do not combine unrelated issues
	•	Do not reuse folders

Facts vs Analysis
	•	timeline/ → what happened, when, by whom
	•	findings/ → interpretation, constraints, risks, conclusions

No Protocol Redefinition
	•	Do not redefine custody, confidence, or escalation rules
	•	Protocols live in StegDB
	•	Incidents apply them

⸻

Evidence Handling
	•	Evidence files live in folders
	•	Claims about evidence live in Markdown
	•	Do not annotate photos directly
	•	Reference evidence by filename and date

⸻

Escalation Readiness

An incident is considered escalation-ready when:
	•	Timeline is complete
	•	Findings justify the remedy sought
	•	All referenced evidence exists
	•	Escalation folder contains:
	•	letter.md
	•	README.md (links + checklist)

⸻

What Does NOT Go Here

❌ Legal advice
❌ Emotional commentary
❌ Duplicated protocol text
❌ Private credentials

⸻

Why This Exists

When stress is high, structure must already exist.

This template ensures:
	•	Nothing important is forgotten
	•	Every claim is traceable
	•	Escalation is fast, calm, and credible

  ---

# 📄 `HouseHold/HEE/README.md`

```md
# HEE — Household Escalation Engine

HEE defines **how incidents become action**.

StegDB defines the protocol.
HouseHold proves it in real life.

---

## What HEE Is

HEE is a **pattern**, not a product.

It provides:
- Intake structure
- Evidence manifests
- Escalation packet templates
- Confidence-aware documentation flow

HEE does **not**:
- Decide legal outcomes
- Replace attorneys
- Alter facts
- Guarantee success

---

## HEE Scope in HouseHold

HouseHold uses HEE to:
- Standardize incident documentation
- Generate escalation packets
- Reduce decision fatigue
- Preserve custody and confidence

HouseHold does **not** define:
- Custody protocol
- Confidence scoring logic
- Notification rules

Those live in **StegDB**.

---

## Relationship to StegDB

| Layer | Responsibility |
|-----|---------------|
| StegDB | Protocols, schemas, rules |
| HouseHold | Real incidents using those rules |
| HEE | The bridge between the two |

If something feels like a “rule” → it belongs in StegDB  
If something feels like “this happened” → it belongs in HouseHold  

---

## HEE Intake Pattern

Each incident:
- Is created from `_new-incident-template/`
- Accumulates evidence
- Produces findings
- Optionally escalates

Nothing skips steps.

---

## Escalation Levels

Escalation is **graduated**, not emotional.

```txt
escalation/
├── level-1/   # Vendor / warranty / dealer
├── level-2/   # Corporate / executive
├── level-3/   # Regulator / AG / formal dispute

Each level is:
	•	Self-contained
	•	Send-ready
	•	Justified by evidence

⸻

Escalation Packet Requirements

Every escalation folder must contain:

level-n/
├── letter.md      # The message being sent
├── README.md      # Why + what’s attached
├── attachments.md # Explicit attachment list

No attachments = no escalation.

⸻

Confidence & Custody

HouseHold:
	•	Records what exists
	•	Notes confidence limits
	•	Does not fabricate certainty

StegDB:
	•	Defines how confidence is scored
	•	Defines custody transitions
	•	Defines notification behavior

⸻

Design Principles
	•	Calm over force
	•	Evidence over argument
	•	Structure over memory
	•	Traceability over volume

⸻

Why HEE Matters

Most warranty and dispute failures happen because:
	•	Documents are scattered
	•	Facts are mixed with opinion
	•	People burn out before escalation

HEE exists to prevent that.

⸻

Future Direction

HEE is designed to scale into:
	•	Consumer services
	•	Asset lifecycle tracking
	•	Custody-aware transfers
	•	Automated escalation generation

HouseHold is the proving ground
