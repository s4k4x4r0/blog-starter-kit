#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = "==3.13.*"
# dependencies = []
# ///
"""
agent-browser のセットアップ状況を確認するスクリプト（確認のみ、インストールはしない）。

終了コード:
    0: 全て利用可能
    1: コマンド未導入
    2: スキル未導入
    3: ブラウザ動作不可
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
NC = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}✓{NC} {msg}")


def ng(msg: str) -> None:
    print(f"{YELLOW}✗{NC} {msg}")


def fail(msg: str) -> None:
    print(f"{RED}✗{NC} {msg}")


def find_project_root() -> Path:
    """プロジェクトルートを検出（.agents/ がある最も近い親ディレクトリ）。"""
    dir = Path.cwd()
    while dir != dir.parent:
        if (dir / ".agents").is_dir():
            return dir
        dir = dir.parent
    return Path.cwd()


def check_command() -> str | None:
    """agent-browser コマンドの存在を確認する。見つかればパスを返す。"""
    path = shutil.which("agent-browser")
    if path:
        try:
            result = subprocess.run(
                ["agent-browser", "--version"],
                capture_output=True, text=True, timeout=10,
            )
            version = result.stdout.strip() or "unknown"
        except Exception:
            version = "unknown"
        ok(f"agent-browser コマンド: インストール済み ({version})")
        return path
    else:
        ng("agent-browser コマンド: 未インストール")
        print("  NEED_INSTALL_CMD")
        return None


def check_skill(project_root: Path) -> bool:
    """agent-browser スキルのインストール状況を確認する。"""
    skill_path = project_root / ".agents" / "skills" / "agent-browser" / "SKILL.md"
    if skill_path.is_file():
        ok("agent-browser スキル: インストール済み")
        return True
    else:
        ng("agent-browser スキル: 未インストール")
        print("  NEED_INSTALL_SKILL")
        return False


def check_browser() -> bool:
    """ブラウザの起動・スクリーンショット動作を確認する。"""
    print()
    print("ブラウザの起動を確認しています...")

    tmp = tempfile.NamedTemporaryFile(suffix=".png", prefix="agent-browser-check-", delete=False)
    tmp_path = tmp.name
    tmp.close()

    try:
        # ブラウザを開く
        result = subprocess.run(
            ["agent-browser", "open", "data:text/html,<h1>OK</h1>"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            fail("ブラウザ動作: 起動に失敗")
            _close_browser()
            print("  NEED_BROWSER_SETUP")
            return False

        # スクリーンショットを撮る
        result = subprocess.run(
            ["agent-browser", "screenshot", tmp_path],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0 or not Path(tmp_path).is_file() or Path(tmp_path).stat().st_size == 0:
            fail("ブラウザ動作: スクリーンショット撮影に失敗")
            _close_browser()
            print("  NEED_BROWSER_SETUP")
            return False

        ok("ブラウザ動作: 正常")
        _close_browser()
        return True
    except subprocess.TimeoutExpired:
        fail("ブラウザ動作: タイムアウト")
        _close_browser()
        print("  NEED_BROWSER_SETUP")
        return False
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _close_browser() -> None:
    try:
        subprocess.run(
            ["agent-browser", "close"],
            capture_output=True, text=True, timeout=10,
        )
    except Exception:
        pass


def main() -> None:
    print("=== agent-browser セットアップチェック ===")
    print()

    # 1. コマンドの確認
    if not check_command():
        sys.exit(1)

    # 2. スキルの確認
    project_root = find_project_root()
    if not check_skill(project_root):
        sys.exit(2)

    # 3. ブラウザの動作確認
    if not check_browser():
        sys.exit(3)

    print()
    print(f"{GREEN}=== agent-browser は利用可能です ==={NC}")


if __name__ == "__main__":
    main()
