#!/bin/bash
set -euo pipefail

# プロジェクト固有のセットアップ（リポジトリclone後に実行）

# ハーネスが使う Node ツールを .agents/tools/ にローカル導入（pnpm-lock.yaml で全ツリー固定）。
# --frozen-lockfile: lockfileと不一致なら失敗させ、こっそりした差し替えを拒否する。
# packageManager を効かせるため tools ディレクトリに cd して実行する。
( cd .agents/tools && pnpm install --frozen-lockfile )

# Chromium ブラウザバイナリ・OS依存ライブラリはイメージビルド時に導入済み（Dockerfile参照）

# git hooks (gitleaks等)
pre-commit install

# agent-browser skill（インストール先判定のためプロジェクトルートで実行。本体は commit SHA で固定）
.agents/tools/node_modules/.bin/skills add vercel-labs/agent-browser#2c7991c9eccca1c9db6eee1a26a713414778de5a --skill agent-browser --agent claude-code cursor --yes
