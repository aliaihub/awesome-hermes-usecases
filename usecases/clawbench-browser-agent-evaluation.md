# ClawBench Browser-Agent Evaluation

**Class:** Ecosystem integration · **Confidence:** High · **Demo status:** Runnable

## Pain Point

You want to evaluate whether Hermes can complete real browser tasks, not just whether it can call a toy tool. Doing that safely requires isolated browsers, realistic task definitions, side-effect interception, scoring, and enough evidence to diagnose failures.

## What It Does

ClawBench runs each task in an isolated container with an instrumented Chromium browser. Selecting `--harness hermes` installs Hermes in the harness image, attaches its native browser tools to that Chromium instance over CDP, and passes the chosen task instruction to `hermes chat`.

The same browser is observed by ClawBench's recorder and request interceptor. Each run produces a session video, action screenshots, HTTP traffic, browser actions, and Hermes messages. Critical matching requests are blocked and saved for evaluation instead of reaching the live service.

ClawBench includes three useful evaluation scales: the 20-task V1 Lite subset for smoke tests, 153 V1 tasks, and 130 V2 tasks across live websites.

## Setup

Prerequisites are Python 3.11+, `uv`, and Docker or Podman.

```bash
git clone https://github.com/TIGER-AI-Lab/ClawBench.git
cd ClawBench
cp models/models.example.yaml models/models.yaml
```

Add a model endpoint and API key to `models/models.yaml`, then use that entry's name in the commands below.

Run one task without the optional LLM judge:

```bash
uv run clawbench-run \
  test-cases/v1-lite/142-office-secretary-tasks-collab-trello \
  <model-name> \
  --harness hermes \
  --no-judge
```

Run the 20-task Lite suite:

```bash
uv run clawbench-batch \
  --models <model-name> \
  --cases-suite v1-lite \
  --all-cases \
  --max-concurrent 1 \
  --harness hermes \
  --no-judge
```

Remove `--no-judge` after configuring the judge entry documented in `models/models.example.yaml`.

## Prompts

No separate Hermes prompt is required. ClawBench uses the selected task's public `instruction` field as the base Hermes query. For the single-task command above, that instruction is:

```text
Create a Trello board "Q3 Sprint Planning" with 3 lists + 5 cards
```

The Hermes harness adds only its completion guidance and, when needed, a note with the task's disposable webmail credentials.

## Skills Needed

- Python 3.11+ and `uv`
- Docker or Podman
- An API endpoint supported by ClawBench's model configuration
- No separate Hermes installation; the harness image installs its pinned Hermes version

## Notes

- The first run builds the Chromium and Hermes container image; later runs reuse it.
- Results land under `test-output/<model>/` with the five trace layers plus interception and run metadata.
- `--no-judge` reports interception-only results. Configure the documented judge model for payload-aware Stage 2 scoring.
- These are live websites, so layouts, availability, bot defenses, and alternate flows can change between runs.

## Sources

- Primary source and setup: <https://github.com/TIGER-AI-Lab/ClawBench>
- Hermes harness implementation: <https://github.com/TIGER-AI-Lab/ClawBench/tree/main/src/clawbench/runtime/harnesses/hermes>
- Project page: <https://claw-bench.com/>
- Paper: <https://arxiv.org/abs/2604.08523>
