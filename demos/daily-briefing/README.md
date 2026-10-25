# Daily briefing starter

Create a **paused** daily research job, inspect it, and enable it when its output is useful. This implements the [Daily Briefing Bot](../../usecases/daily-briefing-bot.md) pattern.

## Requires

- Bash, Python 3.11+, and Hermes compatible with v0.22.5.
- A dedicated Hermes profile with a working model and search backend. Firecrawl is optional when another supported search backend is already configured.
- A running gateway for scheduled execution.
- For Telegram: this profile's configured bot and the numeric destination chat ID.

## Setup

From this directory:

```bash
hermes profile create briefing-demo
hermes --profile briefing-demo setup
cp .env.example .env
```

Set the schedule/name in `.env`. Values are literal; quote values containing spaces. The scripts read this file beside themselves, even when invoked from another directory. They also accept `--env-file /absolute/path/to/settings.env`.

A five-field schedule uses the Hermes profile's timezone. Check it before enabling the job; set `HERMES_TIMEZONE` through Hermes if needed. A service does not inherit temporary exports from your current shell. An optional `FIRECRAWL_API_KEY` supplied in this kit's `.env` is persisted to the selected Hermes profile by setup.

Preview, then apply:

```bash
bash setup-local.sh --dry-run
bash setup-local.sh
hermes --profile briefing-demo cron list
```

Setup creates one **paused** job and prints the upstream CLI's success status without echoing credentials. It does not start a gateway or execute research. Rerunning creates another paused job; use `cron edit JOB_ID` to change an existing job or `cron remove JOB_ID` to remove it.

For Telegram, first configure this profile with `hermes --profile briefing-demo gateway setup`. Set `TELEGRAM_CHAT_ID` in `.env`, then use `setup-telegram.sh` instead of `setup-local.sh`. The destination is explicit (`telegram:CHAT_ID`); an allowed user ID and a delivery chat ID are different settings.

## Sample input and expected output

[prompt.txt](prompt.txt) is the actual scheduled prompt. It requests up to three recent, source-linked items and an honest limitation when search is unavailable. Edit it before creating the job.

Expected output shape (illustrative, not a captured model response):

```text
Briefing — <date>
1. <headline> — <publication date>
   <two-sentence summary>
   Why it matters: <practical implication>
   Source: <original URL>
```

A valid limitation report is preferable to invented stories or links.

## Checks

```bash
bash smoke.sh
```

This checks the profile CLI and cron-store readability. It does not check the scheduler heartbeat, model access, search, output quality, or delivery.

To perform the live acceptance check, start the gateway in another terminal:

```bash
hermes --profile briefing-demo gateway
```

Then select the job's ID from `cron list` and queue one run:

```bash
hermes --profile briefing-demo cron run JOB_ID
hermes --profile briefing-demo cron runs JOB_ID
```

The run is queued for a scheduler tick; command success alone does not mean it completed. Inspect its execution record, source links, and saved output under that profile's `cron/output/`; for Telegram, also confirm the message reached the intended chat. This invokes the configured model and may incur provider/search charges.

Once the live check passes:

```bash
hermes --profile briefing-demo cron resume JOB_ID
```

Keep the gateway running or install its service using upstream instructions. Pause with `cron pause JOB_ID`; remove with `cron remove JOB_ID`.

## Validation and sources

Offline behavior is covered in [tested results](../../docs/tested-results.md). Live execution is pending.

- [Official briefing tutorial](https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot)
- [Cron reference](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [v0.22.5 command parser](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/subcommands/cron.py)
- [Profile guide](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
