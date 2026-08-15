from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "bp.py"
SPEC = importlib.util.spec_from_file_location("bp", MODULE_PATH)
assert SPEC and SPEC.loader
bp = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bp)


class RepositoryStatusTests(unittest.TestCase):
    @mock.patch("subprocess.run")
    def test_repository_status_includes_tracked_and_untracked_files(self, run: mock.Mock) -> None:
        run.return_value = mock.Mock(stdout=" M README.md\n?? output/new.md\n")

        self.assertEqual(bp.repository_status(), [" M README.md", "?? output/new.md"])
        run.assert_called_once_with(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=bp.ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    @mock.patch.object(bp, "repository_status", return_value=[])
    @mock.patch.object(bp, "run")
    def test_check_succeeds_for_clean_reproducible_repository(
        self, run: mock.Mock, repository_status: mock.Mock
    ) -> None:
        self.assertEqual(bp.check(), 0)
        self.assertEqual(run.call_count, 4)
        repository_status.assert_called_once_with()

    @mock.patch.object(bp, "repository_status", return_value=["?? output/new.md"])
    @mock.patch.object(bp, "run")
    def test_check_fails_when_generation_changes_repository(
        self, run: mock.Mock, repository_status: mock.Mock
    ) -> None:
        self.assertEqual(bp.check(), 1)
        self.assertEqual(run.call_count, 4)
        repository_status.assert_called_once_with()

    @mock.patch.object(bp, "repository_status", return_value=["M architectuur/world.bp"])
    @mock.patch.object(bp, "run")
    def test_check_pre_commit_skips_worktree_gate(
        self, run: mock.Mock, repository_status: mock.Mock
    ) -> None:
        self.assertEqual(bp.check(require_clean_tree=False), 0)
        self.assertEqual(run.call_count, 4)
        repository_status.assert_not_called()

    def test_main_pre_commit_flag_disables_worktree_gate(self) -> None:
        with mock.patch.object(bp, "check", return_value=0) as check:
            with mock.patch("sys.argv", ["bp.py", "check", "--pre-commit"]):
                self.assertEqual(bp.main(), 0)
        check.assert_called_once_with(require_clean_tree=False)

    def test_main_defaults_to_worktree_gate(self) -> None:
        with mock.patch.object(bp, "check", return_value=0) as check:
            with mock.patch("sys.argv", ["bp.py", "check"]):
                self.assertEqual(bp.main(), 0)
        check.assert_called_once_with(require_clean_tree=True)


if __name__ == "__main__":
    unittest.main()
