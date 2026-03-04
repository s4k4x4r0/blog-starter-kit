---
name: aws-drawio
description: draw.ioでAWS構成図を描く際に、公式AWSアーキテクチャアイコン（mxgraph.aws4.*シェイプ）、カラーパレット、グルーピングルールを適用する。AWSアーキテクチャ図、AWS構成図、AWSインフラ図、サーバーレス構成図、VPC構成図、AWSクラウド環境の可視化など、AWSサービスを含む図をdraw.ioで描く際は必ずこのスキルを参照すること。
allowed-tools: Bash, Write, Read, Glob, Agent
---

# AWS Architecture Diagram Skill

draw.io の mxGraphModel XML で AWS 構成図を描く際に、AWS 公式の Architecture Icons とデザインルールを適用するスキル。
XML 生成からエクスポートまでこのスキルだけで完結する。

## サービスアイコン

### なぜ AWS アイコンを使うのか

角丸ボックスに色を付けただけでは、サービスの種類が一目で判別できない。AWS 公式アイコンを使うと：
- 色でサービスカテゴリが即座に分かる（オレンジ=Compute、緑=Storage など）
- アイコンのグリフで個別サービスが識別できる
- AWS 公式ドキュメントと一貫性が保てる

### サービスアイコン vs リソースアイコンの使い分け

draw.io の AWS アイコンには 2 パターンある：

- **サービスアイコン（resourceIcon）**: サービス全体を表す。カテゴリカラーのグラデーション正方形にグリフが白で入る。**構成図ではこちらを基本にする。**
- **リソースアイコン（直接シェイプ）**: サービス内の個別リソースを表す。グリフのみのアイコン。同じサービスの複数インスタンスを区別する場合に使う。

### サービスアイコンの XML テンプレート

`resourceIcon` + `resIcon` パターン：

```xml
<mxCell id="<UNIQUE_ID>" value="<サービス名>"
  style="sketch=0;outlineConnect=0;fontColor=#232F3E;
    gradientColor=<GRADIENT>;gradientDirection=north;
    fillColor=<FILL>;strokeColor=#ffffff;dashed=0;
    verticalLabelPosition=bottom;verticalAlign=top;
    align=center;html=1;fontSize=12;fontStyle=0;
    aspect=fixed;shape=mxgraph.aws4.resourceIcon;
    resIcon=mxgraph.aws4.<SERVICE>;"
  vertex="1" parent="<PARENT_ID>">
  <mxGeometry x="<X>" y="<Y>" width="48" height="48" as="geometry"/>
</mxCell>
```

注意点：
- `strokeColor=#ffffff` はアイコングリフを白で描画するために必須。省略するとグリフが見えなくなる
- `aspect=fixed` でアイコンの縦横比を保持
- `verticalLabelPosition=bottom` でラベルをアイコンの下に配置（AWS の慣例）
- 推奨サイズ: 48x48
- ID は図全体で一意にすること。グループの parent 属性には、そのグループの mxCell id を正確に指定すること

### リソースアイコン（直接シェイプ）の XML テンプレート

`shape=mxgraph.aws4.<NAME>` パターン（resourceIcon は使わない）：

```xml
<mxCell id="<UNIQUE_ID>" value="<リソース名>"
  style="sketch=0;outlineConnect=0;fontColor=#232F3E;
    gradientColor=none;fillColor=<CATEGORY_COLOR>;strokeColor=none;
    dashed=0;verticalLabelPosition=bottom;verticalAlign=top;
    align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;
    pointerEvents=1;shape=mxgraph.aws4.<NAME>;"
  vertex="1" parent="<PARENT_ID>">
  <mxGeometry x="<X>" y="<Y>" width="48" height="48" as="geometry"/>
</mxCell>
```

主な直接シェイプ：

| リソース | shape値 | fillColor |
|----------|---------|-----------|
| Users（人物） | `mxgraph.aws4.users` | `#232F3E` |
| Client（PC） | `mxgraph.aws4.client` | `#232F3E` |
| Internet | `mxgraph.aws4.internet` | `#8C4FFF` |
| Internet Gateway | `mxgraph.aws4.internet_gateway` | `#8C4FFF` |
| NAT Gateway | `mxgraph.aws4.nat_gateway` | `#8C4FFF` |
| Lambda Function | `mxgraph.aws4.lambda_function` | `#ED7100` |
| S3 Bucket | `mxgraph.aws4.bucket_with_objects` | `#7AA116` |
| ALB | `mxgraph.aws4.application_load_balancer` | `#8C4FFF` |
| NLB | `mxgraph.aws4.network_load_balancer` | `#8C4FFF` |

### 頻出サービス早見表

`resIcon` の値は `mxgraph.aws4.` を省略して記載。

