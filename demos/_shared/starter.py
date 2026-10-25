#!/usr/bin/env python3
"""Local configuration examples for the three starter kits; no model API client."""

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEMOS = Path(__file__).resolve().parents[1]
SECRET_KEYS = {"API_SERVER_KEY", "FIRECRAWL_API_KEY", "TELEGRAM_BOT_TOKEN"}


class StarterError(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, file, code, message, headers, new_url):
        # A model-list endpoint should not redirect, especially with a bearer key.
        return None


def load_env(path):
    """Read literal KEY=value pairs without executing shell code or expanding variables."""
    if not path.is_file():
        raise StarterError(f"Missing {path}. Copy the starter's .env.example to .env first.")
    values = {}
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        key = key.strip()
        if not separator or not re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
            raise StarterError(f"Invalid setting name on line {number} of {path.name}.")
        try:
            parts = shlex.split(value, comments=True)
        except ValueError:
            raise StarterError(f"Invalid quoting on line {number} of {path.name}.") from None
        if len(parts) > 1:
            raise StarterError(f"Quote values containing spaces (line {number} of {path.name}).")
        values[key] = parts[0] if parts else ""
    return values


def required(values, key):
    value = values.get(key, "").strip()
    if not value or re.match(r"(?i)^(your[-_ ]|replace[-_ ]|change[-_ ]|example)", value):
        raise StarterError(f"Set {key} in the starter's .env.")
    return value


def hermes_command(values):
    profile = required(values, "HERMES_PROFILE")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", profile):
        raise StarterError("HERMES_PROFILE must be a simple profile name (letters, digits, _ or -).")
    return ["hermes", "--profile", profile]


def setting(command, key, value):
    return command + ["config", "set", key, value]


def make_plan(demo, values, delivery="local"):
    command = hermes_command(values)
    if demo == "daily-briefing":
        schedule = required(values, "BRIEFING_SCHEDULE")
        name = required(values, "BRIEFING_NAME")
        prompt = (DEMOS / demo / "prompt.txt").read_text(encoding="utf-8").strip()
        target = "local"
        if delivery == "telegram":
            chat = required(values, "TELEGRAM_CHAT_ID")
            if not re.fullmatch(r"-?[1-9][0-9]*", chat):
                raise StarterError("TELEGRAM_CHAT_ID must be a numeric chat ID.")
            target = "telegram:" + chat
        plan = []
        if values.get("FIRECRAWL_API_KEY"):
            plan.append(setting(command, "FIRECRAWL_API_KEY", values["FIRECRAWL_API_KEY"]))
        plan.append(command + ["cron", "create", schedule, prompt, "--name", name,
                               "--deliver", target, "--paused"])
        return plan
    if demo == "team-telegram":
        token = required(values, "TELEGRAM_BOT_TOKEN")
        if not re.fullmatch(r"[0-9]+:[A-Za-z0-9_-]{20,}", token):
            raise StarterError("TELEGRAM_BOT_TOKEN does not have the expected token shape.")
        users = required(values, "TELEGRAM_ALLOWED_USERS")
        if not re.fullmatch(r"[1-9][0-9]*(,[1-9][0-9]*)*", users):
            raise StarterError("TELEGRAM_ALLOWED_USERS must be comma-separated positive numeric user IDs.")
        plan = [setting(command, "TELEGRAM_BOT_TOKEN", token),
                setting(command, "TELEGRAM_ALLOWED_USERS", users),
                setting(command, "TELEGRAM_ALLOW_ALL_USERS", "false"),
                setting(command, "gateway.allow_all_users", "false"),
                setting(command, "terminal.backend", "docker")]
        home = values.get("TELEGRAM_HOME_CHANNEL", "")
        if home:
            if not re.fullmatch(r"-?[1-9][0-9]*", home):
                raise StarterError("TELEGRAM_HOME_CHANNEL must be a numeric chat ID.")
            plan.append(setting(command, "TELEGRAM_HOME_CHANNEL", home))
        return plan
    key = required(values, "API_SERVER_KEY")
    if len(key) < 32 or re.search(r"\s", key):
        raise StarterError("Use an API_SERVER_KEY of at least 32 characters with no whitespace.")
    return [setting(command, "API_SERVER_ENABLED", "true"),
            setting(command, "API_SERVER_HOST", "127.0.0.1"),
            setting(command, "API_SERVER_PORT", "8642"),
            setting(command, "API_SERVER_KEY", key)]


