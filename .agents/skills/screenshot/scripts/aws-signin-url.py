#!/usr/bin/env -S uv --quiet run --script
# /// script
# requires-python = "==3.13.*"
# dependencies = ["httpx"]
# ///
"""
AWS マネジメントコンソールのフェデレーションサインイン URL を生成する。

使い方:
    uv run .agents/skills/screenshot/scripts/aws-signin-url.py <コンソールURL> [--profile PROFILE]

例:
    uv run .agents/skills/screenshot/scripts/aws-signin-url.py "https://ap-northeast-1.console.aws.amazon.com/lambda/home"
    uv run .agents/skills/screenshot/scripts/aws-signin-url.py "https://ap-northeast-1.console.aws.amazon.com/lambda/home" --profile cb

認証方法に応じて自動で処理を切り替える:
    - SSO / AssumeRole（一時認証情報）: セッション情報をそのまま使用
    - IAM ユーザー（永続認証情報）: get-federation-token で一時認証情報を取得してから使用
"""

import argparse
import json
import subprocess
import sys
import urllib.parse

import httpx


def aws_cmd(args: list[str], *, profile: str | None = None) -> subprocess.CompletedProcess:
    """AWS CLI コマンドを実行する。profile が指定されていれば --profile を付与する。"""
    cmd = ["aws", *args]
    if profile:
        cmd.extend(["--profile", profile])
    return subprocess.run(cmd, capture_output=True, text=True)


def get_current_credentials(*, profile: str | None = None) -> dict:
    """現在の認証情報をエクスポートする。"""
    result = aws_cmd(["configure", "export-credentials"], profile=profile)
    if result.returncode != 0:
        print("エラー: 認証情報のエクスポートに失敗しました", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def get_federation_token(*, profile: str | None = None) -> dict:
    """IAM ユーザー用: get-federation-token で一時認証情報を取得する。"""
    result = aws_cmd(
        [
            "sts", "get-federation-token",
            "--name", "console-session",
            "--duration-seconds", "3600",
            "--policy", json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": "*",
                    "Resource": "*",
                }],
            }),
            "--output", "json",
        ],
        profile=profile,
    )
    if result.returncode != 0:
        print("エラー: get-federation-token に失敗しました", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)["Credentials"]


def get_signin_url(creds: dict, destination: str) -> str:
    """フェデレーションサインイン URL を生成する。"""
    session_json = json.dumps({
        "sessionId": creds["AccessKeyId"],
        "sessionKey": creds["SecretAccessKey"],
        "sessionToken": creds["SessionToken"],
    })

    token_url = (
        "https://signin.aws.amazon.com/federation"
        f"?Action=getSigninToken"
        f"&SessionDuration=3600"
        f"&Session={urllib.parse.quote(session_json)}"
    )
    resp = httpx.get(token_url)
    resp.raise_for_status()
    signin_token = resp.json()["SigninToken"]

    return (
        "https://signin.aws.amazon.com/federation"
        f"?Action=login"
        f"&Issuer="
        f"&Destination={urllib.parse.quote(destination, safe='')}"
        f"&SigninToken={signin_token}"
    )


def main():
    parser = argparse.ArgumentParser(description="AWS マネコンのフェデレーションサインイン URL を生成する")
    parser.add_argument("destination", help="開きたいコンソールページの URL")
    parser.add_argument("--profile", help="AWS CLI プロファイル名")
    args = parser.parse_args()

    # 認証状態を確認
    check = aws_cmd(["sts", "get-caller-identity"], profile=args.profile)
    if check.returncode != 0:
        print("エラー: AWS CLI が認証されていません", file=sys.stderr)
        if args.profile:
            print(f"プロファイル: {args.profile}", file=sys.stderr)
        sys.exit(1)

    identity = json.loads(check.stdout)
    print(f"認証確認: {identity['Arn']}", file=sys.stderr)

    # 現在の認証情報を取得
    exported = get_current_credentials(profile=args.profile)

    if exported.get("SessionToken"):
        # SSO / AssumeRole: セッション情報をそのまま使う
        print("認証方式: SSO / AssumeRole（一時認証情報を直接使用）", file=sys.stderr)
        creds = {
            "AccessKeyId": exported["AccessKeyId"],
            "SecretAccessKey": exported["SecretAccessKey"],
            "SessionToken": exported["SessionToken"],
        }
    else:
        # IAM ユーザー: get-federation-token で一時認証情報を取得
        print("認証方式: IAM ユーザー（get-federation-token で一時認証情報を取得）", file=sys.stderr)
        creds = get_federation_token(profile=args.profile)

    signin_url = get_signin_url(creds, args.destination)
    print(signin_url)


if __name__ == "__main__":
    main()
