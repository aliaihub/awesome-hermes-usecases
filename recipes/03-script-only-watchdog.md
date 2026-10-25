# Run a script-only watchdog

## Goal

Alert on high disk usage without invoking a model for each check.

## Requires

A `recipe-demo` profile and gateway. The example script uses only Python's standard library.

## Steps

From the repository root, copy the script into this profile's scripts directory:

```bash
mkdir -p "$HOME/.hermes/profiles/recipe-demo/scripts"
cp recipes/examples/disk_watchdog.py "$HOME/.hermes/profiles/recipe-demo/scripts/disk_watchdog.py"
python3 "$HOME/.hermes/profiles/recipe-demo/scripts/disk_watchdog.py"
hermes --profile recipe-demo cron create "every 15m" \
  --script "$HOME/.hermes/profiles/recipe-demo/scripts/disk_watchdog.py" \
  --no-agent --deliver local --name "Disk watchdog" --paused
```

The path above assumes the default Hermes root; adjust it when using `HERMES_HOME`. The default alert threshold is 90%. Edit the script's default or use a wrapper if a scheduled job needs a different threshold.

## Expected result

The script emits no stdout below the threshold, and one alert at or above it. `--no-agent` delivers script output directly. The scheduler/gateway must still be running. No model tokens are used by this job; that is not a claim about hosting costs or other scheduled jobs.

## Failure check

Run the script directly with `--threshold 0`; it must reject the invalid threshold with a nonzero exit. Offline tests also exercise silence below the threshold and alerting exactly at the boundary.

## Sources

- [Script-only cron guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [v0.22.5 script/no-agent arguments](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/subcommands/cron.py)
