# HEE — Household Escalation Engine

HEE is the reusable implementation layer that helps turn HouseHold incident records into structured, reviewable escalation packets.

StegDB defines canonical protocols and schemas. HouseHold contains real incident state. HEE connects the two without changing the underlying facts or replacing human judgment.

## What HEE Provides

- intake structure;
- packet and manifest patterns;
- evidence-reference and validation guidance;
- custody-aware documentation patterns;
- confidence-aware decision support;
- graduated escalation templates;
- deterministic tooling and CI validation as those components are implemented.

## What HEE Does Not Do

HEE does not:

- authenticate evidence by itself;
- decide legal rights, liability, or outcomes;
- replace attorneys, regulators, contractors, mechanics, or other professionals;
- convert a custody record into proof of ownership or authority;
- guarantee resolution;
- send external communications without explicit authorization and review.

## Layer Responsibilities

| Layer | Responsibility |
|---|---|
| StegDB | Canonical protocols, schemas, versioning, validation rules, and compatibility requirements |
| HEE | Reusable intake, validation, manifest, and packet-generation implementation |
| HouseHold incident | Real observations, evidence references, findings, custody/provenance records, remedies, and reviewed output |

Rules that apply across repositories belong in StegDB. Reusable implementation belongs in HEE. Statements about a specific real-world matter belong in its HouseHold incident folder.

## Incident Flow

```text
intake
→ timeline and evidence organization
→ findings and remedy goals
→ custody/provenance review
→ packet planning
→ evidence and confidence review
→ human approval
→ external delivery outside HEE
```

No stage should silently rewrite the records produced by an earlier stage.

## Evidence, Confidence, and Custody

HEE records what exists and what factors affect how a record may be used.

- Evidence references identify source material.
- Provenance records describe origin and history.
- Custody records describe handling or responsibility.
- Confidence records disclose transparent factors, limitations, and overrides.

These records support review. None independently proves authenticity, truth, ownership, authority, liability, or admissibility.

Original evidence should remain unchanged. Transformations, redactions, generated derivatives, and custody events should be recorded rather than hidden.

## Escalation Levels

Escalation is graduated and target-specific.

```text
level-1-<target>/      direct provider, dealer, contractor, or warranty channel
level-2-<target>/      management, corporate, manufacturer, or executive channel
level-3-<authority>/   regulator, licensing body, attorney general, arbitration, or another formal channel
```

Skipping a level requires an incident-specific reason. Level names do not confer legal status or guarantee that a recipient has jurisdiction.

## Packet Contract

A typical packet contains:

```text
level-n-<target>/
├── README.md
├── letter.md
├── attachments.md
└── packet.yml        # optional machine-readable manifest
```

The packet should state:

- incident and target;
- requested remedy;
- material claims and their supporting references;
- included and excluded evidence;
- known uncertainty;
- preparation date;
- review state;
- delivery state, when applicable.

A generated packet is a draft. It becomes send-ready only after a human reviewer confirms the recipient, factual statements, attachments, requested remedy, dates, and delivery method.

## Automation Constraints

HEE automation must:

- begin with validation and dry-run behavior;
- preserve original evidence;
- avoid moving or overwriting files by default;
- use synthetic fixtures in CI;
- fail clearly when required inputs or canonical rules are missing;
- record hashes, manifests, exclusions, transformations, and review state;
- never auto-send a letter or notification merely because generation succeeded.

Canonical synchronization from StegDB must be overlay-only and must not replace incident evidence or unrelated working outputs.

## Current Repository Components

The repository currently includes:

- `household-escalation-engine.md` — foundational HEE principles;
- `engine/packet-spec.md` — packet specification work;
- `intake/intake_questionnaire.md` — intake guidance;
- `templates/automotive/` — automotive template examples.

Implementation status and the exact next authorized task are preserved in `../HOUSEHOLD_MIRROR_HANDOFF.md`.

## Design Principles

- evidence before argument;
- facts separated from analysis;
- custody separated from truth;
- transparency over false certainty;
- calm, incremental escalation;
- review before delivery;
- history survives transfer of responsibility.
