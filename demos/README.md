# Starter kits

Three small starting points for running a catalog workflow. Each includes a configuration template, a redacted dry run, a smoke check with a stated scope, sample input, and a manual end-to-end check.

| Kit | Result | Reference platform | Live prerequisites |
| --- | --- | --- | --- |
| [Daily briefing](daily-briefing/) | A reviewed, paused research schedule | Bash + Python 3.11+ | Hermes profile, model, search backend; optional Telegram |
| [Team Telegram](team-telegram/) | A shared bot configuration with a user allowlist | Linux, Bash + Python 3.11+ | Hermes profile, model, Docker, Telegram bot |
| [Open WebUI](openwebui/) | A local browser interface for a Hermes profile | Linux Docker Engine with host networking | Hermes profile, model, Docker Compose |

**Validation:** configuration and failure-path tests run offline. Real model responses, Telegram delivery, Docker containers, and browser interaction have not been exercised for this milestone. See [tested results](../docs/tested-results.md) for the exact boundary and reproduction commands.

Start with a fresh profile, configure its model through Hermes, copy that kit's `.env.example`, and run its setup with `--dry-run`. Dry runs require no Hermes installation, Docker daemon, provider key, or network access; they do require valid example values for the selected kit. Apply the setup only after reviewing the commands.

The examples were checked against [Hermes v0.22.5](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.5). Check `hermes version` and the upstream command help when using another version. The shared helper invokes local Hermes commands; it contains no model-provider API client.

The [Matt Pocock walkthrough](matt-pocock-skills/) contains planning artifacts rather than an executable fourth kit. For smaller building blocks, use the [recipe cookbook](../recipes/README.md).
