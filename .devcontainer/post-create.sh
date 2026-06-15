#!/bin/bash
set -euo pipefail

# プロジェクト固有のセットアップ（リポジトリclone後に実行）

# ハーネスが使う Node ツールを .agents/tools/ にローカル導入（pnpm-lock.yaml で全ツリー固定）。
# --frozen-lockfile: lockfileと不一致なら失敗させ、こっそりした差し替えを拒否する。
# packageManager を効かせるため tools ディレクトリに cd して実行する。
# CI=true: ホスト側(別OS)の node_modules がバインドマウントで見える場合に、pnpm が
#          非対話で作り直せるようにする（TTYが無い post-create で確認プロンプトを回避）。
( cd .agents/tools && CI=true pnpm install --frozen-lockfile )

# git hooks (gitleaks等)
pre-commit install

# agent-browser skill（インストール先判定のためプロジェクトルートで実行。本体は commit SHA で固定）
.agents/tools/node_modules/.bin/skills add vercel-labs/agent-browser#2c7991c9eccca1c9db6eee1a26a713414778de5a --skill agent-browser --agent claude-code cursor --yes
