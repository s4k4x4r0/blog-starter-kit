# AWS マネジメントコンソールのスクリーンショット

AWS マネコンは認証が必要なため、フェデレーションサインイン URL を生成してからブラウザでアクセスする。

## 前提

- AWS CLI が認証済みの状態であること（認証方法は問わない）
- agent-browser がセットアップ済みであること
- `uv` がインストール済みであること

## 手順

### 1. フェデレーションサインイン URL の生成

```bash
SIGNIN_URL=$(uv run .agents/skills/screenshot/scripts/aws-signin-url.py "<コンソールURL>" [--profile PROFILE])
```

例（Lambda コンソール）:
```bash
# デフォルトの認証情報を使う場合
SIGNIN_URL=$(uv run .agents/skills/screenshot/scripts/aws-signin-url.py "https://ap-northeast-1.console.aws.amazon.com/lambda/home")

# プロファイルを指定する場合
SIGNIN_URL=$(uv run .agents/skills/screenshot/scripts/aws-signin-url.py "https://ap-northeast-1.console.aws.amazon.com/lambda/home" --profile my-dev)
```

ユーザーが AWS プロファイルを使い分けている場合は、どのプロファイルを使うか確認すること。

エラーが出た場合はユーザーに認証情報の設定を依頼すること。

### 2. ブラウザで開いてスクリーンショットを撮る

```bash
agent-browser open "$SIGNIN_URL"
# ページの読み込みを待つ
sleep 5
agent-browser screenshot /tmp/<説明的な名前>.png
agent-browser close
```

ページの読み込みに時間がかかる場合は `sleep` の秒数を増やす。
撮影後は SKILL.md のステップ 3〜6（内容確認、機密情報チェック、保存、記録）に従う。

## 注意事項

- フェデレーション URL は一度しか使えない。再撮影が必要な場合はスクリプトを再実行する
- セッションの有効期限はデフォルト 3600 秒（1時間）

## トラブルシューティング

| 問題 | 原因 | 対処 |
|---|---|---|
| `AWS CLI が認証されていません` | 認証情報が未設定 | ユーザーに認証情報の設定を依頼 |
| ページが真っ白 | 読み込み待ち不足 | `sleep` を長くして再撮影 |
| リダイレクトでサインインページに戻る | URL の有効期限切れ | スクリプトを再実行 |
