# Nous Portal Gateway (Single-OAuth, 300+ Models + Tool Gateway)

**Class:** Official integration · **Confidence:** High · **Demo status:** Docs + runbook

## Pain Point

You don't want to manage a drawer of provider API keys (OpenAI, Anthropic, xAI, …) just to get an agent running, and you don't want to wire up separate backends for the tools the agent needs — web search, image generation, TTS, browser automation. You want one login that unlocks a broad model catalog and the common tool surface, billed in one place.

## What It Does

Nous Portal is the maintainers' recommended default provider for Hermes. A single OAuth login covers **300+ models** plus a **Tool Gateway** (web search, image generation, TTS, browser automation) and Nous Chat. Hermes authenticates to it with scoped `inference:invoke` JWTs (with a legacy opaque session-key fallback), auto-tags every request with `client=hermes-client-v<version>`, and quarantines revoked refresh tokens to avoid replay loops.

One subscription, one auth flow, no per-provider key juggling. The `/model` switcher then reaches the whole Portal catalog mid-session.

## Setup

Fresh install:

```bash
hermes setup --portal      # OAuth login in browser, configures the Portal provider
```

Existing install — switch to Portal:

```bash
hermes model                # → pick "Nous Portal"
```

Inspect the active login and routing:

```bash
hermes portal info
```

Switch models mid-session across the Portal catalog:

```
/model nous:anthropic/claude-sonnet-4.6
/model nous:openai/gpt-5
```

## Skills Needed

- A Nous Portal account / subscription
- `hermes setup --portal` or `hermes model` to run the OAuth flow

## Notes

- **Portal is the low-friction default**, not a premium tier — the docs flag it as the recommended way to run Hermes. If you're deciding where to start, start here.
- **Tool Gateway is the real draw beyond models.** Web search, image gen, TTS, and browser automation come with the same login, so you don't need separate Firecrawl/Brave/TTS API keys for those capabilities.
- **Scoped JWTs, not long-lived master keys.** Refresh-token revocation is handled (quarantined on rejection) so a leaked token can't loop forever.
- If you outgrow the Portal catalog — a specific fine-tune, a local model, a regulated-cloud requirement — layer in another provider alongside it and switch with `/model`.

## Sources

- AI Providers docs (rendered, Nous Portal section): <https://hermes-agent.nousresearch.com/docs/integrations/providers/>
- Source-of-truth markdown: <https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md>