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
