"""Offline starter behavior tests. Fake CLIs are fixtures, never Hermes executions."""

from contextlib import contextmanager, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("starter", ROOT / "demos/_shared/starter.py")
starter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(starter)
TOKEN = "123456789:offline_fixture_token_abcdefghijk"
KEY = "offline-fixture-server-key-1234567890"

FAKE_CLI = '''
import json, os, sys
from pathlib import Path
kind = Path(sys.argv[0]).name
args = sys.argv[1:]
log = Path(os.environ['FIXTURE_LOG'])
with log.open('a') as stream:
    stream.write(json.dumps([kind] + args) + '\\n')
if kind == 'docker':
    sys.exit(int(os.environ.get('FIXTURE_DOCKER_EXIT', '0')))
if args[:1] != ['--profile']:
    sys.exit(9)
args = args[2:]
state = Path(os.environ['FIXTURE_STATE'])
values = json.loads(state.read_text()) if state.exists() else {}
if args[:2] == ['config', 'set']:
    if args[2] == os.environ.get('FIXTURE_FAIL_KEY'):
        print('echoed secret: ' + args[3], file=sys.stderr)
        sys.exit(7)
    values[args[2]] = args[3]
    state.write_text(json.dumps(values))
elif args[:2] == ['config', 'get']:
    print(values.get(args[2], 'missing'))
elif args == ['version']:
    print('fixture CLI, not Hermes')
elif args[:2] == ['cron', 'create']:
    print('fixture-paused-job')
elif args != ['cron', 'list']:
    sys.exit(8)
'''


class StarterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.bin = self.home / "bin"
        self.bin.mkdir()
        for name in ("hermes", "docker"):
            path = self.bin / name
            path.write_text(f"#!{sys.executable}\n" + FAKE_CLI)
            path.chmod(0o755)
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ.get("PATH", ""),
                        FIXTURE_LOG=str(self.home / "calls.jsonl"), FIXTURE_STATE=str(self.home / "state.json"))

    def config(self, demo, **overrides):
        values = {"HERMES_PROFILE": "fixture-demo"}
        if demo == "daily-briefing":
            values.update(BRIEFING_NAME="Fixture brief", BRIEFING_SCHEDULE="0 8 * * *")
        elif demo == "team-telegram":
            values.update(TELEGRAM_BOT_TOKEN=TOKEN, TELEGRAM_ALLOWED_USERS="123,456")
        else:
            values.update(API_SERVER_KEY=KEY)
        values.update(overrides)
        path = self.home / f"{demo}.env"
        path.write_text("\n".join(key + "=" + json.dumps(value) for key, value in values.items()) + "\n")
        return path

    def invoke(self, demo, script, config, *args):
        return subprocess.run(["bash", str(ROOT / "demos" / demo / script), "--env-file", str(config), *args],
                              cwd=self.home, env=self.env, capture_output=True, text=True)

    def calls(self):
        path = Path(self.env["FIXTURE_LOG"])
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def test_daily_dry_run_executes_nothing(self):
        result = self.invoke("daily-briefing", "setup-local.sh", self.config("daily-briefing"), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--paused", result.stdout)
        self.assertEqual(self.calls(), [])

    def test_daily_setup_creates_paused_job_without_running_it(self):
        result = self.invoke("daily-briefing", "setup-local.sh", self.config("daily-briefing"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.calls()), 2)
        create = self.calls()[1]
        self.assertEqual(create[:5], ["hermes", "--profile", "fixture-demo", "cron", "create"])
        self.assertIn("--paused", create)
        self.assertEqual(create[create.index("--deliver") + 1], "local")
        self.assertIn("Rerunning setup creates another paused job", result.stdout)

    def test_telegram_delivery_uses_explicit_chat(self):
        result = self.invoke("daily-briefing", "setup-telegram.sh", self.config("daily-briefing", TELEGRAM_CHAT_ID="-100123"), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("telegram:-100123", result.stdout)
        self.assertEqual(self.calls(), [])

    def test_missing_telegram_chat_fails_before_any_command(self):
        result = self.invoke("daily-briefing", "setup-telegram.sh", self.config("daily-briefing"))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_team_dry_run_redacts_token(self):
        result = self.invoke("team-telegram", "setup.sh", self.config("team-telegram"), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(TOKEN, result.stdout + result.stderr)
        self.assertIn("<redacted>", result.stdout)
        self.assertEqual(self.calls(), [])

    def test_wildcard_allowlist_rejected_before_mutation(self):
        result = self.invoke("team-telegram", "setup.sh", self.config("team-telegram", TELEGRAM_ALLOWED_USERS="*"))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_docker_failure_prevents_configuration_writes(self):
        self.env["FIXTURE_DOCKER_EXIT"] = "1"
        result = self.invoke("team-telegram", "setup.sh", self.config("team-telegram"))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(any("set" in call for call in self.calls()))

    def test_team_setup_and_smoke_use_same_named_profile(self):
        config = self.config("team-telegram")
        setup = self.invoke("team-telegram", "setup.sh", config)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        smoke = self.invoke("team-telegram", "smoke.sh", config)
        self.assertEqual(smoke.returncode, 0, smoke.stderr)
        self.assertIn("Telegram login and message handling are untested", smoke.stdout)
        for call in self.calls():
            if call[0] == "hermes":
                self.assertEqual(call[1:3], ["--profile", "fixture-demo"])
        self.assertNotIn(TOKEN, setup.stdout + setup.stderr + smoke.stdout + smoke.stderr)

    def test_team_smoke_rejects_changed_backend(self):
        config = self.config("team-telegram")
        self.invoke("team-telegram", "setup.sh", config)
        path = Path(self.env["FIXTURE_STATE"])
        state = json.loads(path.read_text())
        state["terminal.backend"] = "local"
        path.write_text(json.dumps(state))
        self.assertNotEqual(self.invoke("team-telegram", "smoke.sh", config).returncode, 0)

    def test_failed_cli_does_not_expose_echoed_secret(self):
        self.env["FIXTURE_FAIL_KEY"] = "TELEGRAM_BOT_TOKEN"
        result = self.invoke("team-telegram", "setup.sh", self.config("team-telegram"))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(TOKEN, result.stdout + result.stderr)
        self.assertIn("exit 7", result.stderr)

    def test_search_key_is_redacted(self):
        secret = "offline-search-key-sentinel"
        result = self.invoke("daily-briefing", "setup-local.sh", self.config("daily-briefing", FIRECRAWL_API_KEY=secret), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(secret, result.stdout + result.stderr)

    def test_webui_uses_current_api_settings(self):
        result = self.invoke("openwebui", "setup.sh", self.config("openwebui"))
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(Path(self.env["FIXTURE_STATE"]).read_text())
        self.assertEqual(state["API_SERVER_HOST"], "127.0.0.1")
        self.assertEqual(state["API_SERVER_KEY"], KEY)
        self.assertNotIn(KEY, result.stdout + result.stderr)
        smoke = self.invoke("openwebui", "smoke.sh", self.config("openwebui"))
        self.assertEqual(smoke.returncode, 0, smoke.stderr)
        self.assertTrue(any(call[-2:] == ["config", "--quiet"] for call in self.calls()))

    def test_short_server_key_rejected(self):
        result = self.invoke("openwebui", "setup.sh", self.config("openwebui", API_SERVER_KEY="short"))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_env_contents_are_never_executed(self):
        marker = self.home / "executed"
        config = self.config("team-telegram", TELEGRAM_BOT_TOKEN=f"$(touch {marker})")
        result = self.invoke("team-telegram", "setup.sh", config)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(marker.exists())
        self.assertEqual(self.calls(), [])

    def test_default_env_is_relative_to_starter_not_working_directory(self):
        copied = self.home / "copied-demos"
        shutil.copytree(ROOT / "demos", copied)
        shutil.copyfile(self.config("daily-briefing"), copied / "daily-briefing/.env")
        result = subprocess.run(["bash", str(copied / "daily-briefing/setup-local.sh"), "--dry-run"],
                                cwd=self.home, env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


@contextmanager
def local_api(status=200, payload=None, redirect=False):
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append((self.path, self.headers.get("Authorization")))
            self.send_response(302 if redirect and self.path != "/trap" else status)
            if redirect:
                self.send_header("Location", "/trap")
            self.end_headers()
            body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/v1/models", requests
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


class ModelListProbeTests(unittest.TestCase):
    def test_authenticated_read_only_model_list(self):
        with local_api(payload={"data": [{"id": "fixture-model"}]}) as (url, requests):
            output = io.StringIO()
            with redirect_stdout(output):
                starter.probe_models({"API_SERVER_KEY": KEY}, url)
            self.assertEqual(requests, [("/v1/models", "Bearer " + KEY)])
            self.assertNotIn(KEY, output.getvalue())

    def test_rejects_empty_models_and_malformed_json(self):
        for payload in ({"data": []}, {"data": "wrong type"}, b"not-json"):
            with self.subTest(payload=payload), local_api(payload=payload) as (url, _):
                with self.assertRaises(starter.StarterError):
                    starter.probe_models({"API_SERVER_KEY": KEY}, url)

    def test_http_auth_and_server_failures(self):
        for status in (401, 500):
            with self.subTest(status=status), local_api(status=status, payload={}) as (url, _):
                with self.assertRaises(starter.StarterError) as error:
                    starter.probe_models({"API_SERVER_KEY": KEY}, url)
                self.assertIn(str(status), str(error.exception))
                self.assertNotIn(KEY, str(error.exception))

    def test_does_not_follow_redirects_with_bearer_key(self):
        with local_api(payload={}, redirect=True) as (url, requests):
            with self.assertRaises(starter.StarterError):
                starter.probe_models({"API_SERVER_KEY": KEY}, url)
            self.assertEqual(len(requests), 1)


if __name__ == "__main__":
    unittest.main()
