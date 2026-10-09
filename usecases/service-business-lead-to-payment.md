# Service-Business Lead → Estimate → Payment

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Public reference skills + case study

## Pain Point

A service-business owner has to move every inquiry through qualification, pricing, a customer email, payment collection, and CRM updates. Re-entering the same job details at each step wastes time.

## What It Does

`hewi333/Mom-n-Pop-Skills` documents a Hermes workflow developed while operating a real service business through Telegram. A `lead-to-payment` skill coordinates a SQLite CRM, a rate-card estimator, Himalaya email, and Stripe. The owner reviews the estimate and customer email before execution; payment status returns to the CRM and Telegram.

The public skill is more specific than the README's broad claims: **Stripe uses test mode, and QuickBooks is not wired in this reference flow.** Treat accounting reconciliation as an optional extension, not an already-working part of the demo.

## Setup

With Hermes already installed, use the default profile:

```bash
git clone https://github.com/hewi333/Mom-n-Pop-Skills.git
mkdir -p ~/.hermes/skills
cp -r Mom-n-Pop-Skills/skills/* ~/.hermes/skills/
```

Customize the estimator's rate card and business details. Configure Himalaya for the actual email provider and Stripe with a test-mode key. The source includes provider-specific email and website-intake references; copying skills alone does not provision these integrations.

## Prompts

The published intake example is an owner pasting a referral lead into Telegram:

```text
new lead: Jane Doe, 2,400 sqft home in [CITY], cigarette smoke, referral from [Referral Partner].
```

Follow the upstream demo: review the summary, authorize pricing, review the estimate, approve the test payment link, and check the resulting payment status. Do not reuse its illustrative dollar amounts as your own rate card.

## Skills Needed

- `lead-to-payment`, `crm-lite`, `estimator-engine`, and `stripe-payments`
- Himalaya CLI with IMAP/SMTP configured
- Hermes Telegram gateway
- Optional `grasshopper-voicemail-monitor` for inbound lead polling

## Notes

- Public implementations are sanitized references, not a turnkey product.
- Keep the separate approvals for an estimate, payment action, and customer email.
- This differs from [ERPClaw](erpclaw-plain-english-erp.md): the core workflow is service-job intake and owner-approved quoting, rather than a general ERP.

## Sources

- First-person repository: <https://github.com/hewi333/Mom-n-Pop-Skills>
- Current implementation and integration limits: <https://github.com/hewi333/Mom-n-Pop-Skills/blob/main/skills/lead-to-payment/SKILL.md>
- Hermes skills installation format: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>
