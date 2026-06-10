# Inbox → Slack Daily Digest

**Class:** First-party pattern · **Confidence:** High · **Demo status:** Documented cron recipe

## Pain Point

You check your inbox first thing in the morning and spend 30 minutes triaging before you can start work. You already use Slack for team chat. You want Hermes to read the inbox, summarize what's actually new, and drop the summary into a Slack channel at 9am — so you read one message instead of fifty.

## What It Does

A Hermes cron job wakes at 9am on weekdays, connects to Gmail or Outlook via OAuth, classifies the inbox into "needs reply / FYI / spam," drafts a short summary, and posts it to a Slack channel via the messaging gateway. Hermes does not auto-reply; it produces a digest and surfaces what should be human-signed-off.

The pattern is documented by Anthony Maio in his Substack setup guide as the canonical example of a natural-language cron prompt that runs against personal infrastructure. Slack is one of ~20 surfaces Hermes's gateway supports (Telegram, Discord, WhatsApp, Signal, Matrix, Mattermost, SMS, Email, etc.) — this is the Slack variant.

**Use case:** any solo operator or small team that wants a daily inbox digest in their team channel without writing a custom IMAP poller.

## Setup

1. Install Hermes and start the gateway so cron runs unattended:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
   hermes setup
   hermes gateway install
   ```
2. Configure Slack as a messaging surface during `hermes gateway setup`. You'll need a Slack app with `chat:write` scope and the bot token in `SLACK_BOT_TOKEN`.
3. Connect Gmail or Outlook — Hermes supports both via the standard OAuth flow documented in `hermes-agent.nousresearch.com/docs/integrations/email`.
4. Add the cron job. The natural-language prompt is the actual recipe:

```
/cron add "0 9 * * 1-5" "Every weekday at 9am, summarize my inbox. Classify each new message as
needs-reply / fyi / spam. Draft a one-line summary for each needs-reply item and a bullet
list of fyi items. Post to #morning-digest in Slack. Do not auto-reply to anything."
```

The `[SILENT]` token in the final response suppresses the post on days when the inbox is empty.

## Prompts

Single-cron version (above). The author documents the pattern as: *"a natural-language cron pattern that the agent runs unattended on its own schedule."*

The pattern is independent of email provider — swap "Gmail" for "Outlook" in the prompt, and the OAuth setup is the only config that changes.

## Skills Needed

- Cron scheduler (built into Hermes)
- Email integration (Gmail API or Microsoft Graph)
- Slack gateway (or any of: Telegram, Discord, Teams, etc.)
- An LLM provider (OpenRouter, OpenAI, or local via Ollama)

## Notes

- **Don't auto-reply.** The pattern's value is *triage*, not sending. If you want auto-replies, add a separate explicit cron that requires human approval before sending.
- **Slack channel choice.** Post to a low-traffic channel (`#morning-digest`, `#bot-output`) so the digest is easy to scan without flooding `#general`.
- **Timezone.** `0 9 * * 1-5` runs at 9am in the gateway's local timezone. If your VPS is in a different region, set the gateway's TZ or adjust the cron expression.
- **Not the same as `daily-briefing-bot.md`.** That one uses web search for topic briefings; this one reads the *inbox* and posts to Slack specifically. They can run side-by-side.

## Sources

- **Primary:** Anthony Maio, "Getting Started with Hermes Agent" — Substack, Mar 30 2026. Documents the "summarize my inbox and post to Slack" pattern as the canonical natural-language cron example.
  <https://anthonymaio.substack.com/p/getting-started-with-hermes-agent>
- **Official cron reference:** Hermes Agent docs — <https://hermes-agent.nousresearch.com/docs/guides/automate-with-cron>
- **Gateway / Slack setup:** Hermes Agent docs — <https://hermes-agent.nousresearch.com/docs/user-guide/messaging>

## Related Use Cases

- [Daily Briefing Bot](daily-briefing-bot.md) — web-search topic briefing, distinct cron pattern
- [Team Telegram Assistant](team-telegram-assistant.md) — same gateway pattern on a different surface
- [Zero-Token Notifications](zero-token-notifications.md) — cron pre-filtering to cut LLM token spend
