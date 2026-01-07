# Contributing to HouseHold

Welcome to **HouseHold**, the primary **real-world proving ground** for StegVerse
escalation, evidence, and custody protocols.

HouseHold demonstrates how StegDB protocols and the HEE engine work
against actual consumer incidents.

---

## 🧭 HouseHold’s Role

HouseHold exists to:

- Track real incidents (warranties, repairs, custody disputes)
- Organize evidence and timelines
- Generate escalation packets
- Demonstrate HEE in practice

HouseHold **does not define protocols**.
It **consumes** them.

---

## 📁 Repository Structure Rules

Each incident folder represents **one real-world event**.

Example:
  `water-heater-replacement/**`

Rules:
- One incident per folder
- No mixing unrelated issues
- All claims must be traceable to evidence

---

## 📄 What You May Edit Freely

You may add or update:
- Timelines
- Findings
- Evidence references
- Incident README summaries
- Generated escalation packets

These reflect **state**, not protocol.

---

## 🚫 What You Must NOT Duplicate

Do **not** copy or redefine:
- Evidence confidence rules
- Custody transition logic
- Escalation level definitions
- Letter templates

These are defined in:
- `StegDB/protocols/**`
- `HouseHold/HEE/templates/**`

Incidents should **reference**, not redefine.

---

## ✉️ Escalation Packets

Escalation folders (`/escalation/level-*`) must:

- Be complete and send-ready
- Contain:
  - `letter.md` (generated)
  - `attachments.md`
  - `README.md` explaining escalation context
- Reference canonical protocols

Letters should never be handwritten when a template exists.

---

## 🧾 Evidence Handling

Evidence must:
- Be indexed
- Be traceable to ingestion
- Respect confidence scoring expectations

If evidence cannot meet minimum confidence thresholds, it should:
- Be flagged
- Or excluded from escalation packets

---

## 🔄 Custody Awareness

Custody changes, access attempts, or ambiguity:
- Should be documented
- May trigger notification events
- Must never be silently altered

HouseHold demonstrates **custody awareness**, not enforcement logic.

---

## 🧠 Design Philosophy

- Incidents are state, not structure
- Templates live once
- Protocols are referenced, not copied
- Escalation should reduce cognitive load, not increase it

HouseHold proves that the system works under pressure.

---

## 📬 Questions & Contributions

If you’re unsure where something belongs:
- Ask first
- Or prototype locally before committing

Your contributions help turn real-world frustration
into verifiable, resolvable outcomes.
