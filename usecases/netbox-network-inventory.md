# Network Discovery → NetBox Inventory

<!-- catalog-summary:start -->
[← Browse use cases](../README.md#infrastructure--security) · **Infrastructure & Security**

| At a glance | Details |
| --- | --- |
| **Outcome** | A daily discovery-to-inventory workflow with optional Proxmox configuration history. |
| **Requires** | Discovery host and network access; NetBox API; custom skill configuration is private. |
| **Available** | Case study |
| **Validation** | Sources linked below; workflow not run during this catalog redesign. |
<!-- catalog-summary:end -->

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** First-person case study; private skill configuration

## Pain Point

Network and VM inventory drifts as infrastructure changes.

## What It Does

Brandon Lee documents Hermes discovering hosts through a tools VM, updating NetBox IP inventory, and gathering Proxmox configuration and change history. An incremental discovery job refreshes the records daily.

## Setup

The generated skill is private. Isolate Hermes, provide scoped access to a discovery host with `nmap`, and configure a dedicated NetBox API account. Add Proxmox MCP if needed. Review the initial import before incremental scheduling.

## Prompts

The author publishes this job outline:

```text
Schedule: 02:00 UTC daily
Skill: netbox-network-discovery
```

Use your authorized network ranges; no complete task prompt or public skill installer is supplied.

## Skills Needed

- Hermes terminal and scheduling
- Network-discovery access and NetBox API
- Optional Proxmox MCP integration

## Notes

- This is documentation maintenance, distinct from [incident remediation](autonomous-sre-incident-commander.md).
- The report's NetBox token is write-capable; its extra Proxmox role includes `Sys.Modify`. Review permissions before reuse.
- Reported outcomes were not independently reproduced here.

## Sources

- First-person implementation: <https://www.virtualizationhowto.com/2026/10/im-using-my-hermes-ai-agent-to-build-my-home-lab-inventory-in-netbox/>
- Hermes substrate: <https://github.com/NousResearch/hermes-agent>
