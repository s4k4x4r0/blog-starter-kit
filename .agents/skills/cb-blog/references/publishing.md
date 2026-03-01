# WordPress投稿フェーズ

## 前提

WordPress MCP サーバーが利用可能であること。
MCP ツール（`create_post` 等）が使えない場合は、[references/mcp-setup.md](mcp-setup.md) を参照してユーザーに設定を案内してください。

## やること

1. `blog/<article-id>/draft.md` の内容を最終確認する
2. `project.yaml` から記事メタ情報（タイトル、タグ等）を取得する
3. WordPress MCP を使って記事を投稿する

## 投稿手順

### 1. 画像のアップロード

`blog/<article-id>/images/` 内の画像がある場合、先にアップロードする。
MCP の画像アップロード機能を使用し、返却されたURLで draft.md 内の画像パスを置換する。

### 2. アイキャッチ画像の設定

`blog/<article-id>/images/eyecatch.png` が存在するか確認する。

**存在する場合:**
1. `upload_media` でアイキャッチ画像をアップロードし、返却された media ID を控える
2. 次の記事投稿ステップで `featured_media` パラメータにこの media ID を指定する

**存在しない場合:**
ユーザーにアイキャッチ画像がないことを伝え、作成を提案する。
eyecatch スキル（`/eyecatch <タイトル>`）を使えばベース画像にタイトルを重ねたアイキャッチを簡単に生成できる旨を案内する。
ユーザーが不要と判断した場合はスキップしてよい。

### 3. 記事の投稿

MCP の記事作成機能を使用して投稿する。

- ステータス: **draft**（下書き）で投稿する。公開はユーザーが手動で行う。
- カテゴリ・タグ: `project.yaml` の情報を使用する
- Markdown から Gutenberg ブロックへの変換は MCP サーバーが自動で行う
- アイキャッチ画像がある場合は `featured_media` に media ID を指定する

### 4. 投稿後

- ユーザーに投稿URLを伝える
- `project.yaml` の `phase` を `posted` に更新する
- `project.yaml` に `wordpress_post_id` を記録する
