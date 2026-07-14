# HouseHold Mirror Handoff

## Status

HouseHold is the active real-world proving ground for the Household Escalation Engine (HEE). This handoff preserves repository state, architectural decisions, unresolved implementation work, and permitted continuation scope.

Current continuation state:

```text
incident documentation
→ timeline and findings separation
→ evidence organization
→ custody/provenance separation
→ escalation packet structure
→ guidance layer committed
→ safe fixture and dry-run validator
→ StegDB protocol registration
→ deterministic evidence ingest
→ confidence-aware packet generation
→ CI execution and validation
```

## Decisions Preserved

1. StegDB is the canonical protocol and schema authority.
2. HouseHold is a consumer/proving-ground repository containing real incident state and implementation evidence.
3. HEE bridges StegDB protocols to HouseHold incident workflows; HEE does not replace legal, regulatory, or professional judgment.
4. Protocols live once in StegDB. HouseHold incidents reference them rather than redefining them.
5. HEE templates live once under `HEE/`; incident folders contain incident state, evidence references, findings, and reviewed escalation packets.
6. Timeline files contain dated observations and events. Interpretation, constraints, impacts, risks, and remedy analysis belong in `findings/`.
7. Custody, provenance, and optional financial context are separate layers.
8. Evidence confidence is decision-support metadata, not proof, authentication, or a legal conclusion.
9. Custody transitions are append-only and notification-capable; notification does not establish authority or truth.
10. Evidence originals must not be silently overwritten. Hashes, transformations, index records, and custody events must remain traceable.
11. Automation must remain deterministic, fail clearly, and preserve human review before external delivery.
12. HouseHold may contain sensitive real-world material; public examples and CI fixtures must be redacted or synthetic.
13. Canonical synchronization must be overlay-only and must not replace incident data or unrelated working outputs.

## Durable Records

### HouseHold

- This handoff: `HOUSEHOLD_MIRROR_HANDOFF.md`
- Root repository guidance: `README.md`
- Contribution boundary and validation rules: `CONTRIBUTING.md`
- Privacy and security handling: `SECURITY.md`
- Incident template guidance: `_new-incident-template/README.md`
- HEE authority, packet, and automation constraints: `HEE/README.md`
- Foundational HEE principles: `HEE/household-escalation-engine.md`
- Packet specification: `HEE/engine/packet-spec.md`
- Intake guidance: `HEE/intake/intake_questionnaire.md`

### StegDB

- Linked protocol task: `StegVerse-Labs/StegDB#9`
- Scope: HEE artifacts, confidence factors and limitations, custody transitions, notifications, packet review state, and overlay-only canonical consumption.

## Completed Work

- Established the StegDB/HEE/HouseHold authority boundary.
- Established facts-versus-analysis separation.
- Established evidence, provenance, custody, confidence, and review-state distinctions.
- Established escalation packet expectations around `letter.md`, `attachments.md`, a packet index, and human review.
- Committed the durable repository guidance layer without adding automation.
- Created the linked StegDB protocol-registration task.

### Guidance Commits

- Initial handoff: `66deb63631ed1d1213c82504e3cc13810baae1ad`
- `CONTRIBUTING.md`: `cc31bbb944df872c5192aa566017712d5fdd0cc3`
- `SECURITY.md`: `505f55ea7f968940b1e856c841aaad417c9b3976`
- `_new-incident-template/README.md`: `2cbc7387e589609be968fb0dc402d75581a2d4c5`
- `HEE/README.md`: `f25e2225e262746023069974c88c3c113a305341`

## Commit-State Distinction

The following items were discussed or drafted previously but are not authoritative unless present and validated on the default branch:

- `docs/STRUCTURE.md`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/*`
- `HEE/escalation-level-spec.md`
- `HEE/letter-template.md`
- `HEE/attachments-template.md`
- `HEE/tools/hee.py`
- `HEE/engine/hee_engine.py`
- `HEE/engine/__init__.py`
- `.github/workflows/hee-generate.yml`

Do not copy old drafts blindly. Inspect current files and implement the smallest verified next slice.

## Known Blockers and Risks

- No complete repository-side HEE automation bundle has been validated through GitHub Actions.
- Confidence scoring semantics require canonical StegDB review before ecosystem-wide use.
- Filesystem modification time and EXIF presence are not reliable truth indicators; they may only be disclosed factors.
- Generated letters and packets require human review before delivery.
- Existing incidents may not share one identical folder contract; migration must remain additive and non-destructive.
- Privacy review is required before using real incident evidence in examples, tests, artifacts, or workflow logs.

## Remaining Work

### Phase 2 — Minimal HEE implementation

1. Add a synthetic fixture incident under a clearly non-production path.
2. Implement a standard-library-first, read-only validator and dry-run packet planner.
3. Validate required packet fields, stable evidence references, review state, and unresolved uncertainty.
4. Emit a machine-readable plan and human-readable report without moving, renaming, or rewriting evidence.
5. Add tests that use only the synthetic fixture.
6. Update this handoff with commands, outputs, and commit SHAs.

### Phase 3 — StegDB protocol integration

Continue through `StegVerse-Labs/StegDB#9`:

- version canonical artifact, confidence, custody, notification, packet-review, and source-lock requirements;
- use synthetic examples;
- preserve implementation independence;
- keep HouseHold synchronization overlay-only.

### Phase 4 — CI validation

1. Add a manually dispatched validation workflow only after local fixture validation exists.
2. Capture reports and receipts as workflow artifacts.
3. Observe a real workflow run.
4. Do not auto-send letters, notifications, or evidence.
5. Add mutation behavior only after dry-run validation is deterministic and reviewed.

## Exact Next Authorized Task

```text
Create one synthetic HEE fixture and one read-only validator/dry-run packet planner.
Do not add evidence ingestion, confidence scoring, file movement, letter generation, or external delivery yet.
```

Expected files:

```text
HEE/fixtures/minimal-incident/
HEE/tools/validate_incident.py
HEE/tests/test_validate_incident.py
```

Expected outputs when run:

```text
out/hee/minimal-incident/validation.json
out/hee/minimal-incident/validation.md
out/hee/minimal-incident/packet-plan.json
```

Done when:

- the fixture contains no real personal or incident data;
- the validator is read-only with respect to fixture and incident inputs;
- outputs distinguish errors, warnings, unresolved uncertainty, and review state;
- tests pass locally or in an existing safe execution path;
- no external-facing letter is generated;
- this handoff records the implementation commit and validation evidence.

## Ownership and Permitted Continuation Scope

- Active HouseHold owner: next authorized HouseHold/HEE build session or StegVerse entity assigned to `StegVerse-Labs/HouseHold`.
- Active StegDB owner: next authorized session or entity assigned to `StegVerse-Labs/StegDB#9`.
- No authority is granted to publish private evidence, send escalation letters, notify counterparties, claim legal validity, or perform full-folder replacement.
- Permitted scope is synthetic fixtures, read-only validation, dry-run planning, protocol registration, additive exact-file changes, and later CI evidence.

## Pending Validation and Observation Requirements

- Verify every path against the default branch before mutation.
- Validate Python and structured outputs against synthetic fixtures.
- Verify canonical references resolve before claiming integration.
- Observe at least one GitHub Actions run before claiming workflow completion.
- Record hashes, manifests, exclusions, uncertainty, and review state in durable receipts as implementation matures.

## Archive Readiness

All session-specific decisions, completed work, discovered blockers, remaining tasks, active ownership, validation requirements, and continuation boundaries are preserved in this handoff and `StegVerse-Labs/StegDB#9`.
