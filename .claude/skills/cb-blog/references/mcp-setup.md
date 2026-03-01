# WordPress MCP セットアップガイド

WordPress MCP ツールが使えない場合、以下の手順をユーザーに案内してください。

## 1. WordPress アプリケーションパスワードの発行

WordPress 管理画面でアプリケーションパスワードを発行する必要があります:

1. WordPress 管理画面にログイン
2. 「ユーザー」→ 自分のプロフィール
3. 「アプリケーションパスワード」セクションで新しいパスワードを発行
4. 発行されたパスワードを控える（再表示できません）

## 2. 環境変数の設定

以下の環境変数をシェルの設定ファイル（`~/.zshrc` 等）に追加してもらう:

```bash
export WORDPRESS_USERNAME="<WordPressのユーザー名>"
export WORDPRESS_APP_PASSWORD="<発行したアプリケーションパスワード>"
```

設定後、シェルを再起動するか `source ~/.zshrc` を実行してもらう。

## 3. エディタの再起動

環境変数を反映するため、使用しているエディタを完全に再起動してもらう:

- **Claude Code**: ターミナルを閉じて再度 `claude` を起動
- **Cursor**: Cursor を完全に終了して再起動

## 参考

- MCP サーバーのリポジトリ: https://github.com/cloudbuilders-jp/mcp-wordpress-server
