# Enterprise Cloud Deployment (Bedrock / Azure AI Foundry / NVIDIA Build)

**Class:** Official integration · **Confidence:** High · **Demo status:** Config patterns

## Pain Point

Your shop standardized on a hyperscaler — AWS, Azure, or NVIDIA — for compliance, procurement, or existing-spend reasons. "Just point Hermes at OpenRouter" isn't an option: data residency, IAM integration, and private-network egress all have to flow through your cloud account. You need Hermes to speak to the models you already have contracted access to, inside the perimeter.

## What It Does

Hermes's providers documentation ships first-class support for the three major enterprise model gateways. Same agent, same skills/memory/cron surface — only the model backend changes. Each is a configured provider with its own auth chain, so Hermes slots into existing credential infrastructure instead of carrying a new API key.

- **AWS Bedrock** (`bedrock`) — uses boto3's standard credential chain (env vars, `~/.aws/credentials` profile, EC2/ECS IAM role, IMDS, SSO). Speaks the Bedrock Converse API, so Claude, Nova, DeepSeek, and Llama models all work. Optional Bedrock Guardrails attach via `guardrail.guardrail_identifier`.
- **Azure AI Foundry** (`azure-foundry`) — `hermes model` wizard path, authenticates with an Azure OpenAI / Foundry endpoint and key.
- **NVIDIA Build / NIM** (`nvidia`) — cloud endpoint at `build.nvidia.com` with `NVIDIA_API_KEY`, or a self-hosted NIM by pointing `NVIDIA_BASE_URL` at your NIM's `/v1` endpoint. Hermes auto-attaches the NIM billing-origin header on every cloud request.

## Setup

### AWS Bedrock

```bash
# credentials via any boto3-supported method, e.g.:
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...        # if using a session role
```

```yaml
# ~/.hermes/config.yaml
model:
  provider: "bedrock"
  default: "us.anthropic.claude-sonnet-4-6"
bedrock:
  region: "us-east-1"
  # guardrail:
  #   guardrail_identifier: "gr-abc123"
  #   guardrail_version: "1"
```

### Azure AI Foundry

```bash
hermes model          # → "Azure AI Foundry" → paste endpoint + key
```

### NVIDIA Build / NIM

```bash
# ~/.hermes/.env
NVIDIA_API_KEY=nvapi-...
# optional self-hosted NIM:
# NVIDIA_BASE_URL=<your-nim-host>/v1
```

```yaml
# ~/.hermes/config.yaml
model:
  provider: "nvidia"
  default: "nvidia/llama-3.3-nemotron-super-49b"
```

## Skills Needed

- An account and model access on Bedrock, Azure AI Foundry, or NVIDIA Build (the model-grant step on the cloud side is the slow part)
- For Bedrock: boto3 credentials reachable by the standard chain
- For NVIDIA NIM self-hosting: a GPU box running the NIM container

## Notes

- **Bedrock Converse API normalizes the model surface** — you get one config shape across Anthropic, Amazon, DeepSeek, and Meta models on Bedrock, instead of per-vendor quirks.
- **Guardrails are opt-in.** If your compliance team requires them, set the guardrail block; otherwise Hermes behaves like any other provider.
- **NVIDIA NIM self-hosted vs Build cloud** are the same provider ID with a different base URL — useful for moving a workload from cloud eval to on-prem without changing agent config.
- Context-window limits still apply and vary per Bedrock/Azure model; set `context_length` in config if Hermes's default probe gets it wrong.

## Sources

- AI Providers docs (rendered, enterprise section): <https://hermes-agent.nousresearch.com/docs/integrations/providers/>
- Source-of-truth markdown: <https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md>