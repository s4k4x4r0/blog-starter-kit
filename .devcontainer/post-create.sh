#!/bin/bash
set -euo pipefail

# プロジェクト固有のセットアップ（リポジトリclone後に実行）

# git hooks (gitleaks等)
pre-commit install

# agent-browser skill
# skills CLI とスキル本体(agent-browserリポジトリ)の両方をバージョン/commit SHAで固定する
npx -y skills@1.5.11 add vercel-labs/agent-browser#2c7991c9eccca1c9db6eee1a26a713414778de5a --skill agent-browser --agent claude-code cursor --yes
