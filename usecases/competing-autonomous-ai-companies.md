# Competing Autonomous AI Companies

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Runnable hackathon demonstration

## Pain Point

Multi-agent demonstrations often show activity but provide little evidence about whether agents completed work, learned reusable techniques, or benefited from another team's discoveries. It is difficult to compare organizational strategies under the same task and starting conditions.

## What It Does

Gladiator creates two autonomous Paperclip companies with different strategies and identical starter repositories. Nine Hermes workers execute ten tasks while a dashboard records task progress, Git commits, skill versions, memory growth, session continuity, and an audit trail.

After the competition, a merge phase transfers skills between the teams and records cross-agent use. This makes the project useful as an orchestration and learning demonstration, not as evidence that its synthetic GitHub-star score predicts real product adoption.

## Setup

The full demo requires Python 3.11+, Node.js 20+, pnpm 9+, PostgreSQL 16+, Hermes, Paperclip, and an Anthropic API key. After configuring the Hermes Paperclip adapter:

```bash
git clone https://github.com/runtimenoteslabs/gladiator.git
cd gladiator
cp .env.example .env
# add the documented credentials and Paperclip connection values
```

Start Paperclip, the dashboard, and its watcher using the repository's setup guide, then open `/landing` and select **LAUNCH DEMO**. The demo initializes fresh repositories, wakes the workers, runs the timed competition, and enables the post-result skill-transfer merge.

## Prompts

Gladiator's work prompts are predefined Paperclip issues rather than a single interactive prompt. The source documents the adapter invoking Hermes as:

```text
hermes chat -q "<Paperclip task prompt>" -Q
```

Use the supplied task set so both companies receive the same work and the comparison remains meaningful.

## Skills Needed

- Hermes Agent and `hermes-paperclip-adapter`
- Paperclip with PostgreSQL
- Python, Node.js, and pnpm
- Anthropic model access for the documented configuration
- Gladiator dashboard, watcher, and SQLite evidence database

## Notes

- The repository estimates roughly $5–6 in API cost for a complete run. Set provider budgets before launching repeated experiments.
- The documented adapter version includes local patch notes; check whether newer releases have fixed them before modifying dependencies.
- Treat the projected-star formula as a game score. Validate software quality with tests and human review before merging generated work.

## Sources

- Gladiator repository: <https://github.com/runtimenoteslabs/gladiator>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>
- Paperclip repository: <https://github.com/paperclipai/paperclip>

