# Escalation Packet Specification

An escalation packet consists of:

- letter.md
- README.md (context + evidence links)
- attachments.md (manifest)

## Required Inputs

- incident_id
- escalation_level
- counterparty
- objectives
- evidence_paths

## Output Structure

escalation/<level>/
├── letter.md
├── README.md
└── attachments.md

Generation must never alter source evidence.
