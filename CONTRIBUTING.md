# Contributing to HouseHold

HouseHold is a real-world incident and project repository and the proving ground for the Household Escalation Engine (HEE).

Contributions must preserve incident integrity, privacy, and the boundary between canonical protocols and local implementation.

## Authority Boundary

- **StegDB** defines canonical protocols, schemas, custody semantics, notification requirements, and evidence-confidence rules.
- **HEE** implements those rules as reusable intake, validation, and escalation patterns.
- **HouseHold incidents** contain real event state, evidence references, timelines, findings, and reviewed escalation packets.

Do not redefine canonical protocol behavior inside an incident folder.

## Incident Structure

Each incident folder represents one real-world matter.

- Put dated observations and events in `timeline/`.
- Put interpretation, constraints, impacts, risks, and remedy analysis in `findings/`.
- Put supporting artifacts in the applicable evidence folders.
- Put externally deliverable material in `escalation/` only after review.

Do not combine unrelated incidents or silently rename evidence after it has been referenced.

## Evidence and Claims

A claim must point to an identifiable source, record, or observation.

- Preserve original files.
- Record transformations rather than overwriting originals.
- Use hashes, manifests, and stable paths where available.
- State uncertainty and missing context explicitly.
- Treat confidence metadata as decision support, not authentication, proof, or a legal conclusion.

Custody records describe handling or responsibility. They do not independently establish truth, ownership, authority, or liability.

## Escalation Material

Escalation packets should contain:

- `letter.md`
- `attachments.md`
- `README.md` or another packet index
- a review state indicating whether the packet is draft, reviewed, or sent

Generated output is a draft until a human reviewer confirms the recipient, factual statements, attachments, requested remedy, and delivery method.

Do not automate external delivery from this repository without a separately authorized and reviewed workflow.

## Privacy and Security

Before committing:

- Remove credentials, tokens, account numbers, and unnecessary personal identifiers.
- Redact addresses, phone numbers, email headers, signatures, vehicle identifiers, and contract identifiers when public disclosure is unnecessary.
- Prefer safe references, hashes, or synthetic fixtures in public examples.
- Never copy private incident evidence into StegDB.

See `SECURITY.md` for reporting and remediation guidance.

## Change Discipline

- Use additive or exact-file updates.
- Do not perform full-folder replacement.
- Preserve existing incident evidence, templates, papers, references, submissions, and working outputs.
- Keep canonical synchronization overlay-only.
- Separate documentation changes from automation changes when practical.

## Validation

Before merging a change:

1. Confirm referenced paths exist.
2. Confirm no private information was introduced unintentionally.
3. Confirm facts and analysis remain separated.
4. Confirm canonical rules are referenced rather than duplicated.
5. Validate YAML, JSON, and Python where applicable.
6. Use synthetic fixtures for automation tests.
7. Record limitations and unresolved validation explicitly.

## Continuation

Repository continuation state is preserved in `HOUSEHOLD_MIRROR_HANDOFF.md`.
