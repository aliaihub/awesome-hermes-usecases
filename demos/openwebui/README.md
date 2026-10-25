# Open WebUI starter

Run a local browser interface connected to a Hermes profile. This is the Linux reference setup for the [Open WebUI use case](../../usecases/open-webui-frontend.md).

## Requires

- Linux with Docker Engine and Docker Compose, Bash, and Python 3.11+.
- Hermes compatible with v0.22.5 and a dedicated profile with a configured model.
- Available host ports 8642 (Hermes) and 3000 (Open WebUI).

The Compose file uses **host networking** so the container can reach a Hermes API bound to `127.0.0.1`. Both services bind to loopback. The previous bridge-network example could not reach a loopback-only host service on Linux. Docker Desktop on macOS/Windows needs separately enabled host-network support; that path has not been tested here. See upstream for other networking choices.

## Setup

From this directory:

```bash
hermes profile create webui-demo
hermes --profile webui-demo setup
cp .env.example .env
openssl rand -hex 32
```

Save the generated value as `API_SERVER_KEY` in `.env`. This is a local Hermes server credential, not a model-provider key. Existing users should rename this kit's old `HERMES_API_KEY` setting to `API_SERVER_KEY`.

```bash
bash setup.sh --dry-run
bash setup.sh
```

Setup validates the key and Docker daemon, then sets the current Hermes `API_SERVER_*` settings in the selected profile. Secrets are redacted from the preview and captured CLI output is not printed. No gateway or containers are started.

Start Hermes in another terminal:

```bash
hermes --profile webui-demo gateway
```

Check configuration and the authenticated model-list endpoint, then launch the UI:

```bash
bash smoke.sh --probe
docker compose --env-file .env config --quiet
docker compose --env-file .env up -d
```

Open `http://127.0.0.1:3000`, complete the first-run account setup, and select the Hermes model. The image is pinned to `ghcr.io/open-webui/open-webui:v0.12.3`; that container version has not been runtime-tested in this milestone.

The scripts read `.env` beside themselves or accept `--env-file /absolute/path/to/settings.env`. Keep using the same file when running Compose.

## Sample input and expected output

In a new browser chat, send:

```text
Reply with exactly PONG. Do not call any tools.
```

Expected final text: `PONG`. This is an acceptance target, not a captured response. The request uses the configured Hermes model and can incur charges. Tools execute on the Hermes API host, and all users of this connection share that profile's capabilities.

## Checks and troubleshooting

- `smoke.sh` checks Docker, the Compose configuration, and selected Hermes settings. It starts no containers.
- `smoke.sh --probe` additionally performs an authenticated read-only `/v1/models` request. It rejects HTTP errors, redirects, malformed JSON, and empty model lists. It does not submit a completion or prove the UI can reach Hermes.
- A 401 means the configured server key and the kit's key do not match. Restart the gateway after changes.
- No browser model: inspect the Open WebUI connection URL (`http://127.0.0.1:8642/v1`) and its saved credential in **Admin Settings → Connections**.
- Open WebUI persists connection settings in its database after first launch. Editing environment variables alone may not replace an existing saved connection; update it in the admin UI.

The live acceptance check is a browser response through the actual container and Hermes profile. Record its versions and evidence in [tested results](../../docs/tested-results.md#recording-a-live-test). That full path has not been run here.

## Stop

```bash
docker compose --env-file .env down
```

The named volume remains, preserving accounts and settings. Stop the foreground Hermes gateway separately with Ctrl+C. Removing the volume deletes its data.

## Sources

- [Hermes Open WebUI guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/open-webui)
- [v0.22.5 integration reference](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/website/docs/user-guide/messaging/open-webui.md)
- [Open WebUI v0.12.3](https://github.com/open-webui/open-webui/releases/tag/v0.12.3)
- [Open WebUI connection documentation](https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/)
