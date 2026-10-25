# Diagnose a missing scheduled result

## Goal

Distinguish a missing job, inactive scheduler, failed execution, and failed delivery.

## Requires

The correct Hermes profile and a job ID from its cron list.

## Steps

```bash
hermes --profile recipe-demo cron list
hermes --profile recipe-demo cron status
hermes --profile recipe-demo cron doctor
hermes --profile recipe-demo cron runs JOB_ID
hermes --profile recipe-demo logs
```

Work through the evidence in order:

1. Does the job exist, and is it paused/completed rather than active?
2. Does the intended profile have a live scheduler? Is its clock/timezone correct?
3. Does the execution history show a failed model, skill, script, or tool step?
4. Did the run complete but delivery fail? Check the explicit target and destination permissions.

## Expected result

A diagnosis tied to the failing layer, rather than repeated blind reruns. These commands inspect state; this recipe does not queue another model request.

## Failure check

An empty run history does not prove success. Confirm the profile and job ID. When sharing logs in an issue, redact credentials and customer content first.

## Sources

- [Cron troubleshooting](https://hermes-agent.nousresearch.com/docs/guides/cron-troubleshooting)
- [v0.22.5 cron diagnostics CLI](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/subcommands/cron.py)
