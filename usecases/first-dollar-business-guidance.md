# First-Dollar Business Guidance (Hermes Startup)

**Class:** Independent deployment · **Confidence:** High · **Demo status:** Runnable

## Pain Point

Starting a business online is overwhelmed by generic advice. Most AI agents answer "give me a business idea" with the same tired list — dropshipping, freelance writing, an AI wrapper — that ignores who you are, what you can reach, and what you can actually get paid for. Worse, many tools push you into paid subscriptions before you've validated anything, and they quietly send your personal answers to third parties.

## What It Does

Hermes Startup is a local-first Hermes skill that runs a structured onboarding inside the agent: a short personal profile, then an evidence-labeled opportunity map, then one bounded next action. Ingress is the user's own answers, kept in the local Hermes profile. The output is a ranked shortlist where every idea is labeled (inferred / user-confirmed / confirmed) and explicitly not an income guarantee. A single prepaid balance covers per-call tool spend, with no subscription and no automatic top-up; provider calls and external actions still require the user's explicit approval.

## Setup

1. Install the skill into Hermes:
   ```bash
   hermes skills install https://hermesstartup.com/skill/SKILL.md
   ```
2. Install from source (open-core, MIT): `https://github.com/33hodl/hermes-startup` — see `SKILL.md` and `README.md` there.
3. Ask the agent: "Help me find my first dollar online."

## Prompts

```
Help me find my first dollar online. Ask me what you need to know, then show
me 3 of 10 potential ideas for me specifically, why each fits me, how you
would execute it, its realistic potential, and a timeframe to the first
useful result. Do not assume demand for anything — label every idea as
inferred and unverified.
```

The skill's public contract (in the repo) requires: 3 of 10 ideas framed as a
sample, not "the top three"; every idea labeled inferred with buyer demand
unverified; no income guarantee; explicit approval before any external action;
and outcome labels of confirmed / user-confirmed / inferred / uncertain.

## Skills Needed

- Hermes Agent (any recent version; the skill ships as `startup`)
- Optional: approved read-only X/search surface for creative hypothesis
  sourcing (attributed, never treated as proof)

## Notes

- Privacy-safe by design: answers stay in the local profile; nothing is sent
  to the site or a third party without explicit user action.
- Not a money printer and explicitly not an income guarantee — the skill
  contract requires stating that plainly.
- The product itself publishes an evidence ledger
  (`https://hermesstartup.com/outcomes.json`) that currently states no
  customer testimonials, revenue, or outcome statistics are claimed — the
  tool practices the evidence discipline it teaches.

## Sources

- Primary: public open-core repo `https://github.com/33hodl/hermes-startup`
  (SKILL.md + README with install and contract details)
- Public skill bundle: `https://hermesstartup.com/skill/SKILL.md`
- Public evidence record: `https://hermesstartup.com/outcomes.json`
