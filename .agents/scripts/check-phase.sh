#!/bin/bash
# phase 遷移前の機械チェック。
# エディタや AI ツールに依存せず、コマンド実行だけで遷移条件のうち
# 機械的に確認できる部分（ファイルの存在・textlint 合格）を検証する。
# ここで検証するのは機械チェックのみで、ユーザー合意などの残りの遷移条件は
# 各リファレンス（writing.md / publishing.md）に従うこと。
#
# 使い方:
#   .agents/scripts/check-phase.sh <article-id> <draft_completed|posted>
#
# 終了コード:
#   0 = 合格（WARN は合否に影響しない）
#   1 = 不合格（NG が1件以上）
#   2 = 使い方の誤り

set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
ARTICLE_ID="${1:-}"
TARGET_PHASE="${2:-}"

if [ -z "$ARTICLE_ID" ] || [ -z "$TARGET_PHASE" ]; then
  echo "使い方: $0 <article-id> <draft_completed|posted>" >&2
  exit 2
fi

if ! printf '%s' "$ARTICLE_ID" | grep -Eq '^[A-Za-z0-9][A-Za-z0-9._-]*$'; then
  echo "エラー: article-id に使えない文字が含まれている（指定: ${ARTICLE_ID}）" >&2
  exit 2
fi

case "$TARGET_PHASE" in
  draft_completed|posted) ;;
  *)
    echo "エラー: 対応している遷移先は draft_completed / posted のみです（指定: ${TARGET_PHASE}）" >&2
    exit 2
    ;;
esac

ARTICLE_DIR="$ROOT/blog/$ARTICLE_ID"
DRAFT="$ARTICLE_DIR/draft.md"
FAIL=0

ok()   { echo "OK:   $1"; }
ng()   { echo "NG:   $1"; FAIL=1; }
warn() { echo "WARN: $1"; }

# --- 1. project.yaml への登録 ---
# 記事は企画フェーズ（ideation.md Step 3）で project.yaml に登録される。
# 未登録なら article-id の打ち間違いか、フローを飛ばしている可能性が高い
ARTICLE_ID_RE=$(printf '%s' "$ARTICLE_ID" | sed 's/[.]/\\./g')
if [ -f "$ROOT/project.yaml" ] && grep -Eq "^[^#]*id:[[:space:]]*[\"']?${ARTICLE_ID_RE}[\"']?[[:space:]]*$" "$ROOT/project.yaml"; then
  ok "project.yaml に記事 $ARTICLE_ID が登録されている"
else
  ng "project.yaml に記事 $ARTICLE_ID が登録されていない（article-id の打ち間違いに注意）"
fi

# --- 2. draft.md の存在と本文 ---
if [ -s "$DRAFT" ]; then
  ok "blog/$ARTICLE_ID/draft.md が存在し、本文がある"
elif [ -f "$DRAFT" ]; then
  ng "blog/$ARTICLE_ID/draft.md が空ファイル"
  exit 1
else
  ng "blog/$ARTICLE_ID/draft.md が存在しない"
  # 以降のチェックは draft.md 前提のため、ここで打ち切る
  exit 1
fi

# --- 3. 本文が参照する画像の存在 ---
# writing.md の規約どおり images/ への相対参照（![alt](images/xxx.png)）を対象にする。
# コードブロック内は Markdown の例示であることが多いため、フェンスの内側を除外してから探す。
# 規約外の書き方（参照形式・HTML の img タグ・入れ子の角括弧を含む alt など）は対象にしない
DRAFT_BODY=$(awk '/^[[:space:]]*(```|~~~)/{inblock=!inblock; next} !inblock' "$DRAFT")
MISSING_IMAGES=0
while IFS= read -r img; do
  [ -z "$img" ] && continue
  if [ ! -f "$ARTICLE_DIR/$img" ]; then
    ng "本文が参照する画像が存在しない: blog/$ARTICLE_ID/$img"
    MISSING_IMAGES=1
  fi
done < <(printf '%s\n' "$DRAFT_BODY" \
  | grep -oE '!\[[^]]*\]\((\./)?images/[^)]+\)' \
  | sed -E 's/^!\[[^]]*\]\(//; s/\)$//; s/^\.\///; s/[[:space:]]+"[^"]*"$//' \
  | sort -u)

if [ "$MISSING_IMAGES" -eq 0 ]; then
  ok "本文が参照する画像がすべて存在する"
fi

# --- 4. textlint ---
# .agents/tools のローカル導入を優先する。未導入環境では npx フォールバックを使うが、
# 固定されるのは直指定した3パッケージのバージョンのみ（pnpm-lock.yaml は使われない）で、
# ネットワークも必要になるため、可能なら .agents/tools への導入を推奨する
TEXTLINT_BIN="$ROOT/.agents/tools/node_modules/.bin/textlint"
if [ -x "$TEXTLINT_BIN" ]; then
  RESULT=$(cd "$ROOT" && "$TEXTLINT_BIN" --no-color "blog/$ARTICLE_ID/draft.md" 2>&1)
  TEXTLINT_STATUS=$?
elif command -v npx >/dev/null 2>&1; then
  # npx はインストール失敗でも終了コード 1 を返すことがあり、lint の指摘と区別できない。
  # 先にツールの解決だけを試し、環境要因の失敗をここで切り分ける
  NPX_PKGS=(-p textlint@15.7.1 \
    -p textlint-rule-preset-ja-technical-writing@12.0.2 \
    -p @textlint-ja/textlint-rule-preset-ai-writing@1.7.0)
  SETUP=$(cd "$ROOT" && npx -y "${NPX_PKGS[@]}" textlint --version 2>&1)
  if [ $? -ne 0 ]; then
    RESULT="npx で textlint を準備できなかった: $SETUP"
    TEXTLINT_STATUS=127
  else
    RESULT=$(cd "$ROOT" && npx -y "${NPX_PKGS[@]}" textlint --no-color "blog/$ARTICLE_ID/draft.md" 2>&1)
    TEXTLINT_STATUS=$?
  fi
else
  RESULT="textlint が見つからない。README の手順で .agents/tools にツールを導入すること"
  TEXTLINT_STATUS=127
fi

case "$TEXTLINT_STATUS" in
  0)
    ok "textlint に合格した"
    ;;
  1)
    ng "textlint の指摘が残っている:"
    echo "$RESULT"
    ;;
  *)
    ng "textlint を実行できなかった（lint の指摘ではなく環境要因の可能性が高い）:"
    echo "$RESULT"
    ;;
esac

# --- 5. posted のみ: アイキャッチ画像 ---
# publishing.md のフロー上、ユーザーは意図的にスキップできるため WARN 止まりにする
if [ "$TARGET_PHASE" = "posted" ]; then
  if [ -f "$ARTICLE_DIR/images/eyecatch.png" ]; then
    ok "アイキャッチ画像（images/eyecatch.png）が存在する"
  else
    warn "アイキャッチ画像（images/eyecatch.png）がない。eyecatch スキルで生成できる。意図的な省略なら問題ない"
  fi
fi

if [ "$FAIL" -eq 0 ]; then
  echo "機械チェック合格: ${ARTICLE_ID}（遷移先 ${TARGET_PHASE}）。ユーザー合意など残りの遷移条件はリファレンスに従うこと"
else
  echo "機械チェック不合格: 上記の NG を解消してから phase を更新すること" >&2
fi

exit "$FAIL"
