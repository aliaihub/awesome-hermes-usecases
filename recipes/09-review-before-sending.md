# Review a draft before sending

## Goal

Keep a person's review between generated content and an external send/publish action.

## Requires

A fresh drafting profile, a local output folder, and a person who sends the approved result through their normal application. Do not configure mail/social sending credentials or authenticated sending integrations in this drafting profile.

## Steps

Give Hermes a drafting task such as:

```text
Using the approved notes I provide, write a customer follow-up draft to drafts/follow-up.md. Mark assumptions and missing facts. Do not send, publish, or claim approval. End by telling me where the draft is saved.
```

Open the file yourself, verify facts and recipients, and make corrections. Send through your own mail client only after that review. This recipe intentionally has no automated send command.

## Expected result

A local draft and a separate human sending step. A prompt saying "ask first" alone is not an enforced tool permission boundary; keep sending credentials and capabilities out of this fresh profile.

## Failure check

Review the profile's tools, plugins, MCP integrations, browser sessions, and accessible host resources. If the agent can already send through them, this draft-only pattern is not isolated as described; use a dedicated environment before handling real customer data.

## Sources

- [Profiles and shared resources](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Reviewed Box workflow](../usecases/box-renewal-copilot.md)
