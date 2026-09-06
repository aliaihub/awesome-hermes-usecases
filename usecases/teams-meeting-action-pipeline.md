# Microsoft Teams Meeting to Action Pipeline

**Class:** Official integration · **Confidence:** High · **Demo status:** Docs + operator runbook

## Pain Point

Meeting recordings and transcripts often remain disconnected from the systems where teams act. Someone still has to find the artifact, summarize it, and copy the result into a channel, project tracker, or knowledge base.

## What It Does

The official Teams meeting pipeline turns Microsoft Graph events into durable Hermes jobs. It:

1. Receives a Graph webhook for an online meeting.
2. Resolves the meeting and prefers an existing transcript.
3. Falls back to downloading the recording and running speech-to-text when necessary.
4. Stores local job and delivery state.
5. Delivers a structured summary to Microsoft Teams, Notion, or Linear.

The pipeline is event-driven rather than a chat-only summarizer, and includes commands for validation, subscription maintenance, retries, and day-two operations.

## Setup

Run `hermes gateway setup` and choose **Teams Meetings**, or enable the plugin and add Microsoft Graph credentials to `~/.hermes/.env`:

```bash
hermes plugins enable teams_pipeline

MSGRAPH_TENANT_ID=<tenant-id>
MSGRAPH_CLIENT_ID=<client-id>
MSGRAPH_CLIENT_SECRET=<client-secret>
MSGRAPH_WEBHOOK_ENABLED=true
MSGRAPH_WEBHOOK_PORT=8646
MSGRAPH_WEBHOOK_CLIENT_STATE=<random-shared-secret>
MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=communications/onlineMeetings
```

Configure Teams delivery and transcript fallback in `~/.hermes/config.yaml`, expose `/msgraph/webhook` over HTTPS, then start and validate:

```bash
hermes gateway run
hermes teams-pipeline validate
hermes teams-pipeline token-health
hermes teams-pipeline subscriptions
```

Subscribe to the transcript resource using the source-documented CLI flow:

```bash
hermes teams-pipeline subscribe \
  --resource communications/onlineMeetings/getAllTranscripts \
  --notification-url "$PUBLIC_MS_GRAPH_WEBHOOK_URL" \
  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"
```

Set `PUBLIC_MS_GRAPH_WEBHOOK_URL` to the public HTTPS URL ending in `/msgraph/webhook`.

## Prompts

No user prompt is required to trigger this workflow: Microsoft Graph webhook events create the jobs. Operators inspect and maintain it with:

```bash
hermes teams-pipeline list
hermes teams-pipeline validate
hermes teams-pipeline maintain-subscriptions
```

## Skills Needed

- Built-in `teams_pipeline` plugin and Microsoft Graph webhook platform
- Microsoft Graph application credentials and required meeting permissions
- Public HTTPS webhook endpoint
- `ffmpeg` when recording-to-STT fallback is enabled
- At least one configured sink: Teams, Notion, or Linear

## Notes

- Microsoft Graph meeting subscriptions expire after 72 hours and do not renew themselves. Schedule `maintain-subscriptions` before production use.
- If the listener binds beyond loopback, restrict accepted source CIDRs to Microsoft's webhook egress ranges.
- Prefer transcripts to recordings: they are faster and avoid unnecessary media processing.

## Sources

- Official Teams Meetings documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams-meetings>
- Official Teams bot documentation: <https://hermes-agent.nousresearch.com/docs/user-guide/messaging/teams>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>
