# Reverse Engineering and Crash Triage with REA

**Class:** Official integration · **Confidence:** High · **Demo status:** Public plugin + runbook; not executed for this catalog update

## Pain Point

Explaining an unfamiliar program or diagnosing a native crash requires evidence from packages, binaries, captures, and decompiler output. A generic coding chat does not provide those artifacts by itself.

## What It Does

Nous Research's REA plugin connects Hermes to REA's MCP server and bundles its investigation workflow. Hermes can inspect Electron/JavaScript applications, native executables, .NET assemblies, Android packages, firmware, and saved captures, then explain the returned evidence. A companion crash-triage skill reads a Linux core dump and its matching binary to investigate the recorded failure.

## Setup

```bash
hermes plugins install rea
hermes plugins enable rea
```

Start a new Hermes session. The plugin launches a pinned REA package over `npx`; it declares Node.js 22.19+, 24.11+, or 26+ and excludes Node.js 23 and 25.

Static JavaScript, archive, and package inspection need no separate decompiler. Native decompilation needs an installed provider such as Ghidra, Hopper, or IDA. Android code and firmware extraction have their own upstream tool requirements.

For the core-dump tools, the current README requires a user-provisioned Python environment with pwntools 4.15.0, pyelftools 0.33, and Unicorn 2.1.2, exposed through `REA_PWNTOOLS_PYTHON` in the Hermes profile's `.env`. Follow the source recovery guide for other provider environment variables.

## Prompts

Actual examples from the plugin README:

```text
Use REA to inspect /Applications/Notes.app and explain how CSV export works.
```

```text
./parser crashed and left ./core. Why?
```

Replace the example paths with artifacts you have authority to inspect. The crash workflow checks the binary's build ID against the core before placing addresses.

## Skills Needed

- Official `rea` plugin and its MCP server
- Bundled `reverse-engineer-anything` and `crash-triage` skills
- Format-specific analysis engines where required
- The exact crashed binary and core dump for crash triage

## Notes

- REA returns analysis evidence; pseudocode is not the original source code. Label inferred names and types and retain evidence references.
- Large native imports can exceed Hermes' tool deadline. The README describes version-specific budget controls; do not infer readiness merely because `open_binary` succeeded.
- The crash skill reads the artifacts without launching the program.
- This differs from [penetration testing](autonomous-penetration-testing.md): the central task is program behavior and artifact analysis.

## Sources

- Official plugin and requirements: <https://github.com/NousResearch/hermes-official-plugins/tree/main/rea>
- Official catalog entry: <https://hermes-agent.nousresearch.com/docs/plugins/rea>
