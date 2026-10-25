# Run a job inside a project

## Goal

Give a scheduled job an explicit working directory and project instructions.

## Requires

A configured `recipe-demo` profile, an existing local repository, and permission to read that project.

## Steps

Run this while inside the intended project:

```bash
hermes --profile recipe-demo cron create "0 16 * * 1-5" \
  "Read this project's instructions and summarize outstanding TODOs. Produce a local report; make no code changes." \
  --workdir "$(pwd)" --name "Project TODO review" --deliver local --paused
```

Review the project's `AGENTS.md` and other agent instruction files before running. `--workdir` selects context and working directory; it is not a filesystem sandbox, and a read-only prompt is not an enforced permission policy.

## Expected result

A paused job with an absolute project path. The documented project instruction files are available when the task runs.

## Failure check

If creation rejects the path, confirm it is an absolute, existing directory on the **gateway host**, not just on your laptop.

## Sources

- [Cron project-directory behavior](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
- [v0.22.5 workdir argument](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/subcommands/cron.py)
