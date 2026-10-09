# Lead Research → YouTrack Briefs

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Case study

## Pain Point

A small technical agency has a spreadsheet of potential clients but no consistent way to research, prioritize, and prepare for first contact.

## What It Does

Halfbit Studio describes Hermes researching 24 prospects and creating a YouTrack ticket for each. Tickets capture the company profile, a concrete operational problem, a suggested first-contact approach, and a hot/warm/cold assessment. The team packages the process as `lead-research-brief` and supplies company context through `halfbit-advisor`.

This is a human-reviewed research pipeline. The author describes automatic lead intake and scheduled follow-ups as a future direction; the article does not establish that entire loop as deployed.

## Setup

The company-specific skills and YouTrack connector are not published. A reproduction needs:

1. Hermes with web research and persistent company context.
2. The agency's services, relevant work, and prospect criteria.
3. An authenticated YouTrack integration that can create tickets.
4. A reviewed schema for the four fields above.

Follow the official skills guide to package the workflow. This is a reproduction outline, not a runnable copy of Halfbit's private setup.

## Prompts

The article identifies the actual skill as `lead-research-brief`, invoked with a company name. It does not publish the underlying prompt or an exact command; none is invented here.

## Skills Needed

- Web research tools
- Company-context skill
- Lead-research skill
- YouTrack API or MCP integration with suitable project permissions

## Notes

- Treat inferred problems and prospect scores as hypotheses for a person to check.
- The source says humans handle customer contact.
- This adds prospect-specific research and durable CRM tickets beyond the [Daily Briefing Bot](daily-briefing-bot.md).

## Sources

- First-person field report: <https://halfbitstudio.com/en/how-we-run-our-company-with-hermes-agent/>
- Hermes Agent substrate: <https://github.com/NousResearch/hermes-agent>
- Skills format: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>
