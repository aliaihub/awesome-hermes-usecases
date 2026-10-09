# Receipt Text or Image → Structured JSON

**Class:** First-party demo · **Confidence:** High · **Demo status:** Runnable reference plugin; not executed for this catalog update

## Pain Point

A receipt needs to become a machine-readable expense record without maintaining a separate provider-specific extraction client.

## What It Does

Nous Research's `plugin-llm-example` adds `/receipt-extract`. It accepts a local text or image file and requests a record containing vendor, total, currency, and tags through `ctx.llm.complete_structured()`. Hermes owns provider credentials and model routing; the plugin handles the parsed result and extraction errors.

## Setup

With a current Hermes installation and active model, install the reference plugin into the default profile:

```bash
git clone https://github.com/NousResearch/hermes-example-plugins.git
mkdir -p ~/.hermes/plugins
cp -r hermes-example-plugins/plugin-llm-example ~/.hermes/plugins/
hermes plugins enable plugin-llm-example
```

Start a new Hermes session. Image input requires a compatible vision model or routing configuration.

## Prompts

Actual commands from the plugin README:

```text
/receipt-extract /path/to/receipt.png
/receipt-extract /path/to/receipt.txt
```

Use real local file paths. The plugin's schema requires `vendor` and `total`; currency and tags are additional supported fields.

## Skills Needed

- `plugin-llm-example`
- Hermes plugin LLM API
- Active model; vision support for image inputs

## Notes

- These examples live in a separate companion repo and are not bundled with core.
- Structured output constrains format, not factual accuracy. Check totals and currency before accounting import.
- This does not reconcile accounts, deduplicate transactions, or file receipts automatically.

## Sources

- Official example and code: <https://github.com/NousResearch/hermes-example-plugins/tree/main/plugin-llm-example>
- Host API and validation behavior: <https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access>
