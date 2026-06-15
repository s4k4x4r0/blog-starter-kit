#!/bin/bash
# PostToolUse hook: blog/*/draft.md が編集されたら textlint を実行し結果を注入する

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# ファイルパスが取得できない場合はスキップ
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# blog/*/draft.md 以外はスキップ
if ! echo "$FILE_PATH" | grep -qE '/blog/[^/]+/draft\.md$'; then
  exit 0
fi

# ファイルが存在しない場合はスキップ
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# textlint 実行（.agents/tools のローカル導入を優先。未導入環境では
# lockfile相当のバージョンを固定した npx フォールバックを使う）
TEXTLINT_BIN="${CLAUDE_PROJECT_DIR:-.}/.agents/tools/node_modules/.bin/textlint"
if [ -x "$TEXTLINT_BIN" ]; then
  RESULT=$("$TEXTLINT_BIN" --no-color "$FILE_PATH" 2>&1)
else
  RESULT=$(npx -y \
    -p textlint@15.7.1 \
    -p textlint-rule-preset-ja-technical-writing@12.0.2 \
    -p @textlint-ja/textlint-rule-preset-ai-writing@1.7.0 \
    textlint --no-color "$FILE_PATH" 2>&1)
fi

STATUS=$?

if [ $STATUS -eq 0 ]; then
  exit 0
else
  echo "textlint found issues in draft.md. Please fix them:" >&2
  echo "$RESULT" >&2
  exit 2
fi
