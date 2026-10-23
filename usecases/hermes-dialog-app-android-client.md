# Hermes Dialog App — Native Android Client

**Class:** Ecosystem integration
**Confidence:** High
**Demo status:** Runnable

## Pain Point

Hermes runs great from the CLI, a web dashboard, or a chat platform — but most people carry a phone, not a terminal. The existing Android entries in this space are *device-control* bridges (let Hermes drive a phone). There was no native Android **chat client** that talks to your own gateway and survives the things that actually break mobile clients: dropped SSE connections, the app being killed mid-run, and turns started from another surface.

## What It Does

A self-hosted Android client (Kotlin + Jetpack Compose) that connects to the Hermes `api_server` platform. Pure client-side project — no server code required.

Ingress → core → delivery:

- **Chat** — `POST /v1/runs` to start a turn, `GET /v1/runs/{id}/events` for SSE streaming, `Last-Event-ID` backlog replay on reconnect.
- **Multi-profile** — switch between two bots (e.g. `default` / `friend`); each has its own API key, session list, and local storage. `/p/<profile>/...` routing and per-profile bearer keys.
- **Media both ways** — upload images via `/v1/artifacts/upload` (`artifact_id` into the run's `images` array); render server-sent `MEDIA:` content as images or file cards.
- **Voice** — server-side TTS completion playback, plus per-message voice replay fetched by `run_id`.
- **Scheduled jobs** — a page wired to `/api/jobs` (list / pause / resume / run now), with server-side English identifiers translated to the user's language.
- **Live usage** — token counts (input / cache read / cache write / output), elapsed time, tok/s per turn; sub-task progress rows and a collapsed tool-call trace.
- **Human-in-the-loop** — approval and clarify cards driven by `approval.request` / `clarify.request`, with a background notification when the turn is waiting on you.
- **Updates** — in-app check against `version.json`, download with progress, MD5 verify, hand off to the system installer.

## Setup

```bash
# 1. Clone
git clone https://github.com/shang1626/hermes-dialog-app.git
cd hermes-dialog-app

# 2. Configure — no secrets live in the source; they are injected at build time.
cat > local.properties <<'PROPS'
sdk.dir=/your/android/sdk
HERMES_APP_PASSWORD=your-app-login-password
HERMES_DEFAULT_KEY=your-default-profile-api-key
HERMES_FRIEND_KEY=your-friend-profile-api-key
HERMES_DEFAULT_URL=https://your-gateway.example.com
HERMES_UPDATE_URL=https://your-update-host.example.com/update/version.json
# optional: old-host=new-host migration
HERMES_LEGACY_HOSTS=old.example.com=new.example.com
PROPS

# 3. Build (no gradle wrapper in the repo — use your installed gradle or build.sh)
./build.sh

# 4. Install
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Gateway side:

```bash
curl http://127.0.0.1:8642/health          # confirm api_server is up
# create/read the per-profile bearer key the app expects
```

Expose `8642` through a reverse proxy or tunnel with HTTPS if you want to reach it from outside your LAN — do **not** expose `api_server` directly.

## Prompts

Not prompt-driven — this is a client. The relevant "config" is the endpoint contract it speaks:

| Method | Path | Purpose |
|---|---|---|
| POST | `/v1/runs` | start a turn (`input` / `session_id?` / `images?`) → `run_id` |
| GET | `/v1/runs/{id}` | run status + result (recovery after app restart) |
| GET | `/v1/runs/{id}/events` | SSE stream with `Last-Event-ID` resume |
| POST | `/v1/runs/{id}/stop` | abort |
| POST | `/v1/runs/{id}/steer` | mid-run steering |
| POST | `/v1/artifacts/upload` | upload an image, get `artifact_id` |
| GET | `/api/sessions` | session list incl. `active_run` (adopt turns started elsewhere) |
| GET | `/api/jobs` | scheduled jobs |
| GET | `/health` `/health/sysinfo` | liveness + status page |

## Skills Needed

- Hermes gateway with the built-in `api_server` platform enabled.
- Android build toolchain: JDK 17+, Android SDK platform 34 + build-tools 34.0.0, Gradle 8.9.
- Optional server patches to receive non-image attachments (the `_resolve_media_to_data_urls` extension noted in the repo's README).

## Notes

- **No secrets in the repo.** Everything is injected via `local.properties` → `BuildConfig`; the published tree contains no keys, domains, or internal IPs.
- **Signing:** releases sign with the debug keystore by default. Building on a different machine generates a different debug keystore and the APK will fail to install over an existing one (signature conflict) — carry the same `~/.android/debug.keystore`.
- **The parts that are easy to get wrong and are handled here:** SSE reconnect with backlog replay; re-attaching a run after the app process is killed; adopting a run that another surface (CLI / web / chat) started, via `active_run` on the session list; and a queue/mutex model so two turns' TTS never play over each other.
- **CS-side voice and text both come from the same `run`** — the client does not do its own inference.

## Sources

- Repo: https://github.com/shang1626/hermes-dialog-app (public, MIT)
- In-repo docs: `docs/DESIGN.md`, `docs/INTERNALS.md` (run lifecycle, SSE event table, storage format), `docs/BUILD.md`, `docs/CHANGELOG.md`