def display(command):
    safe = list(command)
    if len(safe) >= 4 and safe[-2] in SECRET_KEYS:
        safe[-1] = "<redacted>"
    return shlex.join(safe)


def run(command):
    if not shutil.which(command[0]):
        raise StarterError(f"{command[0]} is not on PATH.")
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        raise StarterError(f"Timed out: {display(command)}") from None
    if result.returncode:
        # CLI errors may echo supplied credentials; never relay captured output.
        raise StarterError(f"Command failed (exit {result.returncode}): {display(command)}")
    return result.stdout.strip()


def check_config(command, key, expected):
    actual = run(command + ["config", "get", key, "--raw"])
    if actual.lower() != expected.lower():
        raise StarterError(f"Configured {key} does not match the starter. Run its setup, then restart the gateway.")
    print(f"OK: {key} matches the starter.")


def probe_models(values, url="http://127.0.0.1:8642/v1/models"):
    # A read-only loopback request: lists models, never submits a chat/completion.
    request = Request(url,
                      headers={"Authorization": "Bearer " + values["API_SERVER_KEY"]})
    try:
        with build_opener(NoRedirect()).open(request, timeout=5) as response:
            payload = json.load(response)
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list) or not payload["data"]:
            raise StarterError("/v1/models returned no models. Check the Hermes profile and API-server configuration.")
    except HTTPError as error:
        code = error.code
        error.close()
        raise StarterError(f"Hermes model-list request returned HTTP {code}. Check the key and restart the gateway.") from None
    except (URLError, TimeoutError, json.JSONDecodeError):
        raise StarterError("Hermes model-list probe failed. Check the gateway on 127.0.0.1:8642.") from None
    print("OK: authenticated /v1/models returned a nonempty model list; chat execution is still untested.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", choices=["daily-briefing", "team-telegram", "openwebui"])
    parser.add_argument("action", choices=["setup", "smoke"])
    parser.add_argument("--deliver", choices=["local", "telegram"], default="local")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Validate and print redacted commands; execute nothing")
    parser.add_argument("--probe", action="store_true", help="For Open WebUI smoke only: read the local Hermes model list")
    args = parser.parse_args()
    if args.probe and (args.demo != "openwebui" or args.action != "smoke"):
        parser.error("--probe is only available for Open WebUI smoke checks")
    path = args.env_file or DEMOS / args.demo / ".env"
    try:
        values = load_env(path)
        plan = make_plan(args.demo, values, args.deliver)
        if args.dry_run:
            for command in plan:
                print(display(command))
            print("DRY RUN: configuration validated; no commands, network requests, or model calls executed.")
            return 0
        command = hermes_command(values)
        run(command + ["version"])
        if args.demo in {"team-telegram", "openwebui"}:
            run(["docker", "info"])
        if args.action == "setup":
            for step in plan:
                run(step)
            if args.demo == "daily-briefing":
                print("Created one PAUSED briefing job. List jobs, inspect its ID, then resume it when ready.")
                print("Rerunning setup creates another paused job; edit or remove the existing job instead.")
            else:
                print("Configuration saved. Start or restart this profile's gateway using the README.")
        else:
            if args.demo == "daily-briefing":
                run(command + ["cron", "list"])
                print("OK: profile CLI and cron store are readable. No briefing, search, or delivery was run.")
            elif args.demo == "team-telegram":
                check_config(command, "terminal.backend", "docker")
                check_config(command, "TELEGRAM_ALLOWED_USERS", values["TELEGRAM_ALLOWED_USERS"])
                check_config(command, "TELEGRAM_ALLOW_ALL_USERS", "false")
                check_config(command, "gateway.allow_all_users", "false")
                print("OK: Docker daemon and selected profile settings checked. Telegram login and message handling are untested.")
            else:
                for key, value in [("API_SERVER_ENABLED", "true"), ("API_SERVER_HOST", "127.0.0.1"), ("API_SERVER_PORT", "8642")]:
                    check_config(command, key, value)
                run(["docker", "compose", "--env-file", str(path.resolve()), "-f",
                     str(DEMOS / "openwebui" / "docker-compose.yml"), "config", "--quiet"])
                print("OK: Docker daemon, Compose configuration, and profile settings checked. No containers started.")
                if args.probe:
                    probe_models(values)
        return 0
    except (StarterError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
