import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace

import codex_switcher


class SwitcherPathTests(unittest.TestCase):
    def test_switcher_dir_defaults_to_script_directory(self):
        expected = Path(codex_switcher.__file__).resolve().parent
        self.assertEqual(codex_switcher.get_switcher_dir(), expected)
        self.assertEqual(codex_switcher.get_accounts_dir(), expected / "accounts")
        self.assertEqual(codex_switcher.get_usage_cache_dir(), expected / "usage_cache")

    def test_switcher_dir_can_be_overridden_by_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            override = Path(tmp)
            with patch.dict("os.environ", {"CODEX_SWITCHER_DATA_DIR": str(override)}, clear=False):
                self.assertEqual(codex_switcher.get_switcher_dir(), override)
                self.assertEqual(codex_switcher.get_accounts_dir(), override / "accounts")
                self.assertEqual(codex_switcher.get_usage_cache_dir(), override / "usage_cache")

    def test_proxy_login_command_uses_direct_binary_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            binary = home / "workspace" / "openclaw" / "CLIProxyAPI" / "cliproxyapi"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_text("", encoding="utf-8")

            with patch("codex_switcher.get_home_dir", return_value=home):
                command = codex_switcher.get_proxy_login_command("target@example.com")

            self.assertEqual(command, f"{binary} -codex-login -no-browser")

    def test_proxy_login_cwd_uses_binary_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            binary = home / "workspace" / "openclaw" / "CLIProxyAPI" / "cliproxyapi"
            binary.parent.mkdir(parents=True, exist_ok=True)
            binary.write_text("", encoding="utf-8")

            with patch("codex_switcher.get_home_dir", return_value=home):
                self.assertEqual(codex_switcher.get_proxy_login_cwd("target@example.com"), binary.parent)


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

    def test_sync_returns_structured_error_when_enable_rename_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            proxy_dir = Path(tmp)
            active_other = proxy_dir / "codex-11111111-other@example.com-team.json"
            disabled_target = proxy_dir / "codex-22222222-target@example.com-team.json.disabled-20260330-000000"
            active_other.write_text("{}", encoding="utf-8")
            disabled_target.write_text("{}", encoding="utf-8")

            original_rename = Path.rename

            def guarded_rename(path_obj, target):
                if path_obj == disabled_target:
                    raise PermissionError("rename blocked")
                return original_rename(path_obj, target)

            with patch.dict("os.environ", {"CODEX_SWITCHER_PROXY_AUTH_DIR": str(proxy_dir)}, clear=False):
                with patch("pathlib.Path.rename", autospec=True, side_effect=guarded_rename):
                    result = codex_switcher.sync_proxy_auth_for_email("target@example.com")

            self.assertFalse(result["ok"])
            self.assertFalse(result["reauth_required"])
            self.assertEqual(result["enabled_email"], "target@example.com")
            self.assertIn("rename blocked", result["warning"])
            self.assertTrue(active_other.exists())
            self.assertTrue(disabled_target.exists())

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

    def test_ensure_proxy_auth_ready_runs_proxy_login_in_binary_directory(self):
        first = {
            "ok": False,
            "reauth_required": True,
            "login_command": "/tmp/CLIProxyAPI/cliproxyapi -codex-login -no-browser",
            "warning": "need login",
        }
        second = {
            "ok": True,
            "reauth_required": False,
            "enabled_email": "target@example.com",
            "enabled_file": "codex-22222222-target@example.com-team.json",
        }

        with patch("codex_switcher.sync_proxy_auth_for_email", side_effect=[first, second]):
            with patch("codex_switcher.get_proxy_login_cwd", return_value=Path("/tmp/CLIProxyAPI")):
                with patch("codex_switcher.subprocess.run", return_value=SimpleNamespace(returncode=0)) as run_mock:
                    result = codex_switcher.ensure_proxy_auth_ready("target@example.com")

        self.assertTrue(result["ok"])
        self.assertEqual(run_mock.call_args.kwargs["cwd"], "/tmp/CLIProxyAPI")


if __name__ == "__main__":
    unittest.main()
