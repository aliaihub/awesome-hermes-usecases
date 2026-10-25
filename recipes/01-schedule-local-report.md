# Schedule a local report

## Goal

Create a recurring report you can inspect before enabling automatic runs.

## Requires

A configured `recipe-demo` profile, model/search access, and a gateway for execution.

## Steps

```bash
hermes --profile recipe-demo cron create "0 9 * * 1-5" \
  "Research developer-tool releases from the past day. Return up to three items with publication dates, original URLs, and one practical implication each. Report search failures honestly." \
  --name "Developer release brief" --deliver local --paused
hermes --profile recipe-demo cron list
```

Check the profile's timezone before enabling the job. Inspect the ID, run one manual acceptance check, then resume that ID when ready. The [briefing starter](../demos/daily-briefing/) provides the full sequence.

## Expected result

One paused weekday job. No model request or report is produced by creation alone. Completed run output is stored under the profile's `cron/output/` directory.

## Failure check

If no run happens after enabling, check `hermes --profile recipe-demo cron status`. Creating a job does not start its gateway.

## Sources

- [Cron reference](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [v0.22.5 cron CLI](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/subcommands/cron.py)
