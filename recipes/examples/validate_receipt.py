#!/usr/bin/env python3
"""Check the example receipt contract, independently of any model/provider."""

import argparse
import json
import math
from pathlib import Path
import re


def validate(record):
    if not isinstance(record, dict) or set(record) != {"vendor", "total", "currency", "tags"}:
        raise ValueError("Expected exactly vendor, total, currency, and tags")
    if not isinstance(record["vendor"], str) or not record["vendor"].strip():
        raise ValueError("vendor must be a nonempty string")
    total = record["total"]
    if isinstance(total, bool) or not isinstance(total, (int, float)) or (isinstance(total, float) and not math.isfinite(total)) or total < 0:
        raise ValueError("total must be a finite, nonnegative number")
    if not isinstance(record["currency"], str) or not re.fullmatch(r"[A-Z]{3}", record["currency"]):
        raise ValueError("currency must be a three-letter uppercase code")
    tags = record["tags"]
    if not isinstance(tags, list) or not all(isinstance(tag, str) and tag.strip() for tag in tags):
        raise ValueError("tags must be a list of nonempty strings")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        validate(json.loads(args.path.read_text(encoding="utf-8")))
    except (ValueError, OSError) as error:
        parser.exit(1, f"FAIL: {error}\n")
    print("PASS: receipt structure matches the example contract; contents still require review.")


if __name__ == "__main__":
    main()
