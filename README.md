# cb-blog-template

技術ブログの検証と執筆を行うためのテンプレートリポジトリです。

## 使い方

1. このテンプレートからリポジトリを作成する
2. MCP設定を更新する（`.mcp.json` と `.cursor/mcp.json`）
3. Claude Code または Cursor で `/cb-blog` スキルを使う

## スキルの使い方

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
.agents/skills/cb-blog/        # ブログ執筆スキル
.claude/skills -> .agents/skills  # Claude Code用シンボリックリンク
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
