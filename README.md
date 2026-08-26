<p align="center">
  <img src="assets/hermes-agent-usecases.png" alt="Hermes Agent — Real-World Use Cases" width="800">
</p>

# Awesome Hermes Agent Use Cases

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
![Use Cases](https://img.shields.io/badge/usecases-55-blue?style=flat-square)
![Last Update](https://img.shields.io/github/last-commit/ali-erfan-dev/awesome-hermes-usecases?label=Last%20Update&style=flat-square)
![Stars](https://img.shields.io/github/stars/ali-erfan-dev/awesome-hermes-usecases?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

**A community collection of real-world [Hermes Agent](https://github.com/NousResearch/hermes-agent) use cases — each one backed by public evidence.**

| | This Catalog | Official Docs | X Threads | Reddit |
|---|---|---|---|---|
| Organized by category | ✅ | Partial | ❌ | ❌ |
| Runnable demos included | ✅ | ❌ | ❌ | ❌ |
| Primary source required | ✅ | ✅ | ❌ | ❌ |
| Community-maintained | ✅ | ❌ | ❌ | ❌ |

> [!NOTE]
> **Evidence rule.** Every use case here links to a primary source: an official Hermes doc, a Nous Research companion repo, a GitHub issue with deployment details, or a first-person blog post. If the only evidence is a tweet or "community build" marketing page, it lives in [`research/unverified.md`](research/unverified.md) instead — not in the catalog below.

## Quick start

New to Hermes Agent? The fastest path:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
```

Then pick a use case below. The [`/demos`](demos/) folder has three runnable starters: [Daily Briefing](demos/daily-briefing/), [Open WebUI](demos/openwebui/), and [Team Telegram](demos/team-telegram/).

## Categories

- [Automation & Scheduling](#automation--scheduling)
- [Messaging & Team Bots](#messaging--team-bots)
- [Coding & Developer Workflows](#coding--developer-workflows)
- [Frontends & UIs](#frontends--uis)
- [Home & Device Control](#home--device-control)
- [Content & Creative Pipelines](#content--creative-pipelines)
- [Orchestration & Multi-Agent](#orchestration--multi-agent)
- [Memory & Context](#memory--context)
- [Observability & Operations](#observability--operations)
- [Security & Assurance](#security--assurance)
- [Finance & Trading](#finance--trading)
- [Deployment Patterns](#deployment-patterns)
- [Research & Training](#research--training)

## Automation & Scheduling

| Name | Description |
| --- | --- |
| [Daily Briefing Bot](usecases/daily-briefing-bot.md) | A scheduled agent that researches topics every morning and delivers a summary to Telegram or Discord. The canonical "hello world" of Hermes automation. |
| [Zero-Token Notifications](usecases/zero-token-notifications.md) | Cron jobs that only wake the LLM when something actually changed — pre-filter with a Python script, only pay for tokens on meaningful signal. |
| [Intent-to-Artifacts Workflow](usecases/intent-to-artifacts.md) | A personal workflow for turning rough prompts into runbooks, RSS curation, diagrams, and notes — delivered to Telegram + markdown files. |
| [X Social Automation Toolset](usecases/x-social-automation-toolset.md) | A native Hermes plugin for X/Twitter search, account reads, trend checks, and operator-approved actions through Xquik. |
| [Inbox → Slack Daily Digest](usecases/inbox-slack-daily-digest.md) | A weekday 9am cron that classifies your inbox and posts a needs-reply / FYI digest to a Slack channel. No auto-replies. |
| [Sequenzy Email Marketing Agent](usecases/sequenzy-email-marketing-agent.md) | Use Hermes with Sequenzy skills/CLI to draft lifecycle campaigns, manage subscriber workflows, send tests, and monitor email stats. |

## Messaging & Team Bots

| Name | Description |
| --- | --- |
| [Team Telegram Assistant](usecases/team-telegram-assistant.md) | Always-on shared bot for a small team — coding, research, ops — with per-user sessions, Docker-isolated terminal, and an allowlist. The gateway also supports Discord, Slack, WhatsApp, Signal, Matrix, Email, SMS, and more; the Telegram flow is the cleanest starting point for any of them. |
| [Enterprise Messaging (Feishu / WeCom)](usecases/enterprise-messaging-feishu-wecom.md) | Production-style Hermes deployments on Chinese enterprise chat platforms — Feishu managed under `launchd`, WeCom with native media-and-vision analysis. |
| [Voice Assistant Workflows](usecases/voice-assistant.md) | Three modes: CLI mic loop, voice notes in Telegram/Discord, and a Discord voice-channel bot. Same agent, same memory, voice-only I/O. |
| [Hermes Live Voice](usecases/hermes-live-voice.md) | A community voice gateway + Dashboard plugin that keeps a continuous, interruptible voice session open while durable Hermes `/v1/runs` execute in the background — bounded progress, steer/stop by task ID, completion notices after reconnect. |

## Coding & Developer Workflows

| Name | Description |
| --- | --- |
| [GitHub PR Review (cron)](usecases/github-pr-review-cron.md) | Periodic PR review without opening a webhook endpoint. Authenticated `gh`, a review skill, and a cron job. |
| [GitHub PR Review (webhook)](usecases/github-pr-review-webhook.md) | Real-time PR comments via a signed GitHub webhook. End-to-end event-driven code review. |
| [Production Software-Dev Workflow](usecases/production-software-dev-workflow.md) | A field report of daily production development on Hermes — long sessions, delegation, memory, one 12-hour run with ~2.6M replay tokens. |
| [Local Model Quantization with TurboQuant](usecases/dev-local-model-quantization.md) | Optimize MLX models (Qwen3.5-9B) for local Apple Silicon inference using domain-specific skills — apply, benchmark, document, publish. |
| [Hermes VS Code Workspace Stream](usecases/hermes-vscode-workspace-stream.md) | A VS Code sidebar over Hermes ACP for streaming chat, tool output, editor context, attached files, model switching, and persistent workspace sessions. |
| [Function-Calling Patterns](usecases/function-calling-patterns.md) | The `Hermes-Function-Calling` companion repo as a pattern library — yfinance financial data, Pydantic JSON mode, GOAP scratch-pad planning, `@tool` registration, recursive multi-hop via `--max_depth`. |

## Frontends & UIs

| Name | Description |
| --- | --- |
| [Open WebUI Frontend](usecases/open-webui-frontend.md) | Point Open WebUI at the Hermes API server to get a full browser chat frontend for the agent, with session continuity. |
| [TUI Operator Console](usecases/tui-operator-console.md) | Keyboard-first terminal HUD for managing your agent — live sessions, skills toggle, cron, logs, config editing, multiple themes. |

## Home & Device Control

| Name | Description |
| --- | --- |
| [Home Assistant Control](usecases/home-assistant-control.md) | Conversational control of a smart home via four built-in HA tools — list entities, read state, call services. |
| [Android Device Control](usecases/android-device-control.md) | Remote phone control from a Hermes chat — 36 `android_*` tools for taps, swipes, screenshots, and screen reading via a relay app. |
| [Hermes iOS Native Engine](usecases/hermes-ios-native-engine.md) | A self-hosted iPhone companion with relay, connector, MCP sensor tools, voice, camera attachments, widgets, location, activity, and HealthKit context. |
| [Personal AI Hub: Apple Health + Threads + Gmail + Calendar](usecases/personal-ai-hub-apple-health-threads-gmail.md) | Desktop Hermes + Telegram Topics that wires Apple Health, Threads (via open-source skill), Gmail, and Google Calendar into a single chat surface with cross-domain queries. |

## Content & Creative Pipelines

| Name | Description |
| --- | --- |
| [Autonovel — House of Bells](usecases/autonovel-house-of-bells.md) | End-to-end autonomous novel, art, and audiobook production. Nous Research's own pipeline shipped a 19-chapter, 79,456-word book with an audiobook and a website. |
| [Printing-Factory Task Memory](usecases/printing-factory-task-memory.md) | A custom skill that fixes long-context slowness and forgetting during daily factory operations. Local JSON index with sub-second retrieval. |
| [Screen Recording → Tutorial Video](usecases/creative-screen-recording-video.md) | Feed Hermes a raw screen recording and get a finished tutorial video on HeyGen with your AI avatar — script generation, video production, and memory of preferences for repeat work. |
| [ComfyUI Workflow Orchestration](usecases/comfyui-workflow-orchestration.md) | Install, launch, and run ComfyUI node-based media generation workflows on demand — from Stable Diffusion to video pipelines, with automatic custom-node installation and deterministic output management. |
| [AI Video Generation: HTML-to-MP4](usecases/video-generation-html-to-mp4.md) | Hermes writes designed HTML compositions (via Open Design), then renders to MP4 via HyperFrames — GSAP animations, shader transitions, TTS narration, all code-driven with no timeline editor. |

## Orchestration & Multi-Agent

| Name | Description |
| --- | --- |
| [Paperclip Managed Employee](usecases/paperclip-managed-employee.md) | Hermes running as a worker inside Nous Research's Paperclip task-orchestration system, with persistent sessions and checkpoints. |
| [Self-Evolution](usecases/self-evolution.md) | A GEPA + DSPy loop that optimizes your Hermes skills, prompts, and tool text, producing PR-ready improvements for a few dollars per run. |
| [Zouroboros Swarm Bridge](usecases/zouroboros-swarm-bridge.md) | Hermes as one of four interchangeable executors (Claude Code, Codex, Gemini, Hermes) inside a third-party multi-agent orchestrator. Bash-bridge adapter pattern with shared identity. |
| [Matt Pocock Skills + Sub-Agents](usecases/matt-pocock-skills-subagents.md) | Use Matt Pocock's open-source skills (`/grill-me`, `/to-prd`, `/to-issues`) for planning and scoping, then Hermes sub-agents for parallel implementation of vertical-sliced issues — with HITL gates to stop AI slop before it ships. |
| [Dynamic Skill Dojo](usecases/dynamic-skill-dojo.md) | A monitoring and improvement loop that reads session history, ranks weak skills, proposes patches or new skills, invokes self-evolution, and reports learning progress. |
| [Hermes Kanban: Multi-Agent Swarm from Slack](usecases/kanban-multi-agent-swarm.md) | The v0.15 `/kanban` slash command turns a Slack message into a durable multi-agent swarm with named workers, a verifier, and a synthesizer — persistent via `~/.hermes/kanban.db`. |
| [Deterministic Workflow Delegation](usecases/deterministic-workflow-delegation.md) | Hermes keeps the judgment, a deterministic runner keeps the receipts: repeatable jobs graduate from chat into checked `.nika.yaml` DAG files — audited before any token is spent, budget-capped, with tamper-evident run traces. Offline demo, zero keys. |

## Memory & Context

| Name | Description |
| --- | --- |
| [YantrikDB Cognitive Memory (via MCP)](usecases/yantrikdb-memory-mcp.md) | Replace or augment native memory with a dedicated cognitive DB — vector + knowledge graph + temporal decay + contradiction detection. Integrates over MCP, so no Hermes plugin needed. |
| [Obsidian Vault as a Second Brain](usecases/obsidian-second-brain.md) | Wire Hermes into an Obsidian vault for persistent knowledge — read notes, create daily dashboards, cross-reference tags, maintain a self-improving personal knowledge base. |

## Observability & Operations

| Name | Description |
| --- | --- |
| [Hermes Labyrinth Observability](usecases/hermes-labyrinth-observability.md) | A read-only dashboard plugin that turns prompts, tool calls, failures, approvals, model switches, cron runs, and memory hits into auditable agent journeys. |

## Security & Assurance

| Name | Description |
| --- | --- |
| [Autonomous Penetration Testing with Kali](usecases/autonomous-penetration-testing.md) | A Kali-backed Hermes skill for authorized security assessments with scope confirmation, playbooks, zero-findings fallback, approval gates, and structured reports. |

## Finance & Trading

| Name | Description |
| --- | --- |
| [Weather Trading on Polymarket](usecases/weather-trading-polymarket.md) | Autonomous weather prediction-market trading — Kelly Criterion position sizing, EV scoring against market odds, self-calibrating with real traders reporting $300→$123K in 3 months on a $5 VPS. |
| [ERPClaw: Plain-English ERP and Accounting](usecases/erpclaw-plain-english-erp.md) | Self-hosted double-entry ERP and accounting run from chat. Invoicing, inventory, payroll, and multi-company books, written to a local database by deterministic skill actions. |
| [First-Dollar Business Guidance](usecases/first-dollar-business-guidance.md) | Hermes Startup: a local-first skill that turns your personal profile into 3 of 10 evidence-labeled ideas, one bounded next action, and a prepaid per-call tool balance — no subscription, no income guarantee. |

## Deployment Patterns

| Name | Description |
| --- | --- |
| [Hermes on Fly.io](usecases/hermes-on-flyio.md) | Official Fly-apps deployment guide — run Hermes as a Fly Machine with a volume-backed `/opt/data`, daily snapshots, and ~$15/month baseline. |
| [Local & Proxy Model Backends](usecases/local-and-proxy-models.md) | Run Hermes against Ollama, vLLM, oMLX, or a custom OpenAI-compatible proxy — for cost control, data locality, or model choice beyond the defaults. |
| [Local Model Auto-Detection](usecases/local-model-auto-detection.md) | Hermes probes your local inference server, identifies the running model, detects context window, and auto-configures — eliminates first-setup friction for Ollama, llama.cpp, MLX, and vLLM. |
| [Headless Daemon Server](usecases/headless-daemon-server.md) | A self-managed Linux VPS pattern that runs Hermes gateway and native cron under `systemd` with a dedicated service user and reboot-safe scheduling. |
| [Hermes + Browser Harness on Hostinger](usecases/hermes-browser-harness-hostinger.md) | A 10-minute copy-paste script (54★ gist) that wires Browser Use's Browser Harness as a Hermes skill on a consumer VPS — symlinked skill, OpenRouter, Browser Use Cloud free tier. |
| [scicco/hermzner: Hardened Hermes on Hetzner](usecases/scicco-hermzner-hetzner.md) | Terraform + Ansible setup for a Hetzner VPS with rootless Podman, Tailscale-only network, UFW default-deny, read-only root FS, and pinned image digests. Production-grade, `nascent` (3★). |
| [Enterprise Cloud (Bedrock / Azure AI Foundry / NVIDIA Build)](usecases/enterprise-cloud-deployment.md) | First-class provider IDs for the three major enterprise model gateways — Bedrock Converse API + Guardrails, Azure Foundry endpoint, NVIDIA NIM cloud or self-hosted. For regulated / procurement-constrained shops. |
| [China-Region LLM Endpoints](usecases/china-region-llm-endpoints.md) | Dedicated China-facing provider IDs for Kimi/Moonshot, MiniMax, and z.ai/GLM — auto-probing endpoints, no hand-wired base URLs. Pair with Feishu/WeCom for a fully domestic stack. |
| [Nous Portal Gateway](usecases/nous-portal-gateway.md) | The maintainers' recommended default — one OAuth login unlocks 300+ models plus a Tool Gateway (web search, image gen, TTS, browser) and Nous Chat. Scoped JWTs, no per-provider key juggling. |
| [Coding-Tool Subscriptions as Backends (Copilot / Codex / Claude Max)](usecases/oauth-cloud-providers.md) | Reuse existing coding-tool subscriptions as Hermes model backends — Copilot direct + ACP, Codex device-code OAuth, Claude Max extra-usage OAuth — with native auth and 401 one-shot recovery. |

## Research & Training

| Name | Description |
| --- | --- |
| [Multi-Platform Social Media Research](usecases/multi-platform-research.md) | Run a single query across Reddit, X/Twitter, YouTube, Hacker News, and Polymarket via a single Python engine. Firefox-cookie auth for X, no API key needed on WSL. Delivered as a unified markdown brief to Telegram or local storage. |
| [RL Training & Benchmarks](usecases/rl-training-benchmarks.md) | Use Hermes environments to train and evaluate tool-calling models. The TBLite benchmark covers 100 tasks with strong correlation to TB2. |
| [ClawBench Browser-Agent Evaluation](usecases/clawbench-browser-agent-evaluation.md) | Run Hermes against isolated live-web tasks with native browser tools over CDP, interception-based scoring, and five-layer traces for debugging. |
| [Browser & Admin UIs](usecases/browser-admin-uis.md) | The official web dashboard plus community UIs — browser access to sessions, files, cron, and control plane. |

## Runnable demos

Three starter demos live in [`/demos`](demos/). Each has a `README.md`, a `.env.example`, and a one-command setup:

- [**daily-briefing**](demos/daily-briefing/) — cron + web search + Telegram delivery
- [**matt-pocock-skills**](demos/matt-pocock-skills/) — planning pipeline (`/grill-with-docs` → `/to-issues`) + verification script demo
- [**openwebui**](demos/openwebui/) — Hermes API server + Open WebUI via Docker Compose
- [**team-telegram**](demos/team-telegram/) — gateway + Telegram + Docker terminal backend

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: **one primary source minimum** — official docs, a Nous companion repo, a GitHub issue with real deployment detail, or a first-person blog post. X posts and "community build" marketing pages don't count as primary evidence.

### For Contributors

Every PR that touches `usecases/*.md` triggers automated verification. Learn how it works and how to pass it:

- [docs/verification-criteria.md](docs/verification-criteria.md) — how scoring works, what's green vs yellow vs red, and how to run the script locally before submitting
- `python scripts/verify-usecase.py --usecase usecases/my-topic.md --check all` — generate your own verification report

> Please only submit use cases you have personally run (at least once) or that you can trace to a primary public source. No crypto use cases.

## License

[MIT](LICENSE) for code and configs. Docs and diagrams under [CC BY 4.0](LICENSE-docs).

## Acknowledgements

Catalog format inspired by [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases). Hermes Agent is built by [Nous Research](https://nousresearch.com).
