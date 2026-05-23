# Hermes Labyrinth Observability

**Class:** Observability plugin · **Confidence:** High · **Demo status:** Public dashboard plugin and live demo

## Pain Point

Autonomous agent work can become hard to audit. Prompts, tool calls, failures,
approvals, model switches, cron runs, memory hits, redactions, and sub-agent
delegations are scattered across local state and logs. Teams need a read-only
black-box recorder for what the agent actually did.

## What It Does

Hermes Labyrinth is a dashboard plugin that maps local Hermes work into
journeys and crossings. It is not a chat UI. It is an observability layer for
agent execution.

The plugin provides:

- Journey index for CLI, dashboard, gateway, cron, and delegated work.
- Ordered map of prompts, tool calls, tool results, failures, approvals, memory
  hits, context compression, and model switches.
- Inspector view with input, output, duration, status, evidence, and guideposts.
- Skill atlas for active, shadowed, and duplicate skills.
- Cron gate view for scheduled autonomy.
- Redacted Markdown and JSON reports for a selected journey.

## Setup

Install into the Hermes user plugin directory:

```bash
mkdir -p ~/.hermes/plugins
git clone https://github.com/stainlu/hermes-labyrinth.git ~/.hermes/plugins/hermes-labyrinth
hermes dashboard
```

Open the dashboard and select the Labyrinth tab. If the dashboard was already
running, restart it so the plugin API routes mount cleanly.

## Prompts

Audit a long-running job:

```text
Open the Labyrinth report for the latest cron journey and summarize tool
failures, retries, approvals, and exported evidence.
```

Skill hygiene:

```text
Use the Labyrinth skill atlas to identify duplicate or shadowed skills and
draft a cleanup plan. Do not delete anything.
```

Incident review:

```text
Export the journey that touched production files today as redacted Markdown and
JSON for review.
```

## Skills Needed

- Hermes dashboard
- Hermes plugin directory access
- Local Hermes state with sessions, tools, cron, or gateway activity

## Notes

- Labyrinth is read-only by design, which makes it safer to add to production
  Hermes installations than a new control interface.
- Treat exported traces as sensitive. Even redacted logs may reveal project
  paths, operational habits, or partial secrets.
- The live demo uses mocked state; real value comes from installing it against a
  local Hermes profile.

## Sources

- Hermes Labyrinth repository: <https://github.com/stainlu/hermes-labyrinth>
- Live demo: <https://stainlu.github.io/hermes-labyrinth/>
