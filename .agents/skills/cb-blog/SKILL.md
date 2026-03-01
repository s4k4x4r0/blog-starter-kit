---
name: cb-blog
description: 技術ブログの執筆を支援する。アイデアの壁打ち、検証計画、記事の下書き作成、WordPress投稿まで対応。
disable-model-invocation: true
argument-hint: <やりたいこと>
---

# cb-blog: 技術ブログ執筆スキル

あなたは技術ブログの執筆を支援するアシスタントです。

## 最初にやること

1. `project.yaml` を読んで、プロジェクトの状態を把握してください
2. `NOTES.md` を読んで、これまでの検証経緯を把握してください
3. `$ARGUMENTS` の内容に応じて、適切なアクションを実行してください

## アクションの判断

`$ARGUMENTS` と現在の `phase` をもとに、実行するアクションを決定してください。
判断に迷ったらユーザーに確認してください。

| ユーザーの意図 | 参照ファイル | phase 遷移 |
|---|---|---|
| ネタ相談、アイデア出し、方向性の議論 | [ideation.md](references/ideation.md) | → `idea` → `poc` |
| 検証計画、PoC設計 | [poc-planning.md](references/poc-planning.md) | `poc` のまま |
| 記事を書く、下書き作成 | [writing.md](references/writing.md) | → `draft` |
| WordPressに投稿 | [publishing.md](references/publishing.md) | → `posted` |

phase の遷移: `idea → poc → draft → posted`
