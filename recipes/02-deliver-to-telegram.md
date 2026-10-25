# Deliver to a specific Telegram chat

## Goal

Make a scheduled result's destination explicit instead of relying on a default home channel.

## Requires

A configured `recipe-demo` Telegram gateway, bot access to the target chat, and the numeric chat ID. The sender allowlist controls who can invoke the bot; it is not the delivery destination.

## Steps

Replace the example numeric ID with your destination:

```bash
hermes --profile recipe-demo cron create "0 17 * * 1-5" \
  "Summarize the approved project notes into five bullets. Return the summary as the final response; do not send messages yourself." \
  --name "Team notes digest" --deliver "telegram:-1001234567890" --paused
```

Use a positive chat ID for a DM or the appropriate negative group/channel ID. Put the actual project path or attached skill into the prompt before running; scheduled jobs do not inherit your interactive conversation.

## Expected result

A paused job with a `telegram:CHAT_ID` destination. After a successful live run, the scheduler delivers the final response to that chat.

## Failure check

A completed agent run does not prove delivery. Check run history and the destination chat; verify the bot can send there and review the profile's Telegram settings.

## Sources

- [Telegram configuration](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)
- [Cron delivery](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron)
