# Headless Daemon Server

**Class:** Deployment pattern · **Confidence:** High · **Demo status:** Public deployment guide

## Pain Point

Many Hermes workflows need to keep running after an SSH session closes:
scheduled jobs, gateway integrations, long-lived team bots, and unattended
automation. A shell loop or tmux session is fragile. Operators need a simple,
reboot-safe Linux deployment using the native Hermes gateway and scheduler.

## What It Does

`hermes-autonomous-server` documents a dedicated Linux server deployment for
Hermes using a non-root service user, Nous Portal authentication, native Hermes
cron jobs, and a `systemd` service for `hermes gateway`.

The pattern covers:

- Dedicated `hermes` user.
- Install and login flow for Hermes Agent.
- Creating recurring Hermes cron jobs from a chat session.
- Running the gateway as a system-level service.
- Reboot safety and automatic restart.
- `journalctl` and Hermes cron diagnostics.
- Cost and billing considerations for scheduled runs.

## Setup

Create a service user and install Hermes:

```bash
sudo adduser hermes
sudo usermod -aG sudo hermes
su - hermes
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes login
```

Create cron jobs from Hermes, then install a `systemd` unit similar to:

```ini
[Unit]
Description=Hermes Gateway Service
After=network.target

[Service]
User=hermes
WorkingDirectory=/home/hermes
ExecStart=/home/hermes/.local/bin/hermes gateway
Restart=always
RestartSec=10
Environment=PATH=/home/hermes/.local/bin:/usr/local/bin:/usr/bin:/bin

[Install]
WantedBy=multi-user.target
```

Enable and verify:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hermes-gateway
sudo systemctl start hermes-gateway
hermes cron status
```

## Prompts

Create a scheduled job:

```text
Create a cron job that runs every weekday at 8:00 AM. It should summarize the
top operational alerts from local files and write the result to
~/reports/morning-ops.md.
```

Diagnose daemon health:

```text
Check Hermes cron status, gateway status, and the latest systemd logs. Summarize
whether scheduled jobs can fire after reboot.
```

## Skills Needed

- Linux VPS or dedicated server with `systemd`
- Hermes Agent and Nous Portal login
- Native Hermes cron and gateway
- Basic Linux service administration

## Notes

- This complements the existing Fly.io deployment entry. Fly.io is managed
  infrastructure; this pattern is for a self-managed Linux server.
- Avoid running Hermes as root. Use a dedicated service account and firewall the
  host appropriately.
- Monitor model/API usage when jobs run frequently.

## Sources

- Headless server guide repository: <https://github.com/JackTheGit/hermes-autonomous-server>
