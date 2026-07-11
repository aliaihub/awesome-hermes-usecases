# Deterministic Delegation: Repeatable Jobs as Checked Workflow Files

**Class:** First-party integration · **Confidence:** High · **Demo status:** Runnable (offline, no keys)

## Pain Point

You ask Hermes for the same morning brief, triage pass, or report pipeline and get a slightly different improvisation every time. When a repeated job spends money, there's no receipt; when a small model claims it "verified" something, you can't tell narration from execution (we've watched a local 9B answer "VERIFIED ✓" with zero tool calls in the log).

## What It Does

![A repeated chat prompt becomes meeting-actions.nika.yaml; nika check audits it, then a real local run (ollama/llama3.2:3b) writes typed action items](https://raw.githubusercontent.com/supernovae-st/nika/main/media/gifs/chat-to-workflow.optimized.gif)

Hermes keeps the judgment; a deterministic runner keeps the receipts. The repeatable slice of the work graduates from chat into one plain-text `.nika.yaml` file (a small DAG: fetch → summarize → save) that Hermes delegates to via the `nika` skill:

- `nika check` audits the file **before any token is spent**: the plan, an honest cost floor (unpriced work is flagged, never shown as $0), which secrets flow into which task.
- Paid runs are budget-capped (`--max-cost-usd`); the offline mock and Ollama paths need zero keys.
- Every run writes a hash-chained trace: `nika trace verify` exits 0 or names the first broken link. The receipt comes from the runner, not from the model's prose.

Honest tradeoff: workflows are non-interactive by design. For autonomous coding, the OpenCode skill stays the right seat: this is for the boring-on-purpose slice (daily digests, triage, ETL, report pipelines).

## Setup

1. Install the runner (single Rust binary) and the skill:
   ```bash
   brew install supernovae-st/tap/nika
   hermes skills tap add supernovae-st/nika-agents
   ```
2. Nothing else. The offline demo below needs no API key, no model server.

## Prompts

Ask Hermes to capture a repeated job as a workflow, then run it with receipts:

```
Use the nika skill. Create a workflow file daily-brief.nika.yaml that
fetches https://news.ycombinator.com/rss (feed mode), keeps the top 5
titles, and writes them to brief.md. Check it with nika check first,
run it on the mock model, then verify the trace and tell me the chain
head from the terminal output, not from memory.
```

Or hand it an existing file:

```
Run nika check on report.nika.yaml, explain any findings with
nika explain, fix the file, and only run it once check passes.
Cap the run at $0.10 with --max-cost-usd.
```

## Runnable Demo (offline · zero keys)

![nika run executes the DAG in parallel waves in the terminal, live lanes, per-task timings, then the verdict card](https://raw.githubusercontent.com/supernovae-st/nika/main/media/gifs/dag-execution.optimized.gif)

```bash
nika examples run 01-hello --model mock/echo   # deterministic offline run
nika examples run 01-hello --model ollama/qwen3.5:4b   # same run, real local model
nika trace verify .nika/traces/*.ndjson        # exit 0 = chain intact
```

## Skills Needed

- The `nika` skill (taught commands are CI-tested against each released binary before the skill can merge)
- Optional: Ollama for a real local model (the mock path works with nothing installed)

## Notes

- The skill passed the hermes-agent skill-guard security scan (it never edits host config and never pipes curl|sh, installs are a human step, by design).
- Engine AGPL-3.0, spec + TS SDK Apache-2.0. Disclosure: contributed by the nika author.
