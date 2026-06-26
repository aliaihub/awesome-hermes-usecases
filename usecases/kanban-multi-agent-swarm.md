# Hermes Kanban: Multi-Agent Swarm from Slack

**Class:** First-party feature · **Confidence:** High · **Demo status:** First-party docs + tutorial

## Pain Point

You want to throw a complex multi-step task at an AI — "design a multi-region failover plan" or "audit this codebase for security issues across auth, data, and infra" — and have it handled by *specialist* sub-agents that work in parallel, with a verifier checking their output, and a synthesizer combining the results. Hermes has `delegate_task`, but that's a function call inside the running agent's session — it doesn't persist, doesn't checkpoint, and doesn't survive a restart.

## What It Does

The Hermes Kanban feature (introduced in v0.15, the "Velocity Release") turns a chat message into a *durable* multi-agent swarm. A SQLite board at `~/.hermes/kanban.db` holds every handoff as a row. Workers run as full OS processes with their own identity; results are written back to the board, not to a chat session.

The pattern from the official docs:

```bash
hermes kanban swarm "Design a multi-region failover plan" \
  --workers researcher,architect,sre \
  --verifier reviewer \
  --synthesizer writer
```

The first worker becomes the lead; the others are specialists. The verifier checks the specialists' output; the synthesizer combines verified work into a final deliverable. The whole thing is observable in the Hermes dashboard and checkable mid-flight.

Critically, **`/kanban` is a slash command** that works from any messaging gateway — Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, email, and SMS. So a Slack message in your team's `#agent-tasks` channel can spin up a swarm without you touching the CLI.

**Use case:** a team that wants to dispatch complex tasks to a multi-agent system from a chat surface they already use, with audit-trail persistence.

## Setup

1. Install Hermes v0.15 or later:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   ```
2. Configure Slack (or any other gateway) and pair the bot to your `#agent-tasks` channel:
   ```bash
   hermes gateway setup
   hermes gateway install
   ```
3. Enable Kanban in your Hermes config. It's part of the v0.15 release; check the docs for the current default.
4. From Slack, send the first swarm:
   ```
   /kanban swarm "Audit this repo for hardcoded credentials, exposed
   secrets, and unsafe shell expansions. Workers: scanner, historian,
   reporter. Verifier: senior-reviewer. Synthesizer: writer."
   ```

The command bypasses the running-agent guard — meaning you can drive the board from Slack mid-conversation without interrupting the active agent.

## Prompts

The Anthony Maio Substack piece ("Hermes Agent Got Serious", Jun 5 2026) demonstrates the swarm pattern with a concrete example:

```
/kanban swarm "Design a multi-region failover plan" \
  --workers researcher,architect,sre \
  --verifier reviewer \
  --synthesizer writer
```

Variations the docs and community examples use:

```
# Security audit
/kanban swarm "Audit this repo for OWASP top 10 issues. Workers:
scanner, historian, reporter. Verifier: senior-reviewer.
Synthesizer: writer."

# Codebase documentation
/kanban swarm "Document the auth module end-to-end. Workers: reader,
tester, screenshotter. Verifier: tech-writer. Synthesizer: editor."

# Research synthesis
/kanban swarm "Compare the three main Postgres ORMs on performance,
DX, and ecosystem. Workers: benchmarker, documenter, interviewer.
Verifier: critic. Synthesizer: writer."
```

The pattern scales: more workers = more parallelism, but verify on the synthesizer's output gets noisier. Three to four workers is the sweet spot in the community examples.

## Skills Needed

- Hermes Agent v0.15+
- A messaging gateway (Slack is the focus here; Telegram, Discord, etc. work the same)
- A model provider that can run multiple agents in parallel (OpenRouter, OpenAI, Anthropic direct, or a mix)
- Optional: a Hermes dashboard for mid-flight inspection

## Notes

- **Kanban is durable, `delegate_task` is not.** Use Kanban for jobs that take longer than a chat session; use `delegate_task` for quick parallel calls inside a single conversation.
- **The board is `~/.hermes/kanban.db` — back it up.** Daily cron to copy it to your backup volume is the same pattern as `hermes-on-flyio.md`'s volume snapshot.
- **Verifier pattern is the moat.** A swarm without a verifier is just `delegate_task` with extra steps. The verifier checks the specialists' output before the synthesizer sees it — that's what makes the result trustworthy.
- **Slack as the swarm trigger** is the pattern that makes this useful for a team. A PM can drop a task in `#agent-tasks`, watch the board fill in, and pull the deliverable out — no CLI access needed.
- **Distinct from `paperclip-managed-employee.md`** (Hermes-as-worker inside Nous's Paperclip orchestrator — Hermes is *one* worker there, not a swarm leader). **Distinct from `zouroboros-swarm-bridge.md`** (Hermes as one of four interchangeable executors in an external orchestrator — that one routes *between* frameworks; this one routes *between sub-agents inside* Hermes).
- **First-party feature.** This is Hermes's own primitive, not a third-party integration. If it ships in a Hermes release, the docs are authoritative.

## Sources

- **Primary (first-party docs):** Hermes Agent — Kanban feature reference.
  <https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban>
- **Primary (first-party tutorial):** Hermes Agent — Kanban tutorial with four user stories and dashboard screenshots.
  <https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban-tutorial>
- **Independent first-person coverage:** Anthony Maio, "Hermes Agent Got Serious" — Substack, Jun 5 2026. Documents the swarm pattern in production use over two weeks.
  <https://anthonymaio.substack.com/p/hermes-agent-got-serious>

## Related Use Cases

- [Paperclip Managed Employee](paperclip-managed-employee.md) — Hermes as a single worker in Nous's external orchestrator (complementary, not duplicative)
- [Zouroboros Swarm Bridge](zouroboros-swarm-bridge.md) — Hermes as one of four executors in an external multi-agent orchestrator
- [Matt Pocock Skills + Sub-Agents](matt-pocock-skills-subagents.md) — plan-then-delegate pattern using sub-agents for execution
