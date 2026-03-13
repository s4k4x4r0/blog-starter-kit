FROM mcr.microsoft.com/devcontainers/base:debian-12

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

# Python
RUN uv python install 3.13

# pre-commit
RUN uv tool install pre-commit
ENV PATH="/root/.local/bin:$PATH"

# Claude Code (公式インストーラー)
# WORKDIR を設定しないと root の / スキャンでハングする
WORKDIR /tmp
RUN curl -fsSL https://claude.ai/install.sh | bash
WORKDIR /

# agent-browser + Chromium
RUN npm install -g agent-browser \
    && npx -y playwright install --with-deps chromium
