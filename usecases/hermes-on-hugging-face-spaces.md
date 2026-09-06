# Persistent Hermes on Hugging Face Spaces

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** One-click Space template + Docker deployment

## Pain Point

An always-available Hermes gateway normally requires a continuously running computer or paid VPS, plus a persistence plan for sessions, skills, memory, and configuration. That is a high setup barrier for experiments and personal messaging bots.

## What It Does

HermesFace packages Hermes as a Docker-based Hugging Face Space with a browser dashboard and messaging gateway. Because a Space's local filesystem can be replaced on restart, it periodically synchronizes `/opt/data` to a private Hugging Face Dataset repository.

The result is a hosted Hermes instance whose conversations, skills, memory, and configuration can survive container restarts. The image passes supported Hermes environment variables through to the agent, so model providers and messaging channels can be configured with Space secrets.

## Setup

1. Duplicate the public HermesFace Space.
2. Create a Hugging Face token with write permission.
3. Add `HF_TOKEN` and one model-provider key under **Settings → Repository secrets**.
4. Set `AUTO_CREATE_DATASET=true`, or create a private Dataset and set `HERMES_DATASET_REPO` explicitly.
5. Update the duplicated Space's `datasets:` metadata so it does not point at the original author's dataset.
6. Open the Space URL and configure messaging through the dashboard or environment variables.

For manual persistence, the documented settings include:

```text
AUTO_CREATE_DATASET=true
SYNC_INTERVAL=60
TZ=UTC
```

## Prompts

HermesFace changes deployment and persistence, not Hermes's prompt model. Use the same tasks you would use locally, then restart the Space and verify that the relevant session, memory, or skill returns from the private Dataset backup.

## Skills Needed

- Hugging Face account, Space, and write-capable token
- Private Dataset repository for persistence
- At least one supported model-provider credential
- Optional Telegram, Discord, Slack, WhatsApp, or another Hermes gateway credential

## Notes

- Hugging Face quotas, sleep behavior, hardware allocations, and pricing can change. Treat free-tier and always-on claims as platform-dependent rather than permanent guarantees.
- Keep the persistence Dataset private. It may contain full conversations, memory, custom skills, and configuration.
- Secrets remain server-side, but the agent still has the network and tool capabilities allowed by the Space container and Hermes configuration.

## Sources

- HermesFace repository: <https://github.com/democra-ai/HermesFace>
- Public Space template: <https://huggingface.co/spaces/tao-shen/HermesFace>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>
