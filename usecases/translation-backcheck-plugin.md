# Translation with Back-Translation Checks

**Class:** First-party demo · **Confidence:** High · **Demo status:** Runnable reference plugin; not executed for this catalog update

## Pain Point

A quick translation gives little indication of whether the original meaning survived, and serial review calls add latency.

## What It Does

Nous Research's async reference plugin adds `/translate`. Forward translation and a sentiment/category pass run concurrently through `ctx.llm.acomplete()`. A dependent back-translation then compares the result with the English input. Output includes the translation, back-check, a heuristic confidence label, category, and usage information.

## Setup

Install into the default profile of a current Hermes installation:

```bash
git clone https://github.com/NousResearch/hermes-example-plugins.git
mkdir -p ~/.hermes/plugins
cp -r hermes-example-plugins/plugin-llm-async-example ~/.hermes/plugins/
hermes plugins enable plugin-llm-async-example
```

Start a new session with an active model configured. The example uses host-owned model access rather than storing a second set of credentials.

## Prompts

Actual upstream commands:

```text
/translate fr: I'll be there in five minutes.
/translate Japanese: How much does this cost?
/translate de: Could you send me the report by Friday?
```

## Skills Needed

- `plugin-llm-async-example`
- Hermes async plugin LLM API and an active model

## Notes

- The demo assumes English source text; it is not a general language-detection pipeline.
- The back-check label is a string-similarity heuristic, not calibrated translation accuracy.
- Three model calls are made per request. Concurrency can reduce elapsed time without eliminating those calls.
- This adds an implemented translation review loop beyond generic content generation.

## Sources

- Official async example: <https://github.com/NousResearch/hermes-example-plugins/tree/main/plugin-llm-async-example>
- Plugin LLM API: <https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access>
