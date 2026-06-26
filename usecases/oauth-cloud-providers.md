# Reusing Coding-Tool Subscriptions as Hermes Backends (Copilot / Codex / Claude Max)

**Class:** Official integration · **Confidence:** High · **Demo status:** Config patterns

## Pain Point

You already pay for GitHub Copilot, OpenAI Codex, or a Claude Max plan with extra-usage credits. Standing up Hermes on top of yet another API spend feels wasteful. You want Hermes to authenticate against the coding-tool subscription you already have — OAuth where the tool uses OAuth, API key where it uses a key — and to recover gracefully when a token expires mid-run.

## What It Does

Hermes ships first-class provider IDs for the three major coding-tool backends, each matching the subscription's native auth method instead of forcing a separate API key purchase.

- **GitHub Copilot (direct API)** — provider `copilot`. Auth chain: `COPILOT_GITHUB_TOKEN` → `GH_TOKEN` → `GITHUB_TOKEN` → `gh auth token`. Accepts OAuth (`gho_`), fine-grained PAT (`github_pat_`), and GitHub App (`ghu_`) tokens — **not** classic PATs (`ghp_*`). On HTTP 401 it does a one-shot credential recovery (re-resolves token, rebuilds client, retries once). GPT-5+ models auto-use the Responses API; others use Chat Completions.
- **GitHub Copilot (ACP backend)** — provider `copilot-acp`. Spawns the local Copilot CLI as a subprocess and speaks ACP to it. Requires the Copilot CLI in PATH and an existing `copilot login`. Overridable via `HERMES_COPILOT_ACP_COMMAND` / `HERMES_COPILOT_ACP_ARGS` (defaults `copilot` / `--acp --stdio`).
- **OpenAI Codex (device-code OAuth)** — provider `openai-codex`. Authenticates by device code (open a URL, enter a code). **No Codex CLI install required.** Credentials land in `~/.hermes/auth.json` and can be imported from `~/.codex/auth.json`. On refresh failure (HTTP 4xx / `invalid_grant`), marks the refresh token dead; re-login with `hermes auth add codex-oauth`.
- **Anthropic / Claude Max "extra usage"** — provider `anthropic` (aliases `claude`, `claude-code`). Three auth methods: API key (`ANTHROPIC_API_KEY`, pay-per-token); OAuth via `hermes model` (only works on a Claude Max plan with purchased extra-usage credits); setup-token (`ANTHROPIC_TOKEN`, legacy/fallback). Hermes prefers Claude Code's own credential store over copying the token into `~/.hermes/.env` and auto-detects existing Claude Code credential files.

## Setup

### GitHub Copilot (direct)

```bash
# easiest: let Hermes reuse your gh login
gh auth login            # once, if not already
```

```yaml
# ~/.hermes/config.yaml
model:
  provider: "copilot"
  default: "gpt-5.4"
```

### OpenAI Codex (device-code OAuth)

```bash
hermes model              # → "OpenAI Codex" → device-code flow in browser
# or import an existing Codex login:
#   credentials copied from ~/.codex/auth.json into ~/.hermes/auth.json
```

If the refresh token dies later:

```bash
hermes auth add codex-oauth
```

### Anthropic / Claude Max

```bash
hermes model              # → "Anthropic" → OAuth (needs Claude Max + extra-usage credits)
# or API key:
#   export ANTHROPIC_API_KEY=sk-ant-...
```

```yaml
# ~/.hermes/config.yaml
model:
  provider: "anthropic"
  default: "claude-sonnet-4-6"
```

## Skills Needed

- An active Copilot subscription (direct) or Copilot CLI + `copilot login` (ACP mode)
- A Codex / OpenAI coding-plan account for the device-code flow
- For Claude Max: the Max plan **with purchased extra-usage credits** (plain Max without extra usage won't OAuth); or an `ANTHROPIC_API_KEY` for the pay-per-token path

## Notes

- **Token-type restrictions are real.** Copilot's direct API rejects classic `ghp_*` PATs — use a fine-grained PAT or an OAuth/App token. Don't waste time debugging a 401 on a classic PAT.
- **The 401 one-shot recovery on Copilot** means a transient auth blip won't kill your session; a persistent 401 means the token is actually invalid and you re-`gh auth login`.
- **Claude Max OAuth is conditional** — only plans with extra-usage credits. If `hermes model` OAuth fails and you're on plain Max, fall back to an API key.
- **ACP-mode Copilot vs direct-API Copilot** differ in process model: direct API is an HTTP client; ACP spawns the local CLI subprocess. Direct API is simpler; ACP is useful when you want the CLI's own session/auth handling.
- Mid-session switching (`/model copilot:gpt-5.4`, `/model anthropic:claude-sonnet-4-6`) lets you spend cheap tokens for routine work and reserve your subscription's quota-billed models for the hard parts.

## Sources

- AI Providers docs (rendered, Copilot / Codex / Anthropic sections): <https://hermes-agent.nousresearch.com/docs/integrations/providers/>
- Source-of-truth markdown: <https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md>