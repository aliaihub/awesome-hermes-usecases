# Recipe cookbook

Ten small building blocks to combine with the [use cases](../README.md#find-a-use-case) or [starter kits](../demos/README.md).

| # | Recipe | Result |
| --- | --- | --- |
| 01 | [Schedule a local report](01-schedule-local-report.md) | A paused recurring job with a self-contained prompt |
| 02 | [Deliver to a specific Telegram chat](02-deliver-to-telegram.md) | An explicit delivery destination |
| 03 | [Run a script-only watchdog](03-script-only-watchdog.md) | Threshold alerts without an LLM run |
| 04 | [Attach a skill to a scheduled job](04-attach-a-skill.md) | A reusable workflow loaded for each run |
| 05 | [Run a job inside a project](05-project-working-directory.md) | Explicit project context and working directory |
| 06 | [Create a separate workspace profile](06-separate-workspace-profile.md) | Separate configuration, memory, and session state |
| 07 | [Connect a catalog MCP server](07-connect-an-mcp-server.md) | A documented path to an external capability |
| 08 | [Validate structured output](08-validate-structured-output.md) | A local contract check for extracted receipt data |
| 09 | [Review a draft before sending](09-review-before-sending.md) | A manual approval boundary before publication |
| 10 | [Diagnose a missing scheduled result](10-diagnose-a-scheduled-job.md) | Checks that separate scheduling, execution, and delivery |

The commands were reviewed against Hermes v0.22.5; they have not all been executed against a live Hermes installation. Recipes are documented patterns, not additional verified use cases. Sample data is fictional. See [tested results](../docs/tested-results.md).

Commands assume you created and configured the named profile first. Setup commands change local configuration or create paused jobs; a live `cron run`, resumed schedule, or chat can incur provider charges. `JOB_ID` and `INSTALLED_SKILL` are values you select from your installation, not literal names to paste unchanged.

Each recipe states its prerequisites, expected result, and one useful failure check. Keep provider credentials in Hermes profile configuration; do not put them into prompts or repository files.
