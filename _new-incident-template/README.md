# New Incident Template

This directory defines the reusable starting structure for a HouseHold incident.

Copy the template to a new kebab-case directory. Do not modify this template to represent a specific incident.

## Authority Boundary

- StegDB defines canonical protocols and schemas.
- HEE supplies reusable intake, validation, and escalation patterns.
- An incident directory contains only incident state, evidence references, findings, and reviewed packet output.

Do not duplicate custody, confidence, notification, or escalation rules inside an incident.

## Recommended Incident Layout

```text
incident-name/
├── README.md
├── timeline/
├── findings/
├── attachments/
│   └── comms/
├── photos/
├── estimates/
├── contract/
├── custody/
├── provenance/
└── escalation/
    ├── level-1-<target>/
    ├── level-2-<target>/
    └── level-3-<authority>/
```

Only create folders the incident needs. Existing incidents do not need destructive migration to match this example.

## Start a New Incident

1. Copy `_new-incident-template/`.
2. Rename the copy using a clear kebab-case name.
3. Write an incident summary in `README.md`.
4. Record the first dated observation in `timeline/`.
5. Add supporting artifacts without renaming or overwriting originals after they are referenced.
6. Record interpretation, risks, constraints, impacts, and remedy analysis in `findings/`.
7. Create an escalation directory only when a packet is being prepared.

## Facts and Analysis

Use `timeline/` for dated observations and events:

- what happened;
- when it happened;
- who communicated or acted;
- which source records the event.

Use `findings/` for analysis:

- what the records may mean;
- inconsistencies or missing information;
- safety, cost, loss-of-use, or reliability impacts;
- remedy goals and alternatives.

State uncertainty explicitly. Do not present an inference as an observed fact.

## Evidence Handling

- Preserve originals.
- Reference artifacts by stable filename or artifact identifier.
- Record transformations and redactions.
- Use hashes and manifests where available.
- Do not annotate or modify an original merely to support a claim.
- Treat confidence metadata as decision support, not proof or authentication.

Custody describes handling or responsibility and is separate from provenance, truth, ownership, authority, and liability.

## Escalation Readiness

A packet may be prepared when:

- the requested remedy is clear;
- material claims point to supporting records;
- attachments are enumerated;
- known uncertainty and excluded evidence are visible;
- the packet has an explicit review state.

A typical packet contains:

```text
level-n-<target>/
├── README.md
├── letter.md
├── attachments.md
└── packet.yml        # optional machine-readable manifest
```

Generated material remains a draft until a human reviewer confirms the recipient, factual statements, attachments, remedy, and delivery method.

## Privacy

Do not commit credentials, tokens, unnecessary personal identifiers, account numbers, signatures, or unredacted private communications. Use synthetic fixtures for public automation tests.

See the repository `SECURITY.md` and `CONTRIBUTING.md` before publishing evidence or automation changes.
