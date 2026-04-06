FROM mcr.microsoft.com/devcontainers/base:debian-12

# ============================================================
# root: システムパッケージとグローバルバイナリ
# ============================================================

# Node.js LTS (NodeSource APTリポジトリ)
ARG NODE_MAJOR=22
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
      | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" \
      > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# uv (公式Docker imageからバイナリコピー)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
ENV UV_LINK_MODE=copy

# AWS CLI v2 (公式インストーラー)
RUN ARCH=$(uname -m) \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-${ARCH}.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# agent-browser + Chromium (グローバルインストール + システム依存)
RUN npm install -g agent-browser \
    && npx -y playwright install --with-deps chromium

# textlint (グローバルインストール — hooks/textlint-draft.sh で使用)
RUN npm install -g \
    textlint \
    textlint-rule-preset-ja-technical-writing \
    @textlint-ja/textlint-rule-preset-ai-writing

# ============================================================
# vscode: ユーザーレベルのツール
# ============================================================
USER vscode

# Python
RUN uv python install 3.13

# pre-commit
RUN uv tool install pre-commit

# Claude Code (公式インストーラー)
# WORKDIRが / だとスキャンでハングするため専用の一時ディレクトリで実行する
RUN WORK=$(mktemp -d) && cd "$WORK" && curl -fsSL https://claude.ai/install.sh | bash && rm -rf "$WORK"
