# China-Region LLM Endpoints (Kimi/Moonshot, MiniMax, z.ai/GLM)

**Class:** Official integration · **Confidence:** High · **Demo status:** Config patterns

## Pain Point

You want Hermes reachable for users in mainland China, or you want to run on domestic Chinese models for cost, latency, or regulatory reasons. The global endpoints (OpenAI, Anthropic, OpenRouter) are unreliable or blocked from inside the GFW, and hand-configuring each domestic provider's base URL and auth is tedious. You need first-class provider entries that just work against the China-facing API surfaces.

## What It Does

Hermes ships dedicated China-region provider IDs for the three most-used domestic model families, distinct from their global endpoints. Set one env var and pick the model — no custom base URL to hand-wire (except where you want to override).

- **Kimi / Moonshot (China)** — provider `kimi-coding-cn` (aliases `kimi-cn`, `moonshot-cn`), endpoint `api.moonshot.cn`, auth via `KIMI_CN_API_KEY`.
- **MiniMax (China)** — provider `minimax-cn`, auth via `MINIMAX_CN_API_KEY`, base URL overridable with `MINIMAX_CN_BASE_URL`.
- **z.ai / GLM** — provider `zai`, auth via `GLM_API_KEY`. Hermes auto-probes multiple endpoints (global, China, coding variants) to find the one that accepts your key — no manual `GLM_BASE_URL`.

These are separate from the global MiniMax (`minimax`) and the messaging-gateway story. Pair with the Chinese enterprise-chat deployment (Feishu / WeCom) for a fully domestic stack: Chinese chat surface + Chinese model backend.

## Setup

```bash
# ~/.hermes/.env — pick the family/ies you have keys for
KIMI_CN_API_KEY=sk-...
MINIMAX_CN_API_KEY=...
GLM_API_KEY=...
```

```yaml
# ~/.hermes/config.yaml — Kimi/Moonshot China
model:
  provider: "kimi-coding-cn"
  default: "kimi-k2-0905-preview"
```

```yaml
# MiniMax China (override base URL only if you need a mirror)
model:
  provider: "minimax-cn"
  default: "MiniMax-M1"
  # minimax_cn_base_url: "https://api.minimax.chat/v1"
```

```yaml
# z.ai / GLM — auto-probes, no base URL needed
model:
  provider: "zai"
  default: "glm-4.6"
```

Switch mid-session the usual way:

```
/model kimi-coding-cn:kimi-k2-0905-preview
/model zai:glm-4.6
```

## Skills Needed

- API key(s) from Moonshot, MiniMax China, and/or z.ai (Bigmodel)
- For a full domestic deployment: a Chinese messaging surface (Feishu / WeCom — see `enterprise-messaging-feishu-wecom.md`) hosted where the domestic endpoint is reachable

## Notes

- **Distinct from the global endpoints.** `minimax` (global) and `minimax-cn` are different provider IDs with different auth and base URLs — don't confuse them.
- **z.ai auto-probing is the low-friction option** if you're unsure which GLM endpoint your key is provisioned for. The others require the right key for the right endpoint.
- **Context windows on domestic models vary** and some coding variants are tuned for code over chat. Pick the model variant matching your workload (`kimi-coding-cn` for code, plain `kimi-cn` for general).
- Network egress matters: if Hermes runs outside China, these endpoints may be slow or blocked. Host the agent in-region for the latency win.

## Sources

- AI Providers docs (rendered, China-region section): <https://hermes-agent.nousresearch.com/docs/integrations/providers/>
- Source-of-truth markdown: <https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md>
- Related deployment pattern: [Enterprise Messaging (Feishu / WeCom)](enterprise-messaging-feishu-wecom.md)