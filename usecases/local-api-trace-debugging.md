# Local API Trace Debugging with claude-tap

**Class:** Ecosystem integration · **Confidence:** High · **Demo status:** Runnable local proxy and viewer

## Pain Point

When Hermes behaves unexpectedly, terminal output rarely reveals the exact system prompt, accumulated messages, tool schema, tool result, or provider request that caused it. Hosted observability can also be unsuitable for sensitive agent traces.

## What It Does

`claude-tap` launches Hermes through a local forward proxy and records the actual provider traffic. Its self-contained browser viewer exposes:

- System prompts, messages, tool definitions, calls, and results.
- Reconstructed streaming output and token usage.
- Structural diffs between adjacent requests.
- Full-text search, model grouping, path filtering, and portable HTML export.

It complements Hermes Labyrinth: Labyrinth maps semantic agent journeys from Hermes state, while `claude-tap` inspects the model-provider HTTP context itself.

## Setup

Install with Python 3.11+:

```bash
uv tool install claude-tap
# or
pip install claude-tap
```

Launch an interactive Hermes session through the local proxy:

```bash
claude-tap --tap-client hermes
```

To capture model calls triggered by Telegram, Slack, or another configured channel:

```bash
claude-tap --tap-client hermes -- gateway start
```

The wrapper keeps the gateway in the foreground so it inherits the proxy configuration and opens the live trace viewer by default.

## Prompts

Use the normal Hermes prompt that reproduces the behavior under investigation. For gateway tracing, send it through the configured messaging platform after starting the tapped gateway; an idle gateway makes no model request and therefore produces no trace.

## Skills Needed

- Python 3.11+ and `claude-tap`
- A working Hermes Agent installation and model provider
- Optional configured Hermes messaging platform for gateway traces
- Browser access to the local trace viewer

## Notes

- Common authentication headers are redacted, but prompts and tool results can still contain secrets or personal data. Treat exported HTML as sensitive.
- Forward proxy mode is the Hermes default because its supported providers generally honor `HTTPS_PROXY`.
- Reverse mode is only useful when Hermes is configured with an OpenAI-compatible provider that honors `OPENAI_BASE_URL`.

## Sources

- claude-tap repository and Hermes examples: <https://github.com/liaohch3/claude-tap>
- claude-tap guide: <https://liaohch3.com/claude-tap/>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

