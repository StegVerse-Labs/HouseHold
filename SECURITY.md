# Security and Privacy Policy

HouseHold may contain real-world incident records, communications, contracts, receipts, photos, vehicle information, addresses, and other sensitive material.

## Reporting a Security or Privacy Problem

Do not open a public issue containing sensitive content.

Report the minimum information needed to identify the affected path and risk. Do not repeat exposed credentials, account numbers, addresses, signatures, or private communications in the report.

Examples include:

- accidentally committed credentials or tokens;
- unredacted personal or financial information;
- evidence files exposed beyond their intended audience;
- workflows that can overwrite, relocate, or publish incident material unexpectedly;
- custody or confidence records that can be silently altered;
- generated packets that can be sent without explicit review.

## Immediate Response

When sensitive material is discovered:

1. Stop further publication or automation involving the affected path.
2. Preserve the original record privately when it is needed for the incident.
3. Remove or replace the public copy with a redacted version or safe reference.
4. Rotate any exposed credential or secret.
5. Record the remediation without reproducing the sensitive content.
6. Review repository history and cached artifacts when removal from the current tree is insufficient.

Deleting a file from the latest commit does not necessarily remove it from Git history.

## Evidence Integrity

Security controls must not silently destroy evidence.

- Preserve originals where authorized.
- Record transformations and redactions.
- Use hashes and manifests to identify versions.
- Keep custody events append-only.
- Do not treat a hash, timestamp, metadata field, or confidence score as proof of authenticity by itself.

## Automation Safety

Automation must:

- default to dry-run or validation-only behavior during development;
- avoid moving or overwriting original evidence by default;
- use synthetic fixtures in CI;
- require explicit review before external delivery;
- fail clearly when canonical rules, required inputs, or review state are missing;
- never publish private evidence to StegDB.

## Public Repository Guidance

Prefer:

- redacted documents;
- synthetic examples;
- stable evidence references;
- hashes and manifests without embedded private content;
- private companion storage where public publication is unnecessary.

## Scope Boundary

StegDB contains canonical protocols and schemas. HouseHold contains implementation and incident state. Security fixes must preserve this boundary and must use additive or exact-file updates rather than full-folder replacement.

Current continuation and unresolved validation requirements are recorded in `HOUSEHOLD_MIRROR_HANDOFF.md`.
