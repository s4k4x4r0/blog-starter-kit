# AWS Groups Reference

draw.io の mxGraphModel XML で使用する AWS グループ（境界ボックス）の詳細定義。

## グループスタイルテンプレート

すべてのグループは以下のスタイルテンプレートに従う：

```
points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],
  [1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],
  [0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];
outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;
fontSize=12;fontStyle=0;container=1;pointerEvents=0;
collapsible=0;recursiveResize=0;
shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.<GROUP_ICON>;
strokeColor=<STROKE>;fillColor=<FILL>;
verticalAlign=top;align=left;spacingLeft=30;
fontColor=<FONT>;dashed=0;
```

`container=1` は必須。子要素は `parent="<GROUP_ID>"` で参照する。

## グループ定義一覧

| グループ | grIcon | strokeColor | fillColor | fontColor | dashed |
|---------|--------|-------------|-----------|-----------|--------|
| AWS Cloud | `group_aws_cloud_alt` | `#232F3E` | `none` | `#232F3E` | 0 |
| AWS Account | `group_account` | `#CD2264` | `none` | `#CD2264` | 0 |
| Region | `group_region` | `#00A4A6` | `none` | `#00A4A6` | 1 |
| VPC | `group_vpc2` | `#8C4FFF` | `none` | `#8C4FFF` | 0 |
| Availability Zone | `group_availability_zone` | `#147EBA` | `none` | `#147EBA` | 1 |
| Public Subnet | `group_security_group` | `#7AA116` | `#F2F6E8` | `#248814` | 0 |
| Private Subnet | `group_security_group` | `#147EBA` | `#E6F2F8` | `#147EBA` | 0 |
| Security Group | `group_security_group` | `#DD344C` | `none` | `#DD344C` | 0 |
| Auto Scaling Group | `group_autoScaling` | `#ED7100` | `none` | `#ED7100` | 0 |
| Corporate Data Center | `group_corporate_data_center` | `#147EBA` | `none` | `#147EBA` | 0 |

## サブネットの色分けルール

サブネットの色は通信経路を視覚的に伝える重要な要素：

- **Public Subnet** (緑系): インターネットからの直接アクセスがある
  - 背景: `#F2F6E8`（薄い緑）、枠線: `#7AA116`
  - 配置するもの: ALB, NAT Gateway, Bastion Host

- **Private Subnet** (青系): インターネットからの直接アクセスがない
  - 背景: `#E6F2F8`（薄い青）、枠線: `#147EBA`
  - 配置するもの: EC2, ECS, RDS, ElastiCache

## 入れ子 XML の実例

VPC 内にマルチ AZ の Public/Private Subnet を配置する例：

```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>

    <!-- AWS Cloud -->
    <mxCell id="aws" value="AWS Cloud" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;" vertex="1" parent="1">
      <mxGeometry x="40" y="40" width="800" height="500" as="geometry"/>
    </mxCell>

    <!-- VPC (AWS Cloud の子) -->
    <mxCell id="vpc" value="VPC (10.0.0.0/16)" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#8C4FFF;dashed=0;" vertex="1" parent="aws">
      <mxGeometry x="20" y="40" width="760" height="440" as="geometry"/>
    </mxCell>

    <!-- AZ-a (VPC の子) -->
    <mxCell id="az-a" value="AZ-a" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_availability_zone;strokeColor=#147EBA;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;" vertex="1" parent="vpc">
      <mxGeometry x="20" y="40" width="350" height="380" as="geometry"/>
    </mxCell>

    <!-- Public Subnet (AZ-a の子) -->
    <mxCell id="pub-a" value="Public Subnet" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#7AA116;fillColor=#F2F6E8;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;" vertex="1" parent="az-a">
      <mxGeometry x="20" y="40" width="310" height="150" as="geometry"/>
    </mxCell>

    <!-- Private Subnet (AZ-a の子) -->
    <mxCell id="priv-a" value="Private Subnet" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;strokeColor=#147EBA;fillColor=#E6F2F8;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;" vertex="1" parent="az-a">
      <mxGeometry x="20" y="210" width="310" height="150" as="geometry"/>
    </mxCell>

    <!-- ALB (Public Subnet の子) -->
    <mxCell id="alb" value="ALB" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;fillColor=#8C4FFF;strokeColor=none;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.application_load_balancer;" vertex="1" parent="pub-a">
      <mxGeometry x="131" y="51" width="48" height="48" as="geometry"/>
    </mxCell>

    <!-- ECS (Private Subnet の子) -->
    <mxCell id="ecs" value="ECS" style="sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=#F78E04;gradientDirection=north;fillColor=#D05C17;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ecs;" vertex="1" parent="priv-a">
      <mxGeometry x="131" y="51" width="48" height="48" as="geometry"/>
    </mxCell>

  </root>
</mxGraphModel>
```

ポイント:
- `parent` 属性でグループの入れ子を表現する（`aws` → `vpc` → `az-a` → `pub-a` → `alb`）
- 子要素の座標は親グループの左上からの相対位置
- 各グループに十分な padding を確保する

## サービスの配置スコープ

どのサービスをどのグループに配置するかのガイド：

### AWS Cloud 直下（VPC の外）
- CloudFront, Route 53, S3, DynamoDB, Lambda, API Gateway
- Cognito, IAM, CloudWatch, SQS, SNS, Step Functions
- (サーバーレスサービスは VPC の外に配置)

### VPC 内（Subnet に配置）
- **Public Subnet**: ALB, NLB, NAT Gateway, Bastion Host
- **Private Subnet**: EC2, ECS, EKS, RDS, Aurora, ElastiCache, Redshift

### VPC の外、AWS Cloud 内
- Internet Gateway（VPC 境界上に配置することが多い）
- Transit Gateway, Direct Connect