| カテゴリ | サービス | resIcon | fillColor | gradientColor |
|---------|---------|---------|-----------|---------------|
| Compute | Lambda | `lambda` | `#D05C17` | `#F78E04` |
| Compute | EC2 | `ec2` | `#D05C17` | `#F78E04` |
| Compute | ECS | `ecs` | `#D05C17` | `#F78E04` |
| Compute | Fargate | `fargate` | `#D05C17` | `#F78E04` |
| Networking | CloudFront | `cloudfront` | `#5A30B5` | `#945DF2` |
| Networking | ELB | `elastic_load_balancing` | `#5A30B5` | `#945DF2` |
| Networking | Route 53 | `route_53` | `#5A30B5` | `#945DF2` |
| Integration | API Gateway | `api_gateway` | `#BC1356` | `#FF4F8B` |
| Integration | SQS | `sqs` | `#BC1356` | `#FF4F8B` |
| Integration | SNS | `sns` | `#BC1356` | `#FF4F8B` |
| Integration | Step Functions | `step_functions` | `#BC1356` | `#FF4F8B` |
| Integration | EventBridge | `eventbridge` | `#BC1356` | `#FF4F8B` |
| Storage | S3 | `s3` | `#277116` | `#60A337` |
| Database | DynamoDB | `dynamodb` | `#3334B9` | `#4D72F3` |
| Database | RDS | `rds` | `#3334B9` | `#4D72F3` |
| Database | Aurora | `aurora` | `#3334B9` | `#4D72F3` |
| Database | ElastiCache | `elasticache` | `#3334B9` | `#4D72F3` |
| Security | Cognito | `cognito` | `#C7131F` | `#F54749` |
| Security | IAM | `identity_and_access_management` | `#C7131F` | `#F54749` |
| Security | WAF | `waf` | `#C7131F` | `#F54749` |
| Monitoring | CloudWatch | `cloudwatch_2` | `#BC1356` | `#FF4F8B` |

> 完全なサービス一覧は `references/aws-service-icons.md` を参照

## カラーについて

### AWS 公式パレットと draw.io アイコンカラーの関係

AWS には 2 つの色体系がある。混同しないこと。

**公式パレット**（ブランドカラー）— グループ境界、直接シェイプの fillColor、ラベルに使う：

| 名前 | Hex | 対象カテゴリ |
|------|-----|------------|
| **Squid** | `#232F3E` | テキスト、AWS Cloud 境界 |
| **Smile** | `#ED7100` | Compute, Containers |
| **Endor** | `#7AA116` | Storage |
| **Galaxy** | `#8C4FFF` | Networking, Analytics, Dev Tools |
| **Cosmos** | `#E7157B` | App Integration, Management |
| **Mars** | `#DD344C` | Security |
| **Orbit** | `#01A88D` | ML |

**draw.io アイコンカラー**（グラデーション用）— サービスアイコン（resourceIcon）の fillColor/gradientColor に使う。パレットより暗い色をベースに、明るい色へグラデーションする。上の「頻出サービス早見表」の値をそのまま使うこと。

矢印の色はグレー系（`#545B64` 推奨）を使い、サービスカラーと混同しないようにする。

## グルーピング（境界ボックス）

### なぜグルーピングが必要か

サービスアイコンを並べるだけでは、スコープが伝わらない。グルーピングにより：
- **セキュリティ境界**: VPC、サブネットの範囲が明確になる
- **障害ドメイン**: AZ の冗長構成が伝わる
- **スコープ**: S3（グローバル）は VPC の外、RDS は VPC 内

### グループの階層

```
AWS Cloud
  └── Region（単一リージョンなら省略可）
       └── VPC
            └── Availability Zone
                 └── Subnet (Public / Private)
```

不要なグルーピングは省略する。シンプルさが重要。
- 全サービスが単一リージョン → Region ボックスは不要
- VPC を使わないサーバーレス構成 → VPC ボックスは不要
- サーバーレス構成では AWS Cloud ボックスだけで十分なことが多い

### グループの XML テンプレート

```xml
<mxCell id="<UNIQUE_ID>" value="<グループ名>"
  style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],
    [1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],
    [0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
    outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;
    fontSize=12;fontStyle=0;container=1;pointerEvents=0;
    collapsible=0;recursiveResize=0;
    shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<GROUP_ICON>;
    strokeColor=<STROKE>;fillColor=<FILL>;
    verticalAlign=top;align=left;spacingLeft=30;
    fontColor=<FONT>;dashed=<0or1>;"
  vertex="1" parent="<PARENT_ID>">
  <mxGeometry x="<X>" y="<Y>" width="<W>" height="<H>" as="geometry"/>
</mxCell>
```

`container=1` は必須。子要素は `parent="<GROUP_ID>"` で参照する。
子要素の座標は親グループの左上からの相対位置。子要素の座標 + サイズが親の width/height を超えないこと。

### 主要グループ定義

| グループ | grIcon | strokeColor | fillColor | fontColor | dashed |
|---------|--------|-------------|-----------|-----------|--------|
| AWS Cloud | `group_aws_cloud_alt` | `#232F3E` | `none` | `#232F3E` | 0 |
| Region | `group_region` | `#00A4A6` | `none` | `#00A4A6` | 1 |
| VPC | `group_vpc2` | `#8C4FFF` | `none` | `#8C4FFF` | 0 |
| AZ | `group_availability_zone` | `#147EBA` | `none` | `#147EBA` | 1 |
| Public Subnet | `group_security_group` | `#7AA116` | `#F2F6E8` | `#248814` | 0 |
| Private Subnet | `group_security_group` | `#147EBA` | `#E6F2F8` | `#147EBA` | 0 |
| Security Group | `group_security_group` | `#DD344C` | `none` | `#DD344C` | 0 |

