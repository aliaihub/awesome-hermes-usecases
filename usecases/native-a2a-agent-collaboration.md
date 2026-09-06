# Native A2A Agent Collaboration

**Class:** Official integration · **Confidence:** High · **Demo status:** Docs + runnable protocol endpoint

## Pain Point

Hermes subagents work well inside one process, but they do not solve delegation across machines, security boundaries, or agent frameworks. A desktop agent may need a research specialist on a server, while an external LangChain, CrewAI, or Google ADK agent may need to call Hermes as a service.

## What It Does

Hermes's built-in A2A plugin implements the Linux Foundation Agent2Agent protocol in both directions:

- Outbound tools discover peer Agent Cards, call peers, resume multi-turn conversations, inspect history, and fan work out by advertised capability.
- Inbound HTTP endpoints publish Hermes's Agent Card and accept JSON-RPC tasks, streaming replies, cancellation, status queries, and signed push notifications.
- A task runs inside the normal gateway session, so the called Hermes keeps its own memory, credentials, and enabled tools.

Use A2A when work crosses a process, machine, or framework boundary. For several workers in the same Hermes installation, use native delegation or Kanban instead.

## Setup

Enable the inbound platform with the guided setup:

```bash
hermes gateway setup   # choose A2A
```

Or add it to `~/.hermes/config.yaml` and register a known peer:

```yaml
gateway:
  platforms:
    a2a:
      enabled: true
      extra:
        port: 9900

a2a_agents:
  researcher:
    url: "${RESEARCHER_A2A_URL}"
    auth: { type: bearer, token: "replace-me" }
    timeout: 120
    capabilities: [web_search, research]
```

Enable outbound tools where they are needed, then start the gateway:

```bash
hermes tools enable a2a --platform cli
hermes tools enable a2a --platform a2a
hermes gateway run
```

Set `RESEARCHER_A2A_URL` to the peer's reachable A2A endpoint.

## Prompts

The official documentation uses this request to delegate to the configured peer:

```text
Ask the researcher agent to summarize today's arXiv postings.
```

Its HTTP quick test sends `What tools do you have?` through the A2A `SendMessage` method.

## Skills Needed

- Built-in `a2a` platform and toolset
- A reachable A2A-compliant peer or a second Hermes instance
- Bearer or per-peer tokens for any non-localhost exposure
- Optional reverse proxy or Kubernetes Service with `A2A_PUBLIC_URL`

## Notes

- Without a token the server binds only to `127.0.0.1`; remote exposure requires both authentication and an explicit host binding.
- Hermes filters inbound peer text, blocks remote slash commands, redacts credential-shaped outbound strings, rate-limits callers, and records `~/.hermes/a2a_audit.jsonl`.
- Per-context turn caps prevent two agents from ping-ponging indefinitely.

## Sources

- Official A2A documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/a2a>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>
- Agent2Agent protocol: <https://a2a-protocol.org/>
