# Dynamic Skill Dojo

**Class:** Self-improvement workflow · **Confidence:** High · **Demo status:** Public Hermes skill repository

## Pain Point

Hermes can evolve skills, but operators still need to know which skills are
failing, where the agent repeats mistakes, and what should be optimized first.
Without a measurement loop, self-evolution becomes a manual experiment rather
than an overnight improvement cycle.

## What It Does

Hermes Dojo monitors agent sessions, identifies weak skills and missing
workflows, runs targeted fixes, and reports whether the agent is improving over
time. It closes the loop between observability and self-evolution:

```text
measure -> identify weakness -> evolve -> measure again -> report
```

Core pieces:

- Performance monitor reads Hermes session state and tracks failures.
- Weakness analyzer ranks recurring problems and missing skills.
- Auto-fixer patches weak skills, creates new skills from repeated patterns, or
  invokes the GEPA self-evolution path where appropriate.
- Reporter generates CLI or Telegram summaries.
- Learning curve tracker stores historical metrics across days and weeks.

## Setup

Install as a Hermes skill:

```bash
git clone https://github.com/Yonkoo11/hermes-dojo.git
cd hermes-dojo
./install.sh
```

Run the demo pipeline:

```bash
cd ~/.hermes/skills/hermes-dojo/scripts
python3 seed_demo_data.py --days 7
python3 demo.py --reset
```

Common commands:

```text
/dojo analyze
/dojo improve
/dojo report
/dojo history
/dojo auto
```

## Prompts

Analyze recent failures:

```text
Use Hermes Dojo to analyze the last week of sessions. Rank the top three skill
weaknesses and show evidence before proposing fixes.
```

Overnight improvement:

```text
Set up a Dojo auto run that analyzes failures, proposes skill patches, and
delivers a report. Do not apply patches without creating a reviewable diff.
```

## Skills Needed

- Hermes Dojo skill
- Hermes session state
- Optional: Hermes self-evolution repository for GEPA optimization
- Optional: Hermes cron and Telegram delivery

## Notes

- This is distinct from the existing Self-Evolution use case. Self-Evolution is
  the optimizer; Dojo is the monitoring and prioritization loop around it.
- Treat automatic skill patches as proposed changes. Review diffs before
  trusting them in production workflows.
- Dojo is a good fit for long-lived Hermes installations with enough session
  history to expose recurring patterns.

## Sources

- Hermes Dojo repository: <https://github.com/Yonkoo11/hermes-dojo>
- Hermes self-evolution companion repository: <https://github.com/NousResearch/hermes-agent-self-evolution>
