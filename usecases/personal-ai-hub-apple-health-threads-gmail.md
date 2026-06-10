# Personal AI Hub: Apple Health + Threads + Gmail + Calendar

**Class:** Independent first-person deployment · **Confidence:** Medium-High · **Demo status:** Public blog + open-source skill

## Pain Point

A solo operator has data scattered across Apple Health (sleep, steps), Threads (social analytics), Gmail (inbox), and Google Calendar (schedule). Each lives in its own silo with its own native app. The operator wants *one* interface — a Telegram chat with Hermes — that can pull from any of them on demand, cross-reference (e.g., "what was my sleep on days I had a 7am meeting?"), and run as a daily morning brief.

## What It Does

A desktop Hermes Agent connects to four external services via a mix of native APIs, browser cookies, and Hermes skills. The operator drives everything from Telegram, using **Telegram Topics** to keep workflows visually separate:

| Topic | Workflow |
|---|---|
| **Health** | Apple Health → sleep/steps ingest → morning brief with average sleep vs. yesterday |
| **Social Media** | Threads analytics via browser-cookie auth → top posts of the week |
| **App Development** | Code generation + project management flows |
| **Analytics** | Cross-domain queries ("what was my sleep on days I shipped a release?") |

The Hermes session holds persistent context (`SOUL.md`, `AGENTS.md`, `User.md`) and shares an Obsidian vault with the operator's other tools, so knowledge accumulated in one topic is available in the others.

The deployable artifact is `krumjahn/threads-growth-skill` on GitHub — an open-source Hermes skill that pulls Threads analytics into the agent. Other skills in the workflow are documented in the blog but not all are open-sourced.

**Use case:** a solo founder or technical operator who wants a single chat surface to query personal data across multiple services, with a long-running agent that accumulates knowledge over time.

## Setup

1. Install Hermes Agent on the operator's main machine (the blog uses macOS; Linux/Windows work the same with platform-appropriate substitutions).
2. Configure Telegram as the primary gateway and enable Topics:
   ```bash
   hermes gateway setup
   # pick Telegram, paste bot token, set chat ID with Topics enabled
   ```
3. Wire each service:

   - **Apple Health:** Export Health data to a local file (Health Auto Export app, or a custom iOS Shortcut), point Hermes at the export path. The blog's "Health Data AI Analyzer" pattern reads the JSON and persists it as a daily skill.
   - **Threads:** Install `krumjahn/threads-growth-skill` from GitHub. Auth is via exported browser cookies (Cookie-Editor extension) — no API key needed.
     ```bash
     git clone https://github.com/krumjahn/threads-growth-skill.git
     cp -r threads-growth-skill ~/.hermes/skills/threads-growth-skill
     hermes skills reload
     ```
   - **Gmail + Google Calendar:** Create an OAuth app in Google Cloud Console with Gmail API and Calendar API enabled. Drop the credentials JSON into `~/.hermes/integrations/google/`.
4. Add a daily morning cron that pulls sleep + calendar + inbox + Threads into one brief:
   ```
   /cron add "0 7 * * *" "Every morning at 7am: read my sleep data from
   ~/.hermes/data/health/last-7-days.json, my calendar for the next 24h,
   my unread Gmail (inbox-only, max 20), and my Threads analytics for the
   past 7 days. Compose a 5-bullet morning brief: sleep, schedule, top 3
   emails, top Threads post, and a one-line suggestion for the day.
   Post to my Telegram health topic."
   ```
5. Set up the shared knowledge base. The blog uses an Obsidian vault at `~/ObsidianVault/`, and Hermes reads/writes notes there directly.

## Prompts

The ad-hoc queries that drive the workflow:

```
# Health
"Show me my average sleep this week vs. last week, and call out any
night under 6 hours."

# Social
"Pull my top 3 Threads posts from the last 7 days by impressions,
with their first 50 characters of copy."

# Cross-domain
"On days I shipped a release in the last 30 days, what was my average
sleep the night before?"

# Inbox
"Show me unread inbox messages from senders I've replied to before
and that arrived after 6pm yesterday."
```

The cross-domain query is the killer feature — it requires Hermes to know about both Health data and release history, which the shared Obsidian vault enables.

## Skills Needed

- `krumjahn/threads-growth-skill` (open-source, deployable)
- Apple Health export pipeline (Health Auto Export app on iOS)
- Google Cloud OAuth (Gmail + Calendar)
- Telegram gateway with Topics
- Obsidian vault (optional, for shared knowledge base)
- An LLM provider — the blog uses OpenAI Codex ($20/mo), OpenRouter (free tier), or local Ollama

## Notes

- **Browser-cookie auth for Threads** is the path that works today; the Threads API is restricted. The cookie approach is in the same gray area as other browser-cookie integrations — fine for personal use, fragile if Meta changes the export format.
- **Telegram Topics as a workflow router** is a pattern in itself — instead of separate bots per workflow, one bot with Topics keeps all memory in one place while separating visual contexts.
- **Cross-domain queries** only work if the agent has been writing to a shared knowledge layer (Obsidian, or a structured memory skill). The setup is only as durable as the write-through to that layer.
- **Cost.** The blog uses OpenAI Codex ($20/mo) or OpenRouter's free tier; both are sufficient for the morning brief workload.
- **Distinct from `hermes-ios-native-engine.md`.** That entry is an iPhone companion app with native hardware access. This entry is desktop Hermes + cross-service integration via a single Telegram interface.

## Sources

- **Primary:** Keith Rumjahn, "Complete guide to mastering Hermes Agent" — Substack, Apr 27 2026. Documents the full Apple Health / Threads / Gmail / Calendar / Telegram Topics setup.
  <https://rumjahn.substack.com/p/complete-guide-to-mastering-hermes>
- **Deployable skill:** `krumjahn/threads-growth-skill` — open-source Hermes skill for Threads analytics.
  <https://github.com/krumjahn/threads-growth-skill>
- **Companion video:** "Master Hermes Agent in 41 mins" — Frontier Models, with timestamps covering each integration.
  <https://frontiermodels.cc/video/master-hermes-agent-in-41-mins/>

## Related Use Cases

- [Hermes iOS Native Engine](hermes-ios-native-engine.md) — iPhone companion with native hardware access (different surface)
- [Obsidian Vault as a Second Brain](obsidian-second-brain.md) — the shared knowledge layer that enables cross-domain queries
- [Daily Briefing Bot](daily-briefing-bot.md) — topic-briefing pattern, web search instead of personal services
