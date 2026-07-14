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
→ synthetic fixture committed
→ read-only validator and dry-run planner committed
→ manual CI validation
→ StegDB protocol registration
→ deterministic evidence ingest
→ confidence-aware packet generation
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
- Root guidance: `README.md`
- Contribution rules: `CONTRIBUTING.md`
- Security/privacy policy: `SECURITY.md`
- Incident template guidance: `_new-incident-template/README.md`
- HEE authority and automation constraints: `HEE/README.md`
- Foundational principles: `HEE/household-escalation-engine.md`
- Packet specification: `HEE/engine/packet-spec.md`
- Synthetic fixture: `HEE/fixtures/minimal-incident/`
- Read-only validator and planner: `HEE/tools/validate_incident.py`
- Tests: `HEE/tests/test_validate_incident.py`

### StegDB

- Linked protocol task: `StegVerse-Labs/StegDB#9`
- Scope: HEE artifacts, confidence factors and limitations, custody transitions, notifications, packet review state, and overlay-only canonical consumption.

## Completed Work

- Established the StegDB/HEE/HouseHold authority boundary.
- Established facts-versus-analysis separation.
- Established evidence, provenance, custody, confidence, and review-state distinctions.
- Established escalation packet expectations and mandatory human review.
- Committed the durable repository guidance layer.
- Created the linked StegDB protocol-registration task.
- Added a fully synthetic incident fixture.
- Added a standard-library-only validator that checks required fields, safe relative paths, referenced files, review state, and unresolved uncertainty.
- Added a dry-run packet planner that always sets `send_authorized` to `false`.
- Added four unit tests covering successful validation, missing evidence, non-authorized sending, and output isolation.

## Commit Record

- Initial handoff: `66deb63631ed1d1213c82504e3cc13810baae1ad`
- Guidance layer:
  - `CONTRIBUTING.md`: `cc31bbb944df872c5192aa566017712d5fdd0cc3`
  - `SECURITY.md`: `505f55ea7f968940b1e856c841aaad417c9b3976`
  - `_new-incident-template/README.md`: `2cbc7387e589609be968fb0dc402d75581a2d4c5`
  - `HEE/README.md`: `f25e2225e262746023069974c88c3c113a305341`
- Validator: `3eea79ece5887d8ca6dd64bdbfac05e27fbbc0b0`
- Synthetic fixture:
  - manifest: `bdffcfdef566d4bb7a853aa2a43e3ab9da84d477`
  - evidence: `94c9b7fd51cd66b5dfb789d0b12b4fc47d3abd2a`
  - timeline: `6c6b615011477860dc610319340a116c665b0b12`
  - findings: `6002bef02e8e37ef4c17e74c7a42be9fdcee974a`
- Tests: `59ad28f083a1e364a95cea9eaded3617b6acc16a`

## Validation Evidence

Local safe-fixture validation completed successfully before commit:

```text
python -m unittest discover -s HEE/tests -p 'test_*.py'
Ran 4 tests
OK

python HEE/tools/validate_incident.py HEE/fixtures/minimal-incident --output-root out/hee
status: PASS
errors: 0
warnings: 1 (unresolved uncertainty present)
evidence files validated: 1
supporting files validated: 2
send_authorized: false
```

Deterministic fixture hashes observed:

- manifest SHA-256: `f16410ece35f6a0bc625d38d6f7e129c1281d1f850dd416cb412c0f44f20b292`
- synthetic evidence SHA-256: `c842bbcbdf35a8429e2dfb500c5dcf6a4a8b304ba6ddea2199ceab18ff71395e`
- timeline SHA-256: `2517e22897b792d8d3a39d57c454171a33c87d227a9b720935fd9bfefb3fa053`
- findings SHA-256: `bb092a49c29bcbdb04b9e4ead21dab00dc9553982f16871074235e13ca347aea`

Expected generated outputs:

```text
out/hee/minimal-incident/validation.json
out/hee/minimal-incident/validation.md
out/hee/minimal-incident/packet-plan.json
```

These outputs are generated outside the fixture and do not modify source evidence.

## Commit-State Distinction

The following items are not authoritative unless present and validated on the default branch:

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

- The validator has not yet been observed in GitHub Actions.
- Confidence scoring semantics require canonical StegDB review before ecosystem-wide use.
- Filesystem modification time and EXIF presence are not reliable truth indicators.
- Generated letters and packets require human review before delivery.
- Existing incidents may not share one identical folder contract; migration must remain additive and non-destructive.
- Privacy review is required before using real incident evidence in examples, tests, artifacts, or workflow logs.

## Exact Next Authorized Task

```text
Add one manually dispatched GitHub Actions workflow that runs only the synthetic fixture validator and unit tests, uploads the generated validation outputs as artifacts, and performs no repository mutation or external delivery.
```

Expected path:

```text
.github/workflows/hee-validate.yml
```

Required behavior:

- `workflow_dispatch` only.
- Python standard library only.
- Run the four unit tests.
- Run the validator against `HEE/fixtures/minimal-incident`.
- Upload `out/hee/minimal-incident/` as a workflow artifact.
- Use read-only repository permissions.
- Do not commit generated files.
- Do not send letters, notifications, or evidence.

Done when:

- the workflow file is committed;
- one real GitHub Actions run is observed;
- tests and validation pass;
- the artifact contains `validation.json`, `validation.md`, and `packet-plan.json`;
- the run ID, commit SHA, artifact identity, and result are recorded here.

## Ownership and Permitted Continuation Scope

- Active HouseHold owner: next authorized HouseHold/HEE build session or StegVerse entity assigned to `StegVerse-Labs/HouseHold`.
- Active StegDB owner: next authorized session or entity assigned to `StegVerse-Labs/StegDB#9`.
- No authority is granted to publish private evidence, send escalation letters, notify counterparties, claim legal validity, or perform full-folder replacement.
- Permitted scope is the read-only synthetic-fixture workflow, CI evidence capture, protocol registration, and additive exact-file changes.

## Pending Validation and Observation Requirements

- Observe at least one GitHub Actions run before claiming workflow completion.
- Verify the uploaded artifact contents and hashes.
- Verify canonical references resolve before claiming StegDB integration.
- Preserve the distinction between structure validation and truth/authenticity claims.

## Archive Readiness

All session-specific decisions, completed work, discovered blockers, remaining tasks, active ownership, validation requirements, and continuation boundaries are preserved in this handoff and `StegVerse-Labs/StegDB#9`.
