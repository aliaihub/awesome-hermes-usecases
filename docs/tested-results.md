# Tested results

This page records execution evidence for the starter kits and cookbook. A source link, star count, dry run, successful model-list request, and complete workflow run are different kinds of evidence.

## Current results

Review date: **2026-10-24 (America/Denver)**. Local checks ran on Linux x86_64, Python 3.12.14, and Bash 5.2.21. The reference Hermes version is **v0.22.5**, commit [`bf0203a`](https://github.com/NousResearch/hermes-agent/commit/bf0203a794a07aac3ff764972ab9087baa4e4f4e). A full Hermes installation, Docker daemon, model credentials, and Telegram bot were unavailable in the test environment.

| Starter | Executed checks | Result | Live execution |
| --- | --- | --- | --- |
| [Daily briefing](../demos/daily-briefing/) | Redacted dry run; fixture CLI verifies profile targeting, paused creation, explicit Telegram destination, and missing-input failures | Offline pass | Model/search, scheduler execution, output quality, and delivery: **not run** |
| [Team Telegram](../demos/team-telegram/) | Fixture CLI/Docker checks setup ordering, allowlist validation, current config keys, backend drift, and secret-safe failures | Offline pass | Telegram authentication, authorized/unauthorized messages, and Docker shell execution: **not run** |
| [Open WebUI](../demos/openwebui/) | Fixture CLI configuration; real local HTTP test server checks model-list success, auth/server errors, malformed/empty data, and rejected redirects | Offline pass | Actual Hermes API, image startup, container networking, browser UI, and model response: **not run** |

The suite currently has **22 tests**. Fake `hermes` and `docker` executables are test fixtures, not evidence those programs ran. The HTTP fixture uses a temporary loopback server and a dummy key; it never calls a model. The cookbook's watchdog and receipt validator also have deterministic offline tests.

Separately, **14 cron argument examples** were accepted by the pinned upstream parser's native argument-building functions. The hook-flag registrar is supplied locally; this checks grammar, not the full CLI, scheduler, hooks, or runtime validation. The complete source hash is checked before those functions are loaded.

The [CI workflow](../.github/workflows/practical-check.yml) repeats offline checks on Python 3.11 and 3.12, verifies the pinned cron grammar, and runs the real `docker compose config --quiet` parser without launching containers. Consult the [workflow runs](https://github.com/aliaihub/awesome-hermes-usecases/actions/workflows/practical-check.yml) for its recorded outcomes.

No live model latency, API cost, or integration success rate was measured. Empty cost/latency results are not zero-cost performance claims. Open WebUI v0.12.3 is an explicitly pinned reference image; its live compatibility is pending.

## Reproduce offline checks

From the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/check-practical.py
python scripts/render-catalog.py --check
python recipes/examples/validate_receipt.py recipes/examples/receipt.expected.json
git diff --check
```

The first two commands need Python 3.11+ and Bash. They do not need Hermes, Docker, model credentials, or Telegram. The test HTTP server binds only to loopback.

To repeat the upstream grammar check, download the reviewed file, then run the hash-guarded harness:

```bash
curl --fail --silent --show-error --location \
  https://raw.githubusercontent.com/NousResearch/hermes-agent/bf0203a794a07aac3ff764972ab9087baa4e4f4e/hermes_cli/subcommands/cron.py \
  -o /tmp/hermes-cron-v0.22.5.py
python scripts/check-upstream-cron.py /tmp/hermes-cron-v0.22.5.py
```

With Docker Compose installed, validate its configuration using a dummy key and no container startup:

```bash
API_SERVER_KEY=offline-compose-fixture-key-1234567890 \
  docker compose --env-file demos/openwebui/.env.example \
  -f demos/openwebui/docker-compose.yml config --quiet
```

This dummy key is for configuration validation only. Generate a real local credential when deploying.

## Recording a live test

Submit a small record with the fields below and supporting sanitized output. Keep fixture and live results separate, and keep failures alongside successes. A model-list or health check alone cannot receive an end-to-end pass.

| Field | Record |
| --- | --- |
| Workflow and repository revision | Starter/recipe and the commit tested |
| Date and environment | Date/timezone, OS, Docker/Compose where applicable |
| Hermes version | Exact version and commit if available |
| Provider and model | Exact configured provider/model; no credentials |
| Input and commands | Reproducible sample plus commands/steps used |
| Expected versus observed | Sanitized output and every relevant stage's outcome |
| Timing and cost | Measured values and measurement method, or unmeasured |
| Limits and failures | Unsupported platforms, skipped steps, errors, cleanup |

For briefing: verify research quality, completed execution, and delivery. For Telegram: verify account authorization and actual Docker-backed tool execution. For Open WebUI: verify a browser response through the real container and Hermes profile.

## Primary references

- [Hermes v0.22.5 cron parser](https://github.com/NousResearch/hermes-agent/blob/bf0203a794a07aac3ff764972ab9087baa4e4f4e/hermes_cli/subcommands/cron.py)
- [Hermes environment-key routing](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/hermes_cli/config_env_routing.py)
- [Hermes Open WebUI reference](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/website/docs/user-guide/messaging/open-webui.md)
- [Open WebUI v0.12.3 startup bindings](https://github.com/open-webui/open-webui/blob/v0.12.3/backend/start.sh)
