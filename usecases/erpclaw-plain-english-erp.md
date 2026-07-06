# ERPClaw: Plain-English ERP and Accounting

**Class:** Ecosystem integration
**Confidence:** Medium
**Demo status:** Runnable

## Pain Point

Small businesses run their books across invoicing apps, spreadsheets, and hosted accounting SaaS. The data lives on someone else's servers, the subscription bills stack up, and classic self-hosted ERPs trade that for forms, menus, and a steep setup curve.

## What It Does

Turns a Hermes agent into a working back office. You type plain English ("invoice Globex for the March order", "record their payment"), and the skill routes each request to deterministic Python actions that write real double-entry records to a local database. Chat is the ingress; the ledger is the system of record. Money is stored as exact decimals, submitted ledger entries are immutable (corrections post reversing entries), and every posting passes validation before it commits. SQLite by default, PostgreSQL supported. Covers invoicing, inventory, payroll, purchasing, and multi-company books.

## Setup

```bash
# add the ERPClaw skill from the GitHub tap
hermes skills tap add avansaber/erpclaw

# keep the Curator from rewriting the skill's action catalog
hermes curator pin erpclaw

# optional: choose an install root (unset defaults to ~/.openclaw/erpclaw)
export ERPCLAW_HOME="$HOME/.erpclaw"
```

Requires `python3` and `git` on PATH. On first run, ask the agent to set up your company; the skill initializes its database and walks through onboarding conversationally.

## Prompts

The two flows used to accept the Hermes port (each graded by a deterministic oracle against the resulting database rows, not by the model):

- "Set up my company. We're Acme Consulting, a US company. Use USD."
- "Add a customer named Globex, invoice them 1,200 dollars for March consulting, then record their payment against that invoice."

Everyday usage is the same register: "what's my accounts receivable?", "run payroll for June", "how much of item X do we have in stock?"

## Skills Needed

- `erpclaw` (GitHub tap: `avansaber/erpclaw`)
- `python3` and `git` on PATH
- SQLite (bundled default) or PostgreSQL (optional backend)

## Notes

- OpenClaw is the primary, fully supported runtime; Hermes support is newer and best-effort (the project tags it beta). No encrypted-credential actions on Hermes in v1.
- The curator pin matters: the SKILL.md is the skill's authoritative action catalog, and the port assumes it stays unrewritten.
- Everything runs on your own machine. $0, open source (GPL v3), built by AvanSaber.

## Sources

- Repo and SKILL.md showing the Hermes runtime config (`metadata.hermes`, `ERPCLAW_HOME`): https://github.com/avansaber/erpclaw
- CHANGELOG v4.10.0 "Hermes runtime port v1" entry, including the acceptance scenarios: https://github.com/avansaber/erpclaw/blob/main/CHANGELOG.md
- Merged listing on awesome-hermes-agent (Domain Applications): https://github.com/SamurAIGPT/awesome-hermes-agent/pull/65
