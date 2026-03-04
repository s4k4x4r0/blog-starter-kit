# agent-browser セットアップガイド

agent-browser が使えない場合、以下の手順をユーザーに案内してください。

## 1. agent-browser のインストール

```bash
npm install -g agent-browser
agent-browser install
```

`npx` で都度実行する場合はグローバルインストール不要です:

```bash
npx agent-browser open "https://example.com"
npx agent-browser screenshot example.png
```

## 2. スキルのインストール

```bash
npx skills add vercel-labs/agent-browser --skill agent-browser --agent claude-code cursor --yes
```

## 3. 動作確認

ブラウザを開いてスクリーンショットが撮れることを確認する:

```bash
agent-browser open "https://example.com"
agent-browser screenshot test.png
```

## 参考

- リポジトリ: https://github.com/vercel-labs/agent-browser
