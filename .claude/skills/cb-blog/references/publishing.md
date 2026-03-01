# WordPress投稿フェーズ

## 前提

WordPress MCP サーバーが設定済みであること。
MCP設定は `.claude/mcp.json` または `.cursor/mcp.json` を参照してください。

## やること

1. `blog/<article-id>/draft.md` の内容を最終確認する
2. `project.yaml` から記事メタ情報（タイトル、タグ等）を取得する
3. WordPress MCP を使って記事を投稿する

## 投稿手順

### 1. 画像のアップロード

`blog/<article-id>/images/` 内の画像がある場合、先にアップロードする。
MCP の画像アップロード機能を使用し、返却されたURLで draft.md 内の画像パスを置換する。

### 2. 記事の投稿

MCP の記事作成機能を使用して投稿する。

- ステータス: **draft**（下書き）で投稿する。公開はユーザーが手動で行う。
- カテゴリ・タグ: `project.yaml` の情報を使用する
- Markdown から Gutenberg ブロックへの変換は MCP サーバーが自動で行う

### 3. 投稿後

- ユーザーに投稿URLを伝える
- `project.yaml` の `phase` を `published` に更新する
- 必要に応じて `wordpress_post_id` を `project.yaml` に記録する

## phase の更新

投稿完了後 `phase: review` -> `phase: published` に更新してください。
