#!/bin/bash
set -euo pipefail

# プロジェクト固有のセットアップ（リポジトリclone後に実行）

# git hooks (gitleaks等)
pre-commit install

# agent-browser skill
npx -y skills add vercel-labs/agent-browser --skill agent-browser --agent claude-code cursor --yes
