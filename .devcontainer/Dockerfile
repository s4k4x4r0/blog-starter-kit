FROM mcr.microsoft.com/devcontainers/base:debian-12@sha256:23fa69fed758b7927c60061317d73baf7d66b9fca5c344e80bce3a940b229af0

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

# uv (公式Docker imageからバイナリコピー — ダイジェスト固定: v0.11.21)
COPY --from=ghcr.io/astral-sh/uv:0.11.21@sha256:ff07b86af50d4d9391d9daf4ff89ce427bc544f9aae87057e69a1cc0aa369946 /uv /uvx /usr/local/bin/
ENV UV_LINK_MODE=copy

# AWS CLI v2 (公式インストーラー)
RUN ARCH=$(uname -m) \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-${ARCH}.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# agent-browser + Chromium (グローバルインストール + システム依存)
RUN npm install -g agent-browser@0.27.3 \
    && npx -y playwright@1.61.0 install --with-deps chromium

# textlint (グローバルインストール — hooks/textlint-draft.sh で使用)
RUN npm install -g \
    textlint@15.7.1 \
    textlint-rule-preset-ja-technical-writing@12.0.2 \
    @textlint-ja/textlint-rule-preset-ai-writing@1.7.0

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
