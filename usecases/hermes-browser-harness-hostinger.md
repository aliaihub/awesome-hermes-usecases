# Hermes + Browser Harness on Hostinger VPS

**Class:** Independent first-person deployment · **Confidence:** High · **Demo status:** Public gist, 54★ at writing

## Pain Point

You want Hermes running 24/7 with browser-automation capability — Browser Harness from Browser Use — but you don't want to manage Fly.io Machines, raw Hetzner boxes, or `systemd` units. A consumer VPS with a one-click installer is the simplest path. The catch: Browser Harness is a separate Python package that needs to be installed, registered as a Hermes skill, and wired to a Browser Use Cloud API key — steps that aren't in the official Hermes docs.

## What It Does

David Ondrej's GitHub Gist provides a copy-pasteable shell script that takes a fresh Hostinger VPS to a working Hermes + Browser Harness install in seven steps. The gist registers Browser Harness as a Hermes skill via symlinks so the agent can find it; sets up OpenRouter with Anthropic Claude Opus 4.7 as the model; installs `uv` (Astral's Python tool); and launches Hermes.

The end state: a 24/7 agent on a consumer-priced VPS that can drive a real Chromium browser via the Browser Use Cloud API (free tier, no card) — meaning the agent can log into SaaS, fill forms, scrape, and post, all from a Hermes chat.

**Use case:** an operator who wants browser-using Hermes on a simple VPS without writing the integration glue.

## Setup

The full script lives at the gist URL below. The seven steps, in order:

1. **Install Hermes** via the official installer.
2. **Reload the shell** so `hermes` is on `$PATH`.
3. **Configure Hermes** — pick OpenRouter, paste API key, select `anthropic/claude-opus-4.7` as the model.
4. **Install `uv`** (Astral's Python package manager).
5. **Install Browser Harness** from `browser-use/browser-harness`:
   ```bash
   uv tool install -e .
   ```
6. **Register Browser Harness as a Hermes skill** — symlink the `SKILL.md`, `interaction-skills/`, and `domain-skills/` into `~/.hermes/skills/browser-harness/`:
   ```bash
   mkdir -p ~/.hermes/skills/browser-harness
   ln -s $(pwd)/SKILL.md ~/.hermes/skills/browser-harness/SKILL.md
   ln -s $(pwd)/interaction-skills ~/.hermes/skills/browser-harness/interaction-skills
   ln -s $(pwd)/domain-skills ~/.hermes/skills/browser-harness/domain-skills
   ```
7. **Connect to Browser Use Cloud** (free tier, no card) and launch Hermes:
   ```bash
   hermes config set BROWSER_USE_API_KEY=...
   hermes
   ```

Total: about 10 minutes of copy-paste on a fresh Hostinger VPS.

## Prompts

The prompt pattern that uses Browser Harness from a Hermes chat:

```
Log into our company SSO, navigate to the invoices page, download every
PDF from the last 30 days, and rename them to
"invoice-<vendor>-<date>.pdf". Save into ~/inbox/invoices/.
```

Hermes sees the symlinked `browser-harness` skill, picks it up, and starts driving the browser. The skill instructions in `SKILL.md` guide the agent through Browser Use Cloud API calls.

## Skills Needed

- Hostinger VPS (any KVM 1 plan works; the gist doesn't pin a size)
- OpenRouter API key (or another supported LLM provider)
- Browser Use Cloud API key (free tier)
- `uv` for Python tool installation
- ~10 minutes of SSH time

## Notes

- **Hostinger is interchangeable with any KVM VPS.** The script doesn't use Hostinger-specific APIs. It works on Hetzner, DigitalOcean, Vultr, or any Ubuntu 24.04 box. Hostinger is just the author's choice.
- **Symlinks, not copies.** The skill registration uses symlinks so a `git pull` on Browser Harness updates the Hermes skill in place. Re-symlink only if the source repo moves.
- **Free tier limits.** Browser Use Cloud's free tier caps concurrent sessions and monthly tasks. Production scraping wants the paid tier.
- **Distinct from `hermes-on-flyio.md`.** That's Fly.io's IaaS (Machines, volumes, snapshots). This is a one-script consumer VPS setup. Distinct from `headless-daemon-server.md` (systemd on bare metal) — no service unit, no reboot safety, just a single shell script.
- **Distinct from `scicco-hermzner-hetzner.md`.** That entry is a production-hardened Terraform + Ansible setup with rootless Podman, Tailscale-only, and pinned image digests. This entry is the opposite end: 10-minute copy-paste, no hardening, no Tailscale. Pick by threat model.

## Sources

- **Primary:** David Ondrej, "all commands for Hermes Agent + Browser Harness setup" — GitHub Gist, Apr 19 2026. 54★, 16 forks at time of writing.
  <https://gist.github.com/davidondrej/6f158de34ce83c530526011054fde8d3>
- **Companion video:** "Hermes Agent + Browser Harness = Local AGI" — Frontier Models.
  <https://frontiermodels.cc/video/hermes-agent-browser-harness-local-agi/>
- **Official install reference:** Hermes Agent `install.sh`.
  <https://github.com/NousResearch/hermes-agent/blob/main/scripts/install.sh>

## Related Use Cases

- [Hermes on Fly.io](hermes-on-flyio.md) — managed infrastructure alternative
- [Headless Daemon Server](headless-daemon-server.md) — systemd + bare-metal alternative
- [scicco/hermzner on Hetzner](scicco-hermzner-hetzner.md) — production-hardened alternative on the same VPS class
- [Multi-Platform Research](multi-platform-research.md) — another use case that uses the same Browser Use pattern
