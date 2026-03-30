import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import codex_switcher


class ProxyAuthSyncTests(unittest.TestCase):
    def test_sync_enables_target_and_disables_other_active_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            proxy_dir = Path(tmp)
            active_other = proxy_dir / "codex-11111111-other@example.com-team.json"
            disabled_target = proxy_dir / "codex-22222222-target@example.com-team.json.disabled-20260330-000000"
            active_other.write_text("{}", encoding="utf-8")
            disabled_target.write_text("{}", encoding="utf-8")

            with patch.dict("os.environ", {"CODEX_SWITCHER_PROXY_AUTH_DIR": str(proxy_dir)}, clear=False):
                with patch("codex_switcher.restart_local_proxy_service", return_value={"ok": True, "label": "test"}) as restart:
                    result = codex_switcher.sync_proxy_auth_for_email("target@example.com")

            self.assertTrue(result["ok"])
            self.assertEqual(result["matched_count"], 1)
            self.assertEqual(result["enabled_email"], "target@example.com")
            self.assertTrue((proxy_dir / "codex-22222222-target@example.com-team.json").exists())
            self.assertFalse(disabled_target.exists())
            disabled_others = list(proxy_dir.glob("codex-11111111-other@example.com-team.json.disabled-*"))
            self.assertEqual(len(disabled_others), 1)
            self.assertFalse(active_other.exists())
            restart.assert_called_once()

    def test_sync_returns_proxy_login_hint_when_no_matching_auth_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            proxy_dir = Path(tmp)
            active_other = proxy_dir / "codex-11111111-other@example.com-team.json"
            active_other.write_text("{}", encoding="utf-8")

            env = {
                "CODEX_SWITCHER_PROXY_AUTH_DIR": str(proxy_dir),
                "CODEX_SWITCHER_PROXY_LOGIN_COMMAND": "proxy-login --email target@example.com",
            }
            with patch.dict("os.environ", env, clear=False):
                result = codex_switcher.sync_proxy_auth_for_email("target@example.com")

            self.assertFalse(result["ok"])
            self.assertTrue(result["reauth_required"])
            self.assertEqual(result["login_command"], "proxy-login --email target@example.com")
            self.assertIn("proxy OAuth", result["warning"])

    def test_ensure_proxy_auth_ready_runs_proxy_login_when_reauth_required(self):
        first = {
            "ok": False,
            "reauth_required": True,
            "login_command": "proxy-login --email target@example.com",
            "warning": "need login",
        }
        second = {
            "ok": True,
            "reauth_required": False,
            "enabled_email": "target@example.com",
            "enabled_file": "codex-22222222-target@example.com-team.json",
        }

        with patch("codex_switcher.sync_proxy_auth_for_email", side_effect=[first, second]) as sync_mock:
            with patch("codex_switcher.subprocess.run", return_value=SimpleNamespace(returncode=0)) as run_mock:
                result = codex_switcher.ensure_proxy_auth_ready("target@example.com")

        self.assertTrue(result["ok"])
        self.assertEqual(sync_mock.call_count, 2)
        run_mock.assert_called_once()
        self.assertEqual(run_mock.call_args.args[0], ["proxy-login", "--email", "target@example.com"])


if __name__ == "__main__":
    unittest.main()
