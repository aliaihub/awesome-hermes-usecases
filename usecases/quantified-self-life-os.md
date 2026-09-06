# Quantified-Self Life OS

**Class:** Independent deployment · **Confidence:** High · **Demo status:** Runnable package + Docker demo

## Pain Point

Personal tracking apps split sleep, mood, exercise, nutrition, habits, and goals into separate databases. They record isolated events but rarely connect them into a useful, longitudinal picture or deliver timely reflections without manual analysis.

## What It Does

Hermes Life OS stores structured observations across mood, energy, sleep, hydration, meals, workouts, stress, focus, habits, goals, spending, and other user-chosen dimensions. It combines Hermes memory and scheduled briefings with a local correlation engine that only surfaces relationships after enough overlapping data exists.

The workflow supports onboarding, morning briefings, midday check-ins, evening reflections, weekly reviews, chat, data import, and optional Atropos training. It can run against Ollama or supported hosted providers and can deliver through Hermes gateways.

## Setup

Install the package and choose a backend:

```bash
pip install "hermes-life-os[all]"

# Fully local option
ollama serve
ollama pull llama3.1

hermes-life-os --mode onboard
hermes-life-os --mode morning
hermes-life-os --mode chat
```

Or run the published container with a persistent Hermes data volume:

```bash
docker run --rm -it \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -v hermes-life-os-data:/root/.hermes \
  ghcr.io/lethe044/hermes-life-os:latest --mode morning
```

## Prompts

The repository documents these on-demand analysis prompts:

```text
What patterns have you noticed in my data?
```

```text
What predicts my mood?
```

## Skills Needed

- `hermes-life-os` package or container
- Persistent Hermes memory volume
- Ollama or a supported hosted model provider
- Optional gateway, cron schedule, data imports, and Atropos environment

## Notes

- Correlation is not causation. Treat detected relationships as hypotheses to examine, not medical findings.
- This is a wellness and reflection workflow, not a diagnostic system. Medication, mental-health, or symptom decisions should remain with qualified professionals.
- Decide which categories are appropriate to store before onboarding; health and financial logs are sensitive data.

## Sources

- Hermes Life OS repository: <https://github.com/Lethe044/hermes-life-os>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

