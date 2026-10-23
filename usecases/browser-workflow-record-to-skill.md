# Browser Demonstration → Reusable Hermes Skill

<!-- catalog-summary:start -->
[← Browse use cases](../README.md#orchestration--agent-memory) · **Orchestration & Agent Memory**

| At a glance | Details |
| --- | --- |
| **Outcome** | A recorded browser demonstration converted into a replayable Hermes skill. |
| **Requires** | workflow-record Labs plugin; Chromium CDP access; replay skill and /learn. |
| **Available** | Plugin |
| **Validation** | Sources linked below; workflow not run during this catalog redesign. |
<!-- catalog-summary:end -->

**Class:** Official companion (unsupported Labs plugin) · **Confidence:** Medium-High · **Demo status:** Public plugin + runbook; not executed for this catalog update

## Pain Point

A recurring browser task is easier to demonstrate than to describe as a long list of selectors, fields, and navigation steps.

## What It Does

`workflow-record` attaches to a Chromium-family browser over CDP, records the active tab's clicks, changed input values, Enter presses, and navigation, and saves a profile-local JSON file. A bundled skill guides `/learn` in converting that demonstration into a procedure using Hermes' browser tools. The recording is input to learning, not a guarantee of a robust replay.

## Setup

```bash
hermes plugins install workflow-record
```

Connect a Chromium-family browser through Hermes' `/browser connect`, or configure an existing CDP endpoint. Keep the workflow's starting tab in front, then run:

```bash
hermes record --slug shop-login
```

Perform the demonstration, then press Ctrl-C. The CLI prints the recording path and the next learning command. Recordings live under the active Hermes profile's `recordings` directory.

## Prompts

The upstream example is:

```text
/learn the browser workflow recorded in /home/me/.hermes/recordings/shop-login-20261021-120000.json (follow the workflow-record:replay-recording skill)
```

Use the exact path printed by your recording command. The generated skill should treat recorded labels as data, use selectors as hints, and resolve secret placeholders through the documented secret mechanism at replay time.

## Skills Needed

- `workflow-record` plugin
- Bundled `workflow-record:replay-recording` skill and `/learn`
- Chromium-family browser with CDP access
- Hermes browser tools for replay

## Notes

- Nous built this plugin but explicitly does not support or maintain it; the catalog lists it in the community tier.
- Capture covers one tab. Popups, uploads, scrolling, drag-and-drop, and several other interaction types are not recorded.
- Password-like fields are masked. Secrets entered into ordinary text fields or URLs can still appear in the JSON; inspect a recording before sharing it.
- Unlike the [browser harness](hermes-browser-harness-hostinger.md), this workflow learns a procedure from a human demonstration.

## Sources

- Source and complete capture limitations: <https://github.com/NousResearch/hermes-labs-plugins/tree/main/workflow-record>
- Official catalog, including unsupported status: <https://hermes-agent.nousresearch.com/docs/plugins/workflow-record>
