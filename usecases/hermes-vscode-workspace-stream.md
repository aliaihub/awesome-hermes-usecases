# Hermes VS Code Workspace Stream

**Class:** Community IDE integration · **Confidence:** High · **Demo status:** Public extension repository

## Pain Point

Terminal-first agent sessions are powerful, but coding work often happens inside
an editor. Developers need Hermes context, tool output, file attachments, model
switching, and session continuity without leaving VS Code or manually copying
paths between the editor and the CLI.

## What It Does

`hermes-vscode` runs Hermes through the Agent Client Protocol (ACP) and exposes
the active agent session in a VS Code sidebar. The extension streams chat,
renders tool calls with status, opens edited files in the editor, tracks context
usage, and keeps sessions persistent across reloads.

Key workflow pieces:

- Webview chat panel with streaming markdown and inline media.
- Tool call display for reads, edits, shell commands, fetches, and searches.
- Active file, selection, open tabs, and attached files sent as workspace
  context.
- Session picker for create, switch, rename, and resume.
- Model selector and slash command menu inside VS Code.
- Skills picker that loads from `~/.hermes/skills/`.

## Setup

Install and authenticate Hermes first:

```bash
pip install hermes-agent
hermes setup
```

Install the extension from the public repo or release artifact, then open the
Hermes panel in VS Code. The extension spawns:

```bash
hermes acp
```

from the workspace side of the editor, so Remote SSH workspaces run Hermes on
the remote machine rather than through a hosted proxy.

## Prompts

Use editor context directly:

```text
Review the active file and the selected lines. Suggest the smallest safe patch.
```

Attach a local file from VS Code and ask Hermes to inspect it:

```text
Use the attached config file and the open test file to find why the test suite
is failing.
```

Switch models from the integrated command menu:

```text
/model anthropic:claude-sonnet-4
```

## Skills Needed

- Hermes CLI and ACP support
- VS Code 1.85+
- Optional: project-specific Hermes skills under `~/.hermes/skills/`

## Notes

- The extension does not proxy work through a cloud service. It launches the
  local or remote workspace Hermes binary over stdio.
- This is an IDE interface, not a replacement runtime. Hermes still owns tools,
  session state, skills, and model execution.
- Remote SSH is a strong fit because the extension can run where the code and
  terminal environment already live.

## Sources

- Hermes VS Code repository: <https://github.com/joaompfp/hermes-vscode>
