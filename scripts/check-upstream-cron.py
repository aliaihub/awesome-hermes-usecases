#!/usr/bin/env python3
"""Check recipe grammar with pinned upstream argparse functions, not a Hermes runtime."""

import argparse
import ast
import hashlib
from pathlib import Path
from typing import Callable

SOURCE_SHA256 = "c07a27db9575afd77dfd7e1e0f0051241262706c11998d92f8b26369536f3222"
EXAMPLES = [
    ["cron", "create", "0 8 * * *", "Brief", "--name", "Morning brief", "--deliver", "local", "--paused"],
    ["cron", "create", "0 8 * * *", "Brief", "--name", "Morning brief", "--deliver", "telegram:-100123", "--paused"],
    ["cron", "create", "0 9 * * 1-5", "Report", "--name", "Developer release brief", "--deliver", "local", "--paused"],
    ["cron", "create", "every 15m", "--script", "/tmp/watchdog.py", "--no-agent", "--deliver", "local", "--name", "Disk watchdog", "--paused"],
    ["cron", "create", "every 1d", "Report", "--skill", "fixture-skill", "--name", "Skill report", "--deliver", "local", "--paused"],
    ["cron", "create", "0 16 * * 1-5", "Review", "--workdir", "/tmp", "--name", "Project review", "--deliver", "local", "--paused"],
    ["cron", "list"], ["cron", "status"], ["cron", "doctor"], ["cron", "run", "fixture-id"],
    ["cron", "runs", "fixture-id"], ["cron", "resume", "fixture-id"],
    ["cron", "pause", "fixture-id"], ["cron", "remove", "fixture-id"],
]


def main():
    options = argparse.ArgumentParser(description=__doc__)
    options.add_argument("source", type=Path, help="Pinned upstream hermes_cli/subcommands/cron.py")
    args = options.parse_args()
    raw = args.source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        options.error("Source does not match the reviewed v0.22.5 parser; refusing to execute it")
    source = ast.parse(raw.decode("utf-8"))
    functions = ast.Module(body=[node for node in source.body if isinstance(node, ast.FunctionDef)
                                 and node.name in {"_flag", "build_cron_parser"}], type_ignores=[])
    # Only these pure argument-building functions are loaded. Their imported hook
    # flag registrar is a local stand-in; hook behavior is outside this check.
    namespace = {"Callable": Callable,
                 "add_accept_hooks_flag": lambda parser: parser.add_argument("--accept-hooks", action="store_true")}
    exec(compile(functions, "reviewed-upstream-cron-parser", "exec"), namespace)
    parser = argparse.ArgumentParser()
    namespace["build_cron_parser"](parser.add_subparsers(), cmd_cron=lambda _: None)
    for example in EXAMPLES:
        parser.parse_args(example)
    print(f"PASS: {len(EXAMPLES)} cron argument examples accepted by pinned upstream argparse functions.")
    print("Scope: grammar only; no Hermes imports, hook runtime, scheduler, gateway, or model execution.")


if __name__ == "__main__":
    main()
