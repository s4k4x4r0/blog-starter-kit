# アイデア・企画フェーズ

## やること

1. ユーザーのアイデアを聞き、壁打ち相手として議論する
2. 以下の観点で記事の方向性を整理する:
   - 読者は誰か（初心者向け？経験者向け？）
   - 記事のゴール（何ができるようになる？）
   - 差別化ポイント（既存記事との違いは？）
   - 検証で確認すべきこと
3. 議論の結果を `project.yaml` に反映する
4. 必要に応じて `blog/` に記事ディレクトリを作成する

## project.yaml の更新例

```yaml
articles:
  - id: 01-getting-started
    title: "記事タイトル"
    phase: idea
    tags: [タグ1, タグ2]
```

## 記事ディレクトリの作成

```
blog/<article-id>/
├── draft.md
└── images/
```

`draft.md` は [templates/draft.md](../templates/draft.md) をコピーして作成してください。

## phase の更新

企画がまとまったら `phase: idea` → `phase: poc` に更新してください。
