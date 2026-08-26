# Hermes Live Voice

**Class:** Ecosystem integration
**Confidence:** Medium-High
**Demo status:** Docs + runbook

## Pain Point

The first-party voice modes are a mic loop or a voice note: one turn in, one turn out. They don't fit the case where you delegate a long-running task to Hermes and want to keep talking — ask for bounded progress, steer it, or get told when it's done — while the run continues in the background. Holding open a continuous, interruptible voice session while durable Hermes work runs independently is a different pattern than push-to-talk.

## What It Does

Hermes Live Voice is a community-built MIT voice gateway + Dashboard plugin for Hermes Agent. It keeps a continuous realtime voice session open (VAD + barge-in) while delegated work runs as a separate Hermes `/v1/runs` worker — one run per accepted task, not a subagent team per request. You speak to a new or saved Hermes chat, delegate longer work, keep talking while the run continues, ask for bounded progress, stop or steer a task by its exact task ID, and get spoken completion notices plus a persistent task inbox after reconnect.

Ingress: voice (local S2S, Gemini Live, or OpenAI Realtime) → gateway → Hermes `/v1/runs` worker → bounded progress events + task inbox → spoken/toast delivery.

## Setup

```bash
npm install --global hermes-live-voice
hermes-live setup        # writes ~/.hermes/hermes-live/config.env, picks a free local port
hermes dashboard         # load the Dashboard plugin
hermes-live launch-check # pre-demo/prod gate: rejects mock mode, validates voice provider, plugin, gateway, one bounded worker
```

Requirements: Hermes Agent 0.18.2+ (tested through 0.20.0), Node.js 20+. For the managed local voice stack on Apple Silicon: `uv` + ≥12 GB RAM (16 GB Apple Silicon Mac recommended). Non-Apple-Silicon hosts run the upstream realtime server and point `HERMES_LIVE_LOCAL_URL` at it.

Config lives at `$HERMES_HOME/hermes-live/config.env` (private perms). Env vars override the managed config; project `.env` files are never loaded or executed. Task state is single-writer at `~/.hermes/hermes-live/tasks-v1.json`.

## Prompts

Spoken, same as typed — the voice layer is I/O only. The useful shapes are the ones the mic loop can't do:

```text
Start a new chat. I want you to refactor the auth module and run the test suite — take your time, I'll keep talking.
```

While that run is live:

```text
Where is it up to? Just the bounded progress, not the full log.
```

```text
Stop task <task-id>.  // stopping always targets the exact task ID; barge-in never cancels work
```

After a disconnect/reconnect:

```text
What finished while I was away?
```

## Skills Needed

- Hermes Agent 0.18.2+ with the Dashboard plugin enabled
- `hermes-live-voice` npm package (global)
- A voice provider: local S2S (Apple Silicon), Gemini Live, or OpenAI Realtime
- Hermes `/v1/runs` durable runs (one worker per accepted task)
- For non-loopback binds: a strong `HERMES_LIVE_AUTH_TOKEN`, exact allowed origin, TLS, and edge rate limits

## Notes

- Community-built, MIT, not an official NousResearch distribution. State that honestly (Class: Ecosystem integration).
- **Durability ceiling:** in-progress Hermes runs do *not* survive a Hermes Agent restart. Missing/ambiguous outcomes become `unknown`. This is the main gotcha vs. a true durable queue.
- **Single-process file store:** for one gateway process, not multi-tenant or multi-node. Don't front it with multiple writers.
- **Parallelism is opt-in and policy-based:** requires `HERMES_LIVE_TRUST_DECLARED_READ_ONLY=true`, and model-declared read-only scope is policy input, not a sandbox. Don't treat it as isolation.
- After npm updates: `hermes-live upgrade` then `hermes-live launch-check`.
- `/quit` in the terminal client detaches; it does not cancel work.

## Sources

- Repo (primary, first-party third-party, Hermes explicitly in architecture): https://github.com/bielcarpi/hermes-live-voice
- Release v1.0.0: https://github.com/bielcarpi/hermes-live-voice/releases/tag/v1.0.0
- npm package: https://www.npmjs.com/package/hermes-live-voice