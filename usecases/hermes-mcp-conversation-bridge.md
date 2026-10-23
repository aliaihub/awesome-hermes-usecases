# Hermes Conversations and Tools for External MCP Clients

<!-- catalog-summary:start -->
[← Browse use cases](../README.md#interfaces--integrations) · **Interfaces & Integrations**

| At a glance | Details |
| --- | --- |
| **Outcome** | Conversation history, message events, gateway sending, and opt-in tools for MCP clients. |
| **Requires** | mcp-serve plugin; external stdio MCP client; optional gateway and tool-provider configuration. |
| **Available** | Plugin |
| **Validation** | Sources linked below; workflow not run during this catalog redesign. |
<!-- catalog-summary:end -->

**Class:** Official integration · **Confidence:** High · **Demo status:** Public plugin + runbook; not executed for this catalog update

## Pain Point

An agent in Claude Code, Cursor, or another MCP client cannot normally inspect the messaging conversations and provider-backed tools already connected to a Hermes profile.

## What It Does

The official `mcp-serve` plugin exposes Hermes' conversation bridge over stdio: list conversations, read messages and attachments, wait for new events, send messages through the gateway, and interact with exposed approval requests. An opt-in tool set adds web, browser, vision, image generation, skills, and TTS access through the selected profile's configured providers.

This is Hermes serving an MCP client, rather than Hermes consuming a third-party MCP server. It is not an endpoint exposing the entire agent runtime or a general shell.

## Setup

```bash
hermes plugins install mcp-serve
```

Add the upstream example to your client's MCP configuration, using that client's supported configuration format:

```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp-serve"]
    }
  }
}
```

The client must be able to resolve `hermes`. To serve another profile, upstream specifies `args: ["-p", "<profile>", "mcp-serve"]`; install the plugin in that profile too.

Reading history does not require a running gateway. Sending requires the gateway's platform connections. Configure and review the intended profile before connecting a client.

## Prompts

The published invocation modes are:

```bash
hermes mcp-serve
hermes mcp-serve --tools
```

Use the first for the conversation bridge alone. `--tools` enables the selected provider-backed tools; upstream does not publish a mandatory user-task prompt.

## Skills Needed

- Official `mcp-serve` plugin
- An external MCP client with stdio support
- Hermes profile history and optional gateway connections
- Configured provider backends for any opt-in tools

## Notes

- The plugin replaces the former core command `hermes mcp serve`; existing MCP clients need their arguments updated.
- Terminal, file, code execution, process, kanban, and delegation tools are excluded from the exposed allowlist.
- The profile's tool availability and hooks still apply. Conversation and provider access should match the client you connect; paid provider calls keep their normal costs.
- This promotes both overlapping MCP-server candidates from the unverified backlog.

## Sources

- Official implementation and client example: <https://github.com/NousResearch/hermes-official-plugins/tree/main/mcp-serve>
- Official catalog and migration note: <https://hermes-agent.nousresearch.com/docs/plugins/mcp-serve>
