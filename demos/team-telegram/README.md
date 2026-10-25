# Team Telegram starter

Configure a fresh Hermes profile for a small, trusted team's Telegram bot. This follows the [Team Telegram Assistant](../../usecases/team-telegram-assistant.md) pattern.

## Requires

- Linux, Bash, Python 3.11+, and Hermes compatible with v0.22.5.
- Docker with a running daemon.
- A bot token from [BotFather](https://t.me/BotFather) and numeric user IDs for permitted teammates.
- A fresh profile with its own configured model. Do not clone a personal profile into a shared bot.

Telegram sessions are separated, but teammates still use one Hermes profile: its persistent memory, credentials, configured tools, and accessible resources are shared. A Docker terminal backend applies to shell tools; it does not provide full tenant isolation for every integration. Use separate profiles and credentials when people need separate trust boundaries.

## Setup

From this directory:

```bash
hermes profile create team-demo
hermes --profile team-demo setup
cp .env.example .env
```

Fill in the bot token and comma-separated positive user IDs. Keep bot credentials out of commits; `.env` files are ignored. Review the commands, then apply:

```bash
bash setup.sh --dry-run
bash setup.sh
bash smoke.sh
```

The scripts locate `.env` beside themselves or accept `--env-file /absolute/path/to/settings.env`. They parse literal values without executing shell expressions.

Setup checks the Docker daemon before changing settings. It persists `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS`, disables the broad allow-all settings, and selects `terminal.backend=docker` using the selected profile. An optional home channel is saved for scheduled delivery. It does not install services or start a bot.

Start the profile's gateway:

```bash
hermes --profile team-demo gateway
```

Use a fresh profile so old group allowlists, guest-mode settings, plugins, and other access rules do not silently broaden this example. For an existing profile, review the full [Telegram access configuration](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram) before sharing it.

## Sample input and expected output

From an allowlisted account, DM the bot:

```text
Reply with exactly PONG. Do not call any tools.
```

Expected final text: `PONG`. This is an acceptance target, not a captured response. A model request can incur charges.

## Checks

`smoke.sh` checks the CLI, Docker daemon, selected backend, configured allowed-user list, and broad allow-all settings. It does not authenticate to Telegram, inspect every possible access rule, execute shell tools inside Docker, or exercise the model.

Manual live acceptance:

1. Confirm the allowlisted account receives the response above.
2. Confirm a second allowlisted teammate gets a distinct session.
3. Confirm an unlisted account does not receive an agent response.
4. Ask the bot to run a harmless `pwd`; inspect the Docker backend's execution to confirm where the command ran.

Record the Hermes/model versions, environment, date, and results using the [test record template](../../docs/tested-results.md#recording-a-live-test). None of these live checks has been performed for this milestone.

Stop the foreground gateway with Ctrl+C. For service operation, follow the upstream gateway instructions; recheck the allowlist after configuration changes.

## Sources

- [Official team tutorial](https://hermes-agent.nousresearch.com/docs/guides/team-telegram-assistant)
- [Telegram settings and access rules](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)
- [v0.22.5 environment-key routing](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/config_env_routing.py)
- [Profile guide](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
