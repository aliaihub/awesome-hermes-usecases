# Box Hub → Cited Customer-Renewal Brief

**Class:** Official integration · **Confidence:** High · **Demo status:** Docs + runbook with fictional sample data

## Pain Point

Account teams need a meeting brief drawn from contracts, support escalations, success plans, and approved pricing, with citations they can check.

## What It Does

Box's developer tutorial uses Hermes' bundled `box` skill and Box AI for Hubs to analyze eight fictional customer documents. Hermes verifies the connected user and Hub, prepares a cited renewal brief, then saves reviewed work as a Box Note and checks its Hub membership. Source files stay in Box for the analysis.

## Setup

1. Install or update [Hermes Agent](https://github.com/NousResearch/hermes-agent) and confirm the bundled `box` skill is available.
2. Connect the intended Box account through the skill's OAuth setup. The skill distinguishes a local browser from a remote/headless host.
3. Use the tutorial's sample documents to create the account folder and Customer 360 Hub.
4. Confirm the account can access the Hub and files and that Box AI for Hubs is enabled and indexing is complete.

The bundled skill's actor check is:

```bash
box users:get me --json --fields id,name,login
```

Use the verified CLI runner from the skill if `box` is installed under the Hermes home rather than on `PATH`.

## Prompts

The tutorial's actual briefing request begins:

```text
Use Box AI with the "Northstar Customer 360" Hub to prepare me for tomorrow's renewal meeting.
```

Use the complete request in the source tutorial for its output fields and citation requirements, then the separate request to save and verify the approved Box Note.

## Skills Needed

- Bundled `box` skill and official Box CLI
- Box OAuth account with access to the selected content
- Box Hubs and Box AI for Hubs availability, permissions, and AI units

## Notes

- This is a vendor-authored demo using fabricated data, not evidence of a live customer deployment.
- The skill verifies writes and keeps access bounded by the connected account.
- This differs from [Nextcloud](nextcloud-workspace-assistant.md): its defining output is a cited, cross-document account brief through Box AI.

## Sources

- Official Box walkthrough: <https://blog.box.com/creating-company-brain-box-and-hermes-agent>
- Bundled skill and setup references: <https://github.com/NousResearch/hermes-agent/tree/main/skills/productivity/box>
