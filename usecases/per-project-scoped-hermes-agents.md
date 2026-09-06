# Per-Project Scoped Hermes Agents with Ankh.md

**Class:** Ecosystem integration · **Confidence:** Medium · **Demo status:** Runnable prototype

## Pain Point

One global agent profile can mix memories, instructions, tools, and skills from unrelated codebases. Developers need project-specific agents that automatically adopt the right identity and context when invoked inside a repository.

## What It Does

Ankh.md patches the local Hermes launcher so a valid `.agent/` directory creates a scoped Hermes instance for that folder. Each project can keep its own:

- `config.yaml` overrides merged over the global Hermes baseline.
- Skills and tool selection.
- Sessions, memories, identity, prompt, and instructions.
- Shareable agent configuration committed alongside the project, with private memories ignored when necessary.

Outside an Ankh folder, the ordinary global Hermes Agent continues to run.

## Setup

The documented prototype has been tested on macOS and requires Bun, Git, Hermes, and Python 3.11+:

```bash
git clone --branch divine https://github.com/Abruptive/Ankh.md.git
cd Ankh.md
bun bootstrap
```

The bootstrap installs the extension under `~/.agent/extensions/ankh`. If needed, add its wrapper to the shell path:

```bash
export PATH="$HOME/.agent/extensions/ankh/bin:$PATH"
ankh setup
```

Run `hermes` in the repository root or one of the included example folders to activate that folder's `.agent/` profile.

## Prompts

The repository contrasts global and scoped memory with this example:

```text
What did we work on yesterday in this project?
```

The scoped agent should answer from that project's local identity, sessions, and memory without asking which project the user means.

## Skills Needed

- Hermes Agent and Python 3.11+
- Bun and Git
- Project-local `.agent/config.yaml`, `.agent/agent.jsonc`, and optional `.agent/skills/`

## Notes

- Gateway, cron, and scoped authentication are explicitly work in progress and unlikely to work in the current release.
- The installer uses a patched Hermes copy rather than changing the user's original installation. That still creates maintenance risk when upstream Hermes changes.
- Commit shareable configuration deliberately; keep private memories and credentials ignored.

## Sources

- Ankh.md repository: <https://github.com/Abruptive/Ankh.md>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

