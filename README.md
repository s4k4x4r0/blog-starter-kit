# cb-blog-template

技術ブログの検証と執筆を行うためのテンプレートリポジトリです。

## 前提

- **Node.js** — WordPress MCP サーバーの実行に必要
- **uv** — アイキャッチ画像生成スクリプト等の Python ツール実行に必要（https://docs.astral.sh/uv/）

## セットアップ

1. GitHub で「Use this template」からリポジトリを作成し、clone する
2. WordPress のアプリケーションパスワードを発行する（詳細は `.agents/skills/cb-blog/references/mcp-setup.md`）
3. `.env` ファイルを作成する:
   ```bash
   cp .env.example .env
   ```
   `.env` に WordPress の認証情報を記入する
4. エディタを再起動する（Claude Code: ターミナル再起動、Cursor: アプリ再起動）

### Windows の場合

`.claude/skills` は `.agents/skills` へのシンボリックリンクです。
Windows 環境ではシンボリックリンクが正しく展開されない場合があります。
その場合は以下のいずれかで対応してください:

- WSL2 上で作業する（推奨）
- `.claude/skills/` を削除し、`.agents/skills/` の内容をコピーする

## 使い方

Claude Code または Cursor で `/cb-blog` スキルを使います。

```
/cb-blog ネタを相談したい。〇〇について
/cb-blog 検証計画を立てたい
/cb-blog 記事を書いて
/cb-blog WordPressに投稿して
```

## ディレクトリ構造

```
project.yaml                  # プロジェクトのメタデータ・状態管理
NOTES.md                      # 検証ノート（全ての記録を集約）
AGENTS.md                     # AIエージェントへの共通ルール
CLAUDE.md                     # Claude Code 用（AGENTS.mdをインポート）
poc/                           # 検証コード
blog/                          # ブログ記事
  <article-id>/
    draft.md                   # 記事の下書き
    images/                    # 記事用の画像
.mcp.json                      # Claude Code用MCP設定
.agents/skills/cb-blog/        # ブログ執筆スキル（Cursor はここを直接読む）
.agents/skills/eyecatch/       # アイキャッチ画像生成スキル
.claude/skills -> .agents/skills  # Claude Code 用シンボリックリンク
.cursor/
  mcp.json                     # Cursor用MCP設定
```

## ワークフロー

```
idea -> poc -> draft -> posted
```

1. **idea**: 記事のアイデアを練る
2. **poc**: 技術検証を実施する（検証結果は NOTES.md に記録される）
3. **draft**: 検証結果からブログ記事を書く
4. **posted**: WordPressに下書き投稿する（以降のレビュー・公開はWordPress側で行う）
