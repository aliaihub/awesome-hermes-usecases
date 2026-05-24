# Autonomous Penetration Testing with Kali

**Class:** Security skill · **Confidence:** High · **Demo status:** Public skill repository with simulated demo

## Pain Point

Security testing requires long, stateful investigation across scanning,
enumeration, exploitation checks, credential analysis, and reporting. A generic
agent can call shell tools, but without a constrained playbook it may skip
authorization checks, run shallow scans, lose evidence, or stop after a clean
first pass.

## What It Does

`kali-pentest` is a penetration testing skill for Hermes and other coding
agents. It connects Hermes to a Kali Linux environment through local shell,
SSH, or Docker, then gives the agent structured playbooks for authorized
security assessment.

The workflow includes:

- Mandatory authorization and scope confirmation.
- Playbook selection for target type and test depth.
- Kali tool selection across hundreds of native CLI tools.
- Zero-findings fallback paths so the agent escalates depth before declaring a
  clean result.
- Evidence capture and structured reporting with reproduction and remediation
  notes.
- Human approval gates for high-risk actions.

## Setup

Install the skill into Hermes:

```bash
git clone https://github.com/x-glacier/kali-pentest.git
cp -r kali-pentest/kali-pentest ~/.hermes/skills/kali-pentest
```

Provide one Kali execution environment:

```text
Local mode: run Hermes on a Kali host.
Server mode: connect to a full Kali machine over SSH.
Docker mode: run a persistent Kali container for CLI-heavy assessments.
```

Then start a Hermes session and invoke the skill with a scoped, authorized
target.

## Prompts

Authorized internal assessment:

```text
Use the kali-pentest skill. I have written authorization to test 10.0.10.25
from this workstation. Confirm scope, choose the safest initial playbook, and
stop before any destructive or credential-changing action.
```

Report-only simulation:

```text
Run the kali-pentest demo path against the bundled mock data and produce the
same report structure I would get after a real assessment.
```

## Skills Needed

- `kali-pentest` Hermes skill
- Kali Linux environment through local shell, SSH, or Docker
- Human approval process for intrusive actions

## Notes

- This use case should be documented with a strict authorized-use warning.
- Do not present it as an autonomous attack tool. The value is repeatable,
  scoped security auditing with evidence and stopping conditions.
- A safe demo path exists, which is useful for catalog verification and user
  onboarding without touching a real target.

## Sources

- Kali Pentest skill repository: <https://github.com/x-glacier/kali-pentest>
- Demo player: <https://x-glacier.github.io/kali-pentest/demo/player.html>
