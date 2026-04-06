# エージェント共通ルール

このリポジトリは技術ブログの検証と執筆を行うプロジェクトです。

## プロジェクト構造

```
project.yaml    # プロジェクトのメタデータ・状態管理
NOTES.md        # 検証ノート（全ての記録はここに集約）
poc/            # 検証コード
blog/           # ブログ記事（記事ごとにサブディレクトリ）
```

## セッション開始時

1. `project.yaml` で現在のフェーズと記事の状態を把握する
2. `NOTES.md` で検証の進捗と方針を把握する
3. `poc/` のコードで検証の現状を把握する

## ワークフロー

記事の状態は `project.yaml` の `phase` で管理します。ユーザーの意図と現在の phase に応じて、適切なアクションを実行してください。判断に迷ったらユーザーに確認してください。

| ユーザーの意図 | 参照ファイル | phase 遷移 |
|---|---|---|
| ネタ相談、アイデア出し、方向性の議論 | [ideation.md](.agents/references/ideation.md) | → `idea` → `poc` |
| 検証計画、PoC設計 | [poc-planning.md](.agents/references/poc-planning.md) | `poc` のまま |
| 記事を書く、下書き作成 | [writing.md](.agents/references/writing.md) | → `draft` |
| WordPressに投稿 | [publishing.md](.agents/references/publishing.md) | → `posted` |

phase の遷移: `idea → poc → draft → posted`

## NOTES.md の記録

NOTES.md はこのプロジェクトの最重要ドキュメントです。書き方の詳細は [notes-guide.md](.agents/references/notes-guide.md) を参照してください。

**必ず守ること:**

- **メインエージェントだけが NOTES.md を書く**（サブエージェントは結果を返すのみ）
- **こまめに書く** — ディスカッションで決定したらすぐ、検証結果が出たらすぐ記録する
- **調査セクションは確定事実として維持する** — 後で訂正が見つかったら元の記述を更新する

## AWS CLIアクセス

`aws` コマンドを実行する前に、必ず [aws-access.md](.agents/references/aws-access.md) の手順でユーザーに認証してもらうこと。このプロジェクトでは長期アクセスキーを使わず、`aws login` による一時認証情報のみを使用する。

## コミットルール

- 検証コードのコミットは通常通り行う
- `NOTES.md` と `project.yaml` の更新もコミットに含める
- コミット前に `.git/hooks/pre-commit` が存在するか確認し、なければ `pre-commit install` を実行する（gitleaks によるシークレット漏洩防止）
