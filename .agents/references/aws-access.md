# AWS CLIアクセス

aws loginで一時認証情報を使う。長期アクセスキーは使用禁止。

## 手順

以下のメッセージをそのままユーザーに提示する:

---

AWSへのアクセスが必要です。以下の手順で認証をお願いします。

1. ブラウザで目的のAWSアカウントにサインインしてください（SSO、IAMユーザーなど普段の方法で）
2. ターミナルで以下を実行してください:
   ```
   aws login --profile blog-poc-tmp --region ap-northeast-1 --remote
   ```
3. 表示されるURLをブラウザで開き、認可コードをCLIに貼り付けてください

完了したら教えてください。

---

ユーザーから完了の報告を受けたら:

1. 認証確認: `aws sts get-caller-identity --profile blog-poc-tmp`
2. 以降のコマンドは `--profile blog-poc-tmp` を付けて実行
