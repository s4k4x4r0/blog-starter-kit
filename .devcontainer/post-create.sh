#!/bin/bash
set -euo pipefail

# プロジェクト固有のセットアップ（リポジトリclone後に実行）

# Node依存をプロジェクトローカルに導入（pnpm-lock.yaml で全ツリーを固定）
# --frozen-lockfile: lockfileと不一致なら失敗させ、こっそりした差し替えを拒否する
pnpm install --frozen-lockfile

# Chromium ブラウザバイナリ（OS依存ライブラリはイメージビルド時に導入済み）
pnpm exec playwright install chromium

# git hooks (gitleaks等)
pre-commit install

# agent-browser skill
# skills CLI は pnpm-lock.yaml で固定済み。スキル本体は commit SHA で固定する
pnpm exec skills add vercel-labs/agent-browser#2c7991c9eccca1c9db6eee1a26a713414778de5a --skill agent-browser --agent claude-code cursor --yes
