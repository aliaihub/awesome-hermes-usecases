# Mask Sensitive Numbers in Stored Final Replies

<!-- catalog-summary:start -->
[← Browse use cases](../README.md#infrastructure--security) · **Infrastructure & Security**

| At a glance | Details |
| --- | --- |
| **Outcome** | Selected SSN and card-number formats masked in stored final replies. |
| **Requires** | plugin-hook-example; Hermes lifecycle hooks. Raw CLI streaming can precede masking. |
| **Available** | Plugin |
| **Validation** | Sources linked below; workflow not run during this catalog redesign. |
<!-- catalog-summary:end -->

**Class:** First-party demo · **Confidence:** High · **Demo status:** Runnable reference plugin; not executed for this catalog update

## Pain Point

An assistant can repeat a sensitive number into its final reply, persisted transcript, and future conversation context.

## What It Does

Nous Research's `plugin-hook-example` registers a `transform_llm_output` hook. It replaces dashed US Social Security numbers and supported Luhn-valid card-number shapes before final assistant text is stored and delivered. Its logs record match counts rather than the matched values.

## Setup

Install into a current Hermes default profile:

```bash
git clone https://github.com/NousResearch/hermes-example-plugins.git
mkdir -p ~/.hermes/plugins
cp -r hermes-example-plugins/plugin-hook-example ~/.hermes/plugins/
hermes plugins enable plugin-hook-example
```

Start a new session after enabling the plugin.

## Prompts

The upstream test asks the assistant to repeat this fictitious value:

```text
my SSN is 123-45-6789
```

Check the stored final reply for `[REDACTED:ssn]` and the count-only entry in `hermes logs`.

## Skills Needed

- `plugin-hook-example`
- Hermes lifecycle hooks

## Notes

- With CLI streaming, raw tokens may already appear before the replacement is printed. This is a final-transcript filter, not prevention of every display or disclosure.
- It does not filter inbound prompts, tool payloads, or provider requests.
- It covers selected US SSN/card formats, not Canadian SINs, every PII format, or comprehensive DLP.
- Unlike [OpenShell](hermes-openshell-sandbox.md), it changes final text rather than enforcing execution or network policy.

## Sources

- Official example and pattern limits: <https://github.com/NousResearch/hermes-example-plugins/tree/main/plugin-hook-example>
- Hook reference: <https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks#transform_llm_output>
