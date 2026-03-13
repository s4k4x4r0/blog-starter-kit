# WordPress MCP セットアップガイド

WordPress MCP ツールが使えない場合、以下の手順をユーザーに案内してください。

## 1. WordPress アプリケーションパスワードの発行

WordPress 管理画面でアプリケーションパスワードを発行する必要があります:

1. WordPress 管理画面にログイン
2. 「ユーザー」→ 自分のプロフィール
3. 「アプリケーションパスワード」セクションで新しいパスワードを発行
4. 発行されたパスワードを控える（再表示できません）

## 2. .env ファイルの作成

プロジェクトルートの `.env.example` をコピーして `.env` を作成し、認証情報を記入してもらう:

```bash
cp .env.example .env
```

`.env` の内容:

```
WORDPRESS_USERNAME=<WordPressのユーザー名>
WORDPRESS_APP_PASSWORD=<発行したアプリケーションパスワード>
```

`.env` は `.gitignore` に含まれているため、リポジトリにコミットされません。

## 3. エディタの再起動

MCP設定を反映するため、使用しているエディタを再起動してもらう:

- **Claude Code**: ターミナルを閉じて再度 `claude` を起動
- **Cursor**: Cursor を完全に終了して再起動

## 参考

- MCP サーバーのリポジトリ: https://github.com/cloudbuilders-jp/mcp-wordpress-server
