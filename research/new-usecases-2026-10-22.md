# Catalog additions — October 22, 2026

Five priority workflows selected from the research shortlist, compared with the 77 entries at base commit `c4fc049`. These additions bring the catalog to 82. “New” means missing from this collection, not a claim that every underlying capability was first released this month.

| Entry | Primary evidence | Evidence boundaries |
| --- | --- | --- |
| [SEO audits and content briefs](../usecases/seo-audits-content-briefs.md) | `yuzushi-dev/hermes-seo` README and manifest; official community catalog | Native community port. The README pins a v0.1.0 install while the inspected source manifest says v0.1.2. Google OAuth flows are disabled; upstream Claude SEO demo results are not Hermes deployment results. |
| [REA analysis and crash triage](../usecases/rea-reverse-engineering.md) | Official plugin README, crash-triage skill, and catalog | Format-dependent engines are user-provided. Pseudocode and inferred names are analysis evidence, not original source. |
| [Browser demonstration to skill](../usecases/browser-workflow-record-to-skill.md) | Official Labs plugin README, manifest, and catalog | Unsupported Labs status is explicit. Single-tab capture and secret-masking limits are carried into the entry. |
| [NetBox inventory](../usecases/netbox-network-inventory.md) | First-person implementation article dated October 13 | Case study with private skill configuration. Provides an adaptation outline, not a public installer. |
| [External MCP conversation bridge](../usecases/hermes-mcp-conversation-bridge.md) | Official `mcp-serve` README and catalog | Conversation bridge plus an optional tool allowlist. It does not expose a general shell or the entire agent loop. |

## Backlog promotion

The official MCP Serve implementation supplies the missing primary evidence for two overlapping candidates:

- **Hermes as MCP server**
- **MCP backend for Claude Desktop / Cursor**

Both are represented by the single conversation-bridge entry and removed from the unverified table. The current command is `hermes mcp-serve`; the old core spelling was `hermes mcp serve`.

## Verification scope

All five entries passed `scripts/verify-usecase.py --check all --ci`, each with a green result. The committed reports record the source-availability and repository-engagement signals checked by the script; their numeric scores do not measure integration correctness or maturity.

The index, badge, and 82 non-report use-case files agree. Required sections, Markdown fence balance, local links, and `git diff --check` passed.

These checks establish source availability and catalog consistency. They do not establish successful operation of the integrations. No plugins, customer systems, provider APIs, browser recordings, network scans, or binary-analysis engines were run for this documentation update.
