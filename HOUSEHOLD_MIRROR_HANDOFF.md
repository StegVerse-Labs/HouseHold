# HouseHold Mirror Handoff

## Status

HouseHold is the active real-world proving ground for the Household Escalation Engine (HEE). This handoff preserves the repository state, architectural decisions, unresolved implementation work, and the permitted continuation scope so future work does not depend on this conversation.

Current continuation state:

```text
incident documentation
→ timeline and findings separation
→ evidence organization
→ custody/provenance separation
→ escalation packet structure
→ HEE template consolidation
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
5. HEE templates live once under `HEE/`; incident folders contain incident state, evidence references, findings, and generated escalation packets.
6. Timeline files contain dated observations and events. Interpretation, constraints, impacts, risks, and remedy analysis belong in `findings/`.
7. Custody, provenance, and optional financial context are separate layers. Escalation packets consume these layers without rewriting them.
8. Evidence confidence is decision-support metadata, not proof, authentication, or a legal conclusion.
9. Custody transitions are append-only events and should be notification-capable; notification does not itself establish authority or truth.
10. Evidence originals must not be silently overwritten. Index records, hashes, transformations, and custody events must remain traceable.
11. Automation must remain deterministic, fail clearly, and preserve manual review before external delivery.
12. HouseHold contains sensitive real-world material; public artifacts must be redacted or represented by safe references/hashes.
13. Canonical synchronization must be overlay-only. It must not replace incident data, `entities/`, existing templates, papers, references, submissions, or other working outputs.

## Current Repository Evidence

The repository currently contains:

- Root `README.md` describing HouseHold, HEE, current incidents, evidence organization, escalation packet folders, and privacy cautions.
- `HEE/household-escalation-engine.md` defining HEE as a documentation-first, evidence-backed, domain-agnostic escalation system.
- `HEE/engine/packet-spec.md`.
- `HEE/intake/intake_questionnaire.md`.
- Automotive templates under `HEE/templates/automotive/`.
- `_new-incident-template/timeline/initial-observations.md`.
- `water-heater-replacement/` as a home-warranty incident exemplar.
- `corvette-c8-transmission/` as an automotive custody, provenance, findings, and escalation exemplar.

## Completed Work

- Established the protocol/implementation boundary between StegDB, HEE, and HouseHold.
- Established the facts-versus-analysis split between `timeline/` and `findings/`.
- Established escalation packet expectations around `letter.md`, `README.md`, and `attachments.md`.
- Established custody and provenance as distinct from incident conclusions.
- Established the need for evidence confidence metadata and append-only custody events.
- Drafted contributor guidance, structure documentation, security guidance, issue/PR templates, HEE README material, escalation-level guidance, letter and attachment templates, a Python CLI/engine concept, and a dispatchable packet-generation workflow.

## Important Commit-State Distinction

The following items were designed in session but must not be treated as committed or validated unless they are found in the repository at continuation time:

- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/STRUCTURE.md`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/*`
- `_new-incident-template/README.md`
- `HEE/README.md`
- `HEE/escalation-level-spec.md`
- `HEE/letter-template.md`
- `HEE/attachments-template.md`
- `HEE/tools/hee.py`
- `HEE/engine/hee_engine.py`
- `HEE/engine/__init__.py`
- `.github/workflows/hee-generate.yml`

A continuation session must inspect the default branch before creating any of these files, preserve existing content, and avoid duplicate or conflicting paths.

## Known Blockers and Risks

- No complete repository-side HEE automation bundle has yet been verified through an actual GitHub Actions run.
- Confidence scoring semantics require canonical StegDB review before they can be treated as ecosystem protocol.
- Filesystem modification time and EXIF presence alone are not reliable truth indicators; they may be used only as transparent factors, never as authentication.
- Generated letters and packets require human review before external delivery.
- Existing incident folders may not yet conform to one identical folder contract; migration must be additive and non-destructive.
- The repository may expose personal data, vehicle identifiers, addresses, communications, contracts, or receipts. Privacy review is required before expanding public automation or examples.

## Remaining Work

### Phase 1 — Durable repository guidance

1. Inspect existing repository files and commit non-conflicting versions of:
   - `CONTRIBUTING.md`
   - `SECURITY.md`
   - `_new-incident-template/README.md`
   - `HEE/README.md`
2. Add a concise `docs/STRUCTURE.md` only if it reduces duplication rather than creating another authority source.
3. Add PR/issue templates only after confirming they match actual repository workflows and labels.

### Phase 2 — Minimal HEE implementation

1. Implement a minimal, standard-library-first CLI under `HEE/tools/`.
2. Begin with read-only validation and dry-run packet planning before allowing repository mutation.
3. Add artifact hashing and index generation without moving or rewriting originals by default.
4. Add append-only custody events.
5. Generate packet manifests before generating external-facing letters.
6. Require explicit review state before a packet is marked send-ready.

### Phase 3 — StegDB protocol integration

1. Register or refine canonical HEE artifact, evidence-confidence, custody-transition, and notification specifications in StegDB.
2. Define version identifiers and migration rules.
3. Keep HouseHold implementation-specific paths outside canonical protocol requirements.
4. Add overlay-only canonical consumption with a lock/receipt recording the StegDB source version.

### Phase 4 — CI validation

1. Add a manually dispatched validation workflow first.
2. Run against a safe fixture incident, not private evidence.
3. Capture generated manifests, validation results, and receipts as artifacts.
4. Do not auto-send letters or notifications from CI.
5. Promote mutation or packet-generation behavior only after deterministic fixture validation passes.

## Exact Next Authorized Task

```text
Inspect the current default branch, then commit the smallest non-conflicting guidance layer:
CONTRIBUTING.md, SECURITY.md, _new-incident-template/README.md, and HEE/README.md.
Do not add automation in the same change.
```

Done when:

- Each file exists on the default branch.
- Each file reflects the StegDB/HouseHold/HEE authority boundary.
- The files distinguish evidence, claims, confidence, custody, and external delivery.
- No incident evidence or existing template is overwritten.
- This handoff is updated with the resulting commit SHA and the next implementation task.

## Ownership and Permitted Continuation Scope

- Active owner: next authorized HouseHold/HEE build session or StegVerse entity assigned to `StegVerse-Labs/HouseHold`.
- StegDB protocol work is owned by the next authorized session assigned to `StegVerse-Labs/StegDB`.
- This handoff grants no authority to publish private evidence, send escalation letters, notify counterparties, or claim legal validity.
- Permitted next scope is repository guidance, safe fixture design, protocol registration, deterministic local tooling, and CI validation.
- Do not perform full-folder replacement. Use additive or exact-file updates only.

## Pending Validation and Observation Requirements

- Verify every drafted path against the default branch before mutation.
- Verify that canonical protocol references resolve to committed StegDB files.
- Validate all YAML and Python against safe fixtures.
- Observe at least one GitHub Actions run before claiming workflow completion.
- Record generated hashes, manifests, exclusions, and review state in durable receipts.

## Archive Readiness

This file preserves the session-specific decisions, discovered tasks and blockers, completed design work, remaining work, ownership state, validation requirements, and permitted continuation scope. Future work can continue from this handoff and linked StegDB task records without access to the originating conversation.