> 完全なグループ定義と入れ子の例は `references/aws-groups.md` を参照

## レイアウトのベストプラクティス

### フロー
- 左→右 または 上→下 の一方向フローを徹底する
- 1 つの図で 1〜2 の主要フローに絞る

### アイコン配置
- アイコンサイズは 48x48 で統一
- アイコン間の間隔は 140〜200px（矢印とラベルの余白を確保）
- サービスのスコープを意識して配置する：
  - **グローバル**（CloudFront, Route 53, S3）→ VPC の外
  - **リージョナル**（Lambda, API Gateway, DynamoDB）→ Region / AWS Cloud 内
  - **VPC スコープ**（EC2, RDS, ELB, ECS）→ VPC / Subnet 内

### 矢印

主要フロー（実線）：
```xml
<mxCell id="<UNIQUE_ID>" value="<ラベル>"
  style="edgeStyle=orthogonalEdgeStyle;html=1;
    strokeColor=#545B64;strokeWidth=2;fontSize=10;fontColor=#545B64;"
  edge="1" source="<SOURCE_ID>" target="<TARGET_ID>" parent="<PARENT_ID>">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

二次フロー（破線 — レスポンス、監視ログ等）：
```xml
<mxCell id="<UNIQUE_ID>" value="<ラベル>"
  style="edgeStyle=orthogonalEdgeStyle;html=1;
    strokeColor=#545B64;strokeWidth=1;dashed=1;fontSize=10;fontColor=#545B64;"
  edge="1" source="<SOURCE_ID>" target="<TARGET_ID>" parent="<PARENT_ID>">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

ラベルは動詞で短く（"invoke", "query", "trigger" など）。

### グループの padding
- グループ境界からアイコンまで最低 40px の余白を確保
- グループ名のテキスト分、上部に 30px 追加

## よくある構成パターン

### サーバーレス Web アプリケーション
```
[AWS Cloud]
  Users → CloudFront → S3 (Static)
  Users → Cognito → API Gateway → Lambda → DynamoDB
```
VPC 不要。AWS Cloud ボックスのみ。

### VPC 3 層アーキテクチャ
```
[AWS Cloud]
  [VPC]
    [Public Subnet AZ-a]  [Public Subnet AZ-c]
      ALB                   ALB
    [Private Subnet AZ-a] [Private Subnet AZ-c]
      ECS                   ECS
    [Private Subnet AZ-a] [Private Subnet AZ-c]
      RDS (Primary)         RDS (Standby)
```

### イベント駆動パイプライン
```
[AWS Cloud]
  S3 → Lambda → SQS → Lambda → DynamoDB
                                  ↓
                                SNS → (通知)
```

## 生成フロー

### 1. XML 生成

このスキルの指示に従って .drawio ファイルを生成する。

**XML 基本構造:**
```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- 図の要素は parent="1" で配置 -->
  </root>
</mxGraphModel>
```

**XML の注意事項:**
- XML コメント内で `--` を使わないこと（XML 仕様違反でパースエラーになる）
- 属性値の特殊文字はエスケープ: `&amp;`, `&lt;`, `&gt;`, `&quot;`
- 全 mxCell の `id` は図全体で一意にすること

**ファイル命名:** 小文字ハイフン区切りの説明的な名前（例: `web-system.drawio`）

### 2. PNG エクスポート

draw.io CLI でエクスポートする。CLI が利用できない場合は .drawio ファイルを生成して完了。

```bash
# CLI の確認（drawio が PATH になければ /Applications/draw.io.app/Contents/MacOS/draw.io を使う）
which drawio

# エクスポート（-e は使わない。drawio の -e オプションは PNG に XML を埋め込むが、
# 生成される zTXt チャンクの CRC が不正で Claude API が画像を処理できなくなるため）
drawio -x -f png -b 10 -o <出力>.drawio.png <入力>.drawio

# 結果を開く
open <出力>.drawio.png
```

エクスポート後も `.drawio` ファイルは削除しない（後から修正できるように残す）。

### 3. ユーザー確認（セルフチェックは行わない）

PNG エクスポートまでが必須フロー。エクスポート後の自動レビュー（PNG を Read して確認）は行わない。
ユーザーが PNG を確認し、修正指示があった場合にのみ XML を修正して再エクスポートする。

## リファレンスファイル

上記の早見表にないサービスや、より複雑なグルーピングが必要な場合：

- `references/aws-service-icons.md` — 全 AWS サービスの resIcon、fillColor、gradientColor 一覧（カテゴリ別）
- `references/aws-groups.md` — グループコンテナの完全なスタイル定義、入れ子 XML の実例
