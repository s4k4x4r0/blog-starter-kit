# エージェント共通ルール

このリポジトリは技術ブログの検証と執筆を行うプロジェクトです。

## プロジェクト構造

```
project.yaml    # プロジェクトのメタデータ・状態管理
NOTES.md        # 検証ノート（全ての記録はここに集約）
poc/            # 検証コード
blog/           # ブログ記事（記事ごとにサブディレクトリ）
```

## ワークフロー

記事の状態は `project.yaml` の `phase` で管理します。

**セッション開始時は、必ず以下を行うこと:**

1. `project.yaml` で現在の phase を確認する
2. 対応するリファレンスファイルを読み込む
3. リファレンスに定義されたフローに従ってユーザーを案内する

### phase とリファレンス

| phase | リファレンス |
|---|---|
| (記事なし) | [ideation.md](.agents/references/ideation.md) |
| `idea_completed` | [poc.md](.agents/references/poc.md) |
| `poc_completed` | [writing.md](.agents/references/writing.md) |
| `draft_completed` | [publishing.md](.agents/references/publishing.md) |
| `posted` | — 投稿済み。修正や新しい記事の作成に対応する |

```
(記事なし) → idea_completed → poc_completed → draft_completed → posted
```

**リファレンスにはフローの各ステップ、ユーザーへの案内テンプレート、phase 遷移条件が定義されている。エージェントはリファレンスのフローに従ってユーザーを主導すること。** ユーザーの指示を待つのではなく、次に何をすべきかをエージェントから提示する。

### ユーザーが別の作業を望む場合

ユーザーが現在の phase と異なる作業を指示した場合（例: 検証中だが先に記事を書きたい）、そのまま対応してよい。phase の順序は目安であり、厳密に守る必要はない。

## NOTES.md の記録

NOTES.md はこのプロジェクトの最重要ドキュメントです。書き方の詳細は [notes-guide.md](.agents/references/notes-guide.md) を参照してください。

**必ず守ること:**

- **メインエージェントだけが NOTES.md を書く**（サブエージェントは結果を返すのみ）
- **こまめに書く** — ディスカッションで決定したらすぐ、検証結果が出たらすぐ記録する
- **調査セクションは確定事実として維持する** — 後で訂正が見つかったら元の記述を更新する

## コミット

**エージェントはユーザーの指示を待たず、適切なタイミングで能動的にコミットすること。**

### タイミング

以下のタイミングでコミットする:

- NOTES.md や project.yaml に記録を書き込んだとき
- 検証で TODO を1つ完了したとき
- 下書きの作成・修正が一区切りついたとき
- phase を更新したとき

迷ったら細かくコミットする方を選ぶ。作業が失われるリスクを最小化する。

### ルール

- `NOTES.md` と `project.yaml` の変更は関連するコードと一緒にコミットする
- コミット前に `.git/hooks/pre-commit` が存在するか確認し、なければ `pre-commit install` を実行する（gitleaks によるシークレット漏洩防止）
