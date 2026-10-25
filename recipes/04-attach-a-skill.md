# Attach a skill to a scheduled job

## Goal

Reuse an installed workflow without copying its entire definition into every scheduled prompt.

## Requires

A configured `recipe-demo` profile, a skill installed in that profile, and its dependencies. The skill must work without interactive questions.

## Steps

```bash
hermes --profile recipe-demo skills list
```

Choose the exact installed skill name, then replace `INSTALLED_SKILL`:

```bash
hermes --profile recipe-demo cron create "every 1d" \
  "Use the attached skill to produce today's report. State missing inputs explicitly." \
  --skill INSTALLED_SKILL --name "Skill-based report" --deliver local --paused
```

Repeat `--skill` when more than one is needed. Read the skill's setup instructions before scheduling it; merely attaching a skill does not provision credentials or external tools.

## Expected result

A paused job with the selected skill attached. A live run loads that skill for the scheduled task.

## Failure check

If the skill is missing, confirm `skills list` in the **same profile**. Plugin-namespaced skills and installed profile skills have different discovery behavior; follow that plugin's instructions rather than assuming every name is interchangeable.

## Sources

- [Working with skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
- [Cron skill arguments](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/subcommands/cron.py)
