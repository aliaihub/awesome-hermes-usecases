# Validate structured output

## Goal

Check extracted receipt data locally before passing it to another system.

## Requires

Python 3.11+ for validation. For generation, a configured Hermes profile with file tools; the existing [receipt plugin use case](../usecases/receipt-to-structured-json.md) provides an alternative structured-generation implementation.

## Steps

Start a Hermes chat from this repository and give it this task, using an absolute input/output path:

```text
Read recipes/examples/receipt.txt. Write receipt-output.json containing exactly vendor, total, currency, and tags. total must be a nonnegative JSON number; currency must be a three-letter uppercase code; tags must be an array of strings. Use the tag "office" for this stationery receipt. Do not invent missing fields. If extraction is uncertain, report the problem instead of writing a successful record.
```

Then run the independent validator from the repository root:

```bash
python3 recipes/examples/validate_receipt.py receipt-output.json
```

To exercise the validator without a model:

```bash
python3 recipes/examples/validate_receipt.py recipes/examples/receipt.expected.json
```

## Expected result

The fictional fixture's vendor is `Example Stationery`, total is `8.4`, currency is `CAD`, and tags are `["office"]`. The validator rejects missing/extra fields and incorrect types, including boolean, negative, and nonfinite totals.

A structural pass does not verify arithmetic, extraction accuracy, or whether a currency code is real. Review contents before import.

## Failure check

Change the fixture's total to the string `"8.40"` in a temporary copy; the validator must exit nonzero. Never treat a model's claim that its JSON is valid as the validation result.

## Sources

- [Receipt extraction reference](../usecases/receipt-to-structured-json.md)
- [Python JSON behavior](https://docs.python.org/3/library/json.html)
