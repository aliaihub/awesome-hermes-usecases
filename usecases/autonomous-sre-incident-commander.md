# Autonomous SRE Incident Commander

**Class:** Independent deployment · **Confidence:** High · **Demo status:** Runnable demo + tested watchdog

## Pain Point

During an infrastructure incident, an on-call engineer must collect signals, determine severity, correlate logs, choose a safe response, confirm recovery, and write a post-incident report. Delays and incomplete handoffs increase mean time to recovery.

## What It Does

Hermes Incident Commander implements a `DETECT → TRIAGE → DIAGNOSE → REMEDIATE → VERIFY → DOCUMENT → LEARN` loop for Linux, Docker, and Kubernetes environments. It uses Hermes memory for topology and incident history, cron for health checks, gateway channels for alerts, subagents for parallel service investigation, and skill creation for prevention playbooks.

The repository also includes a standalone watchdog, adaptive time-of-day thresholds, local SQLite/FTS incident search, Prometheus metrics, PagerDuty resolution, dry-run mode, and allowlisted remediation.

## Setup

Clone the repository, install Hermes, and copy the skill:

```bash
git clone https://github.com/Lethe044/hermes-incident-commander.git
cd hermes-incident-commander

curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
hermes gateway setup

cp -r skills/incident-commander ~/.hermes/skills/
```

Run the included simulated incident before pointing anything at a real host:

```bash
pip install anthropic rich
python demo/demo_incident.py --scenario disk-full-logs
```

For the standalone watchdog, preview every proposed action first:

```bash
pip install -e .
python -m monitor.watchdog --dry-run
```

## Prompts

The repository documents this Hermes scheduling prompt:

```text
Set up incident monitoring: run a health check every 5 minutes and alert me
on Telegram if anything is P0 or P1. Send me a daily briefing at 08:00.
```

## Skills Needed

- `incident-commander` skill
- Terminal access to the monitored Linux, Docker, or Kubernetes environment
- Hermes cron and a configured alert gateway
- Optional PagerDuty, Prometheus/Grafana, or cloud-provider MCP integrations

## Notes

- Start in the included demo or `--dry-run` mode. Real infrastructure access changes this from an educational workflow into a high-impact operator.
- The standalone watchdog's auto-remediation is opt-in and allowlisted. Preserve that boundary instead of granting unrestricted shell repair.
- The repository distinguishes safe actions, warned actions, and destructive actions that require explicit approval.

## Sources

- Incident Commander repository: <https://github.com/Lethe044/hermes-incident-commander>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

