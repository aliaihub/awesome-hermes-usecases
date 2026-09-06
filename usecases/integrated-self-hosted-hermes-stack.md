# Integrated Self-Hosted Hermes Stack

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Runnable installer + verification script

## Pain Point

A serious self-hosted agent often needs much more than the agent binary: model routing, local inference, search, vector storage, automation, notifications, observability, monitoring, secrets, and backups. Wiring those services individually creates a large configuration and maintenance burden.

## What It Does

Evey Setup bootstraps an integrated Hermes stack in four phases. Depending on the selected tier, it connects Hermes with LiteLLM, Ollama, MQTT, SearXNG, Qdrant, ntfy, n8n, Langfuse, Uptime Kuma, and categorized community plugins.

The scripts check prerequisites, generate internal secrets, create Docker Compose configuration, select models and fallbacks, configure cron and gateways, and run a final PASS/FAIL verification. Service ports bind to loopback by default.

## Setup

Run the supported interactive flow:

```bash
git clone https://github.com/42-evey/evey-setup.git
cd evey-setup
bash setup.sh
```

Or install all phases non-interactively:

```bash
OPENROUTER_API_KEY=sk-or-... bash install.sh --yes --tier full --plugins all
bash verify.sh
```

The repository requires Docker 24+, Docker Compose v2, Git, at least 5 GB of free disk, and a model-provider key. NVIDIA GPU acceleration is optional.

## Prompts

Evey configures infrastructure rather than adding a single task prompt. After `verify.sh` passes, use Hermes normally through the CLI, Telegram, or Discord and verify only the services required by the chosen workflow are enabled.

## Skills Needed

- Docker and Docker Compose
- Hermes Agent
- LiteLLM and at least one model backend
- Optional Ollama, SearXNG, Qdrant, n8n, Langfuse, Uptime Kuma, MQTT, and ntfy
- Selected community plugins rather than an unrestricted default set

## Notes

- The repository calls its default models zero-cost, but the computer, VPS, electricity, and optional paid providers are not free. Its own reference hardware estimate is about $69/month.
- The stack is designed for local-only exposure. Use an authenticated reverse proxy or SSH tunnel rather than changing every binding to `0.0.0.0`.
- Installing every plugin increases supply-chain and tool-permission risk. Prefer the smallest tier and plugin set that meets the workflow.

## Sources

- Evey Setup repository: <https://github.com/42-evey/evey-setup>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

