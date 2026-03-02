# WordPress投稿フェーズ

## 前提

WordPress MCP サーバーが利用可能であること。
MCP ツール（`create_post` 等）が使えない場合は、[references/mcp-setup.md](mcp-setup.md) を参照してユーザーに設定を案内してください。

## やること

1. `blog/<article-id>/draft.md` の内容を最終確認する
2. `project.yaml` から記事メタ情報（タイトル等）を取得する
3. WordPress MCP でカテゴリ・タグを選定する
4. WordPress MCP を使って記事を投稿する

## 投稿手順

### 1. アイキャッチ画像の設定

`blog/<article-id>/images/eyecatch.png` が存在するか確認する。

**存在する場合:**
1. `upload_media` でアイキャッチ画像をアップロードし、返却された media ID を控える
2. 次の記事投稿ステップで `featured_media` パラメータにこの media ID を指定する

**存在しない場合:**
ユーザーにアイキャッチ画像がないことを伝え、作成を提案する。
eyecatch スキル（`/eyecatch <タイトル>`）を使えばベース画像にタイトルを重ねたアイキャッチを簡単に生成できる旨を案内する。
ユーザーが不要と判断した場合はスキップしてよい。

### 2. カテゴリ・タグの選定

記事の内容に基づいて、適切なカテゴリとタグを選定する。

1. WordPress MCP でカテゴリ一覧・タグ一覧を取得する
2. 記事の内容に合うものを選び、ユーザーに提案する
3. 適切なカテゴリ・タグが存在しない場合は、新規作成をユーザーに提案する

### 3. 記事の投稿

MCP の記事作成機能を使用して投稿する。

- ステータス: **draft**（下書き）で投稿する。公開はユーザーが手動で行う。
- カテゴリ・タグ: 下記「カテゴリ・タグの選定」で決定したものを使用する
- Markdown から Gutenberg ブロックへの変換は MCP サーバーが自動で行う
- 本文中の画像（`![alt](images/xxx.png)`）は MCP サーバーが自動でアップロード・URL置換するため、手動アップロードは不要
- アイキャッチ画像がある場合は `featured_media` に media ID を指定する

### 4. 投稿後

- ユーザーに投稿URLを伝える
- `project.yaml` の `phase` を `posted` に更新する
- `project.yaml` に `wordpress_post_id` を記録する
