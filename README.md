# cb-blog-template

AIエージェントと対話するだけで、技術ブログの企画から WordPress 投稿までできるテンプレートリポジトリです。

## 会話イメージ

```
👤 Lambda の Durable Functions が気になってる

🤖 どのような記事にしたいですか？
   検証したいこと、興味があること、何でも自由に教えてください。
   それをもとに、私が読者ターゲット・記事のゴール・差別化ポイント・
   検証で確認すべきことを整理します。

👤 Step Functions 使ってる人が「これ Lambda だけでできるんだ」ってなる記事がいいな

🤖 企画を整理しました。
   - 読者ターゲット: AWS で Step Functions を使っているエンジニア
   - 記事のゴール: Durable Functions で同等のワークフローが組めるか判断できる
   - 差別化ポイント: 同じワークフローを両方で実装し比較する
   - 検証で確認すべきこと: タスクチェイン・エラーハンドリング・コスト
   この企画案でいかがでしょうか？
   よければ、次は検証計画を決めていきます。

👤 いいね、進めて

   ... 検証計画の策定 → PoC 実行 → 記事執筆 → WordPress 投稿 ...

🤖 投稿しました。
   - 投稿URL: https://example.com/?p=1234
   - ステータス: 下書き（公開は WordPress 管理画面から行ってください）
```

エージェントが企画・検証・執筆・投稿の各フェーズを主導し、次に何をすべきかを案内します。あなたはアイデアを話して、フィードバックするだけ。

## セットアップ

1. GitHub で「Use this template」からリポジトリを作成し、clone する
2. WordPress のアプリケーションパスワードを発行する（詳細は `.agents/references/mcp-setup.md`）
3. `.env` ファイルを作成する:
   ```bash
   cp .env.example .env
   ```
   `.env` に WordPress の認証情報を記入する
4. Node 依存をインストールする（**Dev Container を使う場合はこの手順は自動実行されるため不要**）:
   ```bash
   corepack enable      # pnpm を有効化（バージョンは package.json の packageManager で固定）
   pnpm install --frozen-lockfile
   pnpm exec playwright install chromium
   ```
5. エディタを再起動する（Claude Code: ターミナル再起動、Cursor: アプリ再起動）

## 推奨環境

Dev Containerを使用することを推奨します。
Dev Containerならば、以下のツールが自動でインストールされます。

- **Node.js + pnpm** — WordPress MCP サーバーの実行や Node ツール（textlint・agent-browser 等）に必要。Node パッケージは `package.json` / `pnpm-lock.yaml` でプロジェクトローカルに固定管理する
- **uv** — アイキャッチ画像生成スクリプト等の Python ツール実行に必要（https://docs.astral.sh/uv/）
- **agent-browser** (推奨) — ブラウザのスクリーンショット撮影に使用。pnpm でローカル導入される（https://github.com/vercel-labs/agent-browser）

## Windows の場合

LinuxやMacを想定しています。
Windowsの場合、次の環境を利用することを推奨します。

- Dev Container
- WSL2
