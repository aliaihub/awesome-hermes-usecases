# scicco/hermzner: Hardened Hermes on Hetzner + Tailscale

**Class:** Independent first-person deployment · **Confidence:** Medium-High · **Demo status:** Public repo · **Status label:** `nascent` (below 10★ threshold)

## Pain Point

You want Hermes running 24/7 on your own infrastructure, exposed to the open internet through one of the chat platforms Hermes supports (Telegram, Discord, Slack, etc.) — but you don't want to ship a Docker image with `:latest` tags and a public-facing port. A production deployment wants:

- Pinned image digests (no surprise updates)
- Rootless container runtime
- Tailscale-only network (no public ports)
- UFW default-deny
- Read-only root filesystem
- Automated daily backups
- Reproducible provisioning

Hand-rolling all of that on a Hetzner VPS is a weekend of work. `scicco/hermzner` ships a Terraform + Ansible setup that does it in one command.

## What It Does

`scicco/hermzner` provisions a Hetzner `cx23` (Ubuntu 24.04) and configures it with a defense-in-depth posture:

| Layer | What it does |
|---|---|
| **VPS** | Hetzner `cx23` running Ubuntu 24.04 |
| **Container runtime** | Rootless Podman (Quadlet default, Compose fallback) |
| **Network** | Tailscale SSH + subnet access only — no public services |
| **Service** | Nous Research Hermes Agent (gateway, API, optional dashboard) |
| **Memory** | Optional Mnemosyne SQLite-vec backend |
| **Backups** | Daily cron to `/home/hermes/backups/` (plain or `age`-encrypted) |
| **Image pinning** | Digest-pinned `nousresearch/hermes-agent` image; deploy fails closed if the digest is missing |

The deploy script is a one-liner:

```bash
HCLOUD_TOKEN=... TAILSCALE_AUTH_KEY=tskey-auth-... ./deploy.sh
```

Teardown is a one-liner too: `./teardown.sh`.

The repo's `scripts/repo_check.sh` runs local security/consistency checks (secret leakage, dangerous container flags, image-pinning enforcement, syntax) so a contributor can verify a PR doesn't regress the security posture.

**Use case:** an operator running Hermes on real infrastructure who wants the security baseline done correctly the first time.

## Setup

1. Clone the repo and configure the Terraform variables:
   ```bash
   git clone https://github.com/scicco/hermzner.git
   cd hermzner
   cp terraform/terraform.tfvars.example terraform/terraform.tfvars
   vim terraform/terraform.tfvars
   ```
2. Resolve a pinned digest for `nousresearch/hermes-agent:main`:
   ```bash
   curl -s "https://hub.docker.com/v2/repositories/nousresearch/hermes-agent/tags/main" \
     | jq -r '.images[] | select(.architecture == "amd64" and .os == "linux") | .digest'
   ```
3. Set `hermes_image_ref` in `ansible/inventory/group_vars/all.yml` to the digest.
4. Deploy:
   ```bash
   HCLOUD_TOKEN=... TAILSCALE_AUTH_KEY=tskey-auth-... ./deploy.sh
   ```
5. SSH in over Tailscale and confirm:
   ```bash
   ssh hermes@<tailscale-ip>
   systemctl --user status hermes-gateway
   ```

## Prompts

Not a prompt-driven use case — `hermzner` is infrastructure-as-code. Once deployed, the agent on the box behaves like any other Hermes install: Telegram/Discord gateway, cron jobs, skills, memory. The hardening is at the host level, not the agent level.

## Skills Needed

- Hetzner Cloud account + `HCLOUD_TOKEN`
- Tailscale account + `TAILSCALE_AUTH_KEY`
- Local tools: `terraform`, `ansible`, `jq`, `curl`
- Optional: `age` key for encrypted backups

## Notes

- **`cx23` is a small box.** €4.51/month at Hetzner's published rate. Hermes Agent on rootless Podman fits; heavy browser-automation workloads (Playwright, Browser Harness) want `cx33` or larger. The repo doesn't enforce a minimum.
- **Tailscale is the only network surface.** The UFW default-deny rule and `127.0.0.1`-bound ports mean even a misconfigured Hermes gateway isn't reachable from the public internet. The trade-off: Tailscale must stay up. If your Tailscale account goes away, the box becomes unreachable.
- **Image digest pinning is fail-closed.** If you set a tag instead of a digest, the deploy script refuses to run. This is intentional — it's the difference between "Hermes just shipped a bug" and "Hermes didn't update at all."
- **`scripts/repo_check.sh` is part of the contract.** A PR that weakens any of the security checks should be rejected; that's how the repo maintains the posture.
- **3★ at writing — use the `nascent` path.** The repo is below the catalog's 10★ threshold. Per `docs/verification-criteria.md` line 30, the `nascent` PR label or `nascent` in the PR title lets it through. The repo's own README + `repo_check.sh` constitute first-person evidence per the contributing guidelines.
- **Distinct from `hermes-on-flyio.md`** (managed IaaS, less control), **`headless-daemon-server.md`** (systemd + bare metal, no IaC, no hardening), and **`hermes-browser-harness-hostinger.md`** (10-minute copy-paste, no hardening). This is the "I want it done right" end of the spectrum.

## Sources

- **Primary:** `scicco/hermzner` — GitHub repo, MIT license, sole maintainer (`scicco`), created May 18 2026, last push May 24 2026. 3★, 3 forks at time of writing — below the 10★ threshold; promoted under the `nascent` exception.
  <https://github.com/scicco/hermzner>
- **Referenced official install:** Hermes Agent `install.sh`.
  <https://github.com/NousResearch/hermes-agent/blob/main/scripts/install.sh>

## Related Use Cases

- [Hermes on Fly.io](hermes-on-flyio.md) — managed infrastructure alternative (less control, no IaC)
- [Headless Daemon Server](headless-daemon-server.md) — systemd + bare metal (no IaC, no Tailscale)
- [Hermes + Browser Harness on Hostinger](hermes-browser-harness-hostinger.md) — fast 10-minute copy-paste alternative (no hardening)
