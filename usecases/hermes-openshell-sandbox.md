# Sandboxed Hermes with NVIDIA OpenShell

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Runnable multi-architecture image

## Pain Point

Hermes can use terminals, files, browsers, messaging gateways, and autonomous schedules. Running that tool surface directly on a workstation or server gives prompt injection and faulty automation a large blast radius, while restrictions implemented inside the agent can be bypassed by a compromised process.

## What It Does

HermesClaw packages Hermes inside NVIDIA OpenShell. Policy is enforced outside the agent process:

- OPA and an HTTP CONNECT proxy restrict network destinations.
- Landlock limits filesystem access to approved locations.
- Seccomp blocks high-risk syscalls.
- The inference privacy router keeps backend credentials outside the sandbox.

Persistent memory, skills, cron, delegation, MCP, IDE integration, and messaging remain available according to the selected policy profile.

## Setup

Install the prebuilt multi-architecture package:

```bash
curl -fsSL https://raw.githubusercontent.com/TheAiSingularity/hermesclaw/main/scripts/install.sh | bash
```

Install OpenShell, start a local model endpoint, and launch the strict policy:

```bash
curl -fsSL https://www.nvidia.com/openshell.sh | bash

cd ~/.hermesclaw
llama-server -m models/your-model.gguf --port 8080 --ctx-size 32768 -ngl 99 &
hermesclaw start
hermesclaw chat "hello"
hermesclaw doctor
```

Messaging requires a wider policy, for example `hermesclaw start --gpu --policy gateway`.

## Prompts

The sandbox does not require special task phrasing. The repository demonstrates normal Hermes use through:

```bash
hermesclaw chat "hello"
```

Use `hermesclaw doctor` and the included use-case tests to verify policy behavior before assigning sensitive work.

## Skills Needed

- Docker, Git, and curl
- NVIDIA OpenShell account/install
- A supported inference backend such as local `llama-server`
- A selected OpenShell policy appropriate to the required Hermes tools

## Notes

- Start with the strict profile and widen only the destinations, paths, or capabilities a workflow needs.
- The gateway and permissive profiles intentionally expose more capability than the default policy.
- Hardware- or kernel-enforced isolation reduces risk; it does not make unreviewed destructive tasks safe.

## Sources

- HermesClaw repository: <https://github.com/TheAiSingularity/hermesclaw>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>
- NVIDIA OpenShell documentation: <https://docs.nvidia.com/openshell/about/overview>
