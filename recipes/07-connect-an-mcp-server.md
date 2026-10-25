# Connect a catalog MCP server

## Goal

Add an external capability through Hermes's documented MCP catalog.

## Requires

A configured `recipe-demo` profile, network access, and any dependencies/authentication required by the chosen catalog entry.

## Steps

```bash
hermes --profile recipe-demo mcp catalog
```

Review the entry and its exposed tools. The official guide uses DeepWiki as a public-repository research example:

```bash
hermes --profile recipe-demo mcp install deepwiki
hermes --profile recipe-demo chat
```

In the new chat, request:

```text
Use the DeepWiki capability to explain the top-level structure of NousResearch/hermes-agent. Cite the repository material used. If the server is unavailable, say so.
```

## Expected result

The selected MCP integration is configured. A successful live request can use its tools; installation success alone does not prove the remote service or model works.

## Failure check

Restart the chat or gateway after changing MCP configuration. For another server, check its own authentication, tool selection, and startup instructions; do not substitute arbitrary package names into this example.

## Sources

- [MCP integration and catalog](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp)
- [v0.22.5 MCP guide](https://github.com/NousResearch/hermes-agent/blob/v0.22.5/website/docs/user-guide/features/mcp.md)
