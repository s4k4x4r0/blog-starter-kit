# AWS Service Icons Reference

draw.io の mxGraphModel XML で使用する AWS サービスアイコンの完全なリスト。

すべてのサービスアイコンは以下のスタイルテンプレートに従う：
```
sketch=0;outlineConnect=0;fontColor=#232F3E;
gradientColor=<GRADIENT>;gradientDirection=north;
fillColor=<FILL>;strokeColor=#ffffff;dashed=0;
verticalLabelPosition=bottom;verticalAlign=top;
align=center;html=1;fontSize=12;fontStyle=0;
aspect=fixed;shape=mxgraph.aws4.resourceIcon;
resIcon=mxgraph.aws4.<SERVICE>;
```

`resIcon` 列の値は `mxgraph.aws4.` プレフィックスを省略して記載。

---

## Compute (Smile: fillColor=#D05C17, gradientColor=#F78E04)

| サービス | resIcon |
|---------|---------|
| Lambda | `lambda` |
| EC2 | `ec2` |
| ECS | `ecs` |
| EKS | `eks` |
| Fargate | `fargate` |
| Batch | `batch` |
| Lightsail | `lightsail` |
| App Runner | `app_runner` |
| Elastic Beanstalk | `elastic_beanstalk` |

## Networking & Content Delivery (Galaxy: fillColor=#5A30B5, gradientColor=#945DF2)

| サービス | resIcon |
|---------|---------|
| CloudFront | `cloudfront` |
| VPC | `vpc` |
| ELB | `elastic_load_balancing` |
| Route 53 | `route_53` |
| Direct Connect | `direct_connect` |
| Global Accelerator | `global_accelerator` |
| Transit Gateway | `transit_gateway` |
| PrivateLink | `privatelink` |

## Storage (Endor: fillColor=#277116, gradientColor=#60A337)

| サービス | resIcon |
|---------|---------|
| S3 | `s3` |
| EBS | `elastic_block_store` |
| EFS | `elastic_file_system` |
| S3 Glacier | `s3_glacier` |
| FSx | `fsx` |
| Storage Gateway | `storage_gateway` |
| Backup | `backup` |

## Database (Nebula: fillColor=#3334B9, gradientColor=#4D72F3)

| サービス | resIcon |
|---------|---------|
| DynamoDB | `dynamodb` |
| RDS | `rds` |
| Aurora | `aurora` |
| ElastiCache | `elasticache` |
| Redshift | `redshift` |
| Neptune | `neptune` |
| DocumentDB | `documentdb_with_mongodb_compatibility` |
| MemoryDB | `memorydb_for_redis` |
| Keyspaces | `keyspaces` |
| Timestream | `timestream` |
| QLDB | `qldb` |

## Application Integration (Cosmos: fillColor=#BC1356, gradientColor=#FF4F8B)

| サービス | resIcon |
|---------|---------|
| API Gateway | `api_gateway` |
| SQS | `sqs` |
| SNS | `sns` |
| Step Functions | `step_functions` |
| EventBridge | `eventbridge` |
| AppSync | `appsync` |
| MQ | `mq` |

## Security, Identity & Compliance (Mars: fillColor=#C7131F, gradientColor=#F54749)

| サービス | resIcon |
|---------|---------|
| Cognito | `cognito` |
| IAM | `identity_and_access_management` |
| WAF | `waf` |
| Shield | `shield` |
| GuardDuty | `guardduty` |
| KMS | `kms` |
| Secrets Manager | `secrets_manager` |
| Certificate Manager | `certificate_manager` |
| Inspector | `inspector` |
| Security Hub | `security_hub` |
| Macie | `macie` |

## Management & Governance (Cosmos: fillColor=#BC1356, gradientColor=#FF4F8B)

| サービス | resIcon |
|---------|---------|
| CloudWatch | `cloudwatch_2` |
| CloudFormation | `cloudformation` |
| CloudTrail | `cloudtrail` |
| Systems Manager | `systems_manager` |
| Config | `config` |
| Trusted Advisor | `trusted_advisor` |
| Organizations | `organizations` |
| Control Tower | `control_tower` |
| Service Catalog | `service_catalog` |

## Analytics (Galaxy: fillColor=#5A30B5, gradientColor=#945DF2)

| サービス | resIcon |
|---------|---------|
| Athena | `athena` |
| Glue | `glue` |
| Kinesis Data Streams | `kinesis_data_streams` |
| Kinesis Data Firehose | `kinesis_data_firehose` |
| QuickSight | `quicksight` |
| EMR | `emr` |
| Lake Formation | `lake_formation` |
| OpenSearch | `opensearch_service` |

## Machine Learning (Orbit: fillColor=#01A88D, gradientColor=#60D3A4)

| サービス | resIcon |
|---------|---------|
| SageMaker | `sagemaker` |
| Bedrock | `bedrock` |
| Rekognition | `rekognition` |
| Transcribe | `transcribe` |
| Translate | `translate` |
| Comprehend | `comprehend` |
| Polly | `polly` |
| Lex | `lex` |
| Textract | `textract` |
| Kendra | `kendra` |

## Developer Tools (Galaxy: fillColor=#5A30B5, gradientColor=#945DF2)

| サービス | resIcon |
|---------|---------|
| CodeBuild | `codebuild` |
| CodePipeline | `codepipeline` |
| CodeDeploy | `codedeploy` |
| CodeCommit | `codecommit` |
| Cloud9 | `cloud9` |
| X-Ray | `xray` |
| CodeArtifact | `codeartifact` |

## Containers (Smile: fillColor=#D05C17, gradientColor=#F78E04)

ECS, EKS, Fargate は Compute セクションと同じ resIcon・カラー。ここではコンテナ専用サービスを追加で掲載。

| サービス | resIcon |
|---------|---------|
| ECR | `ecr` |
| ECS | `ecs` |
| EKS | `eks` |
| Fargate | `fargate` |
| App Mesh | `app_mesh` |

## Front-End Web & Mobile (Cosmos: fillColor=#BC1356, gradientColor=#FF4F8B)

AppSync は Application Integration セクションにも掲載（同じ resIcon・カラー）。

| サービス | resIcon |
|---------|---------|
| Amplify | `amplify` |
| Pinpoint | `pinpoint` |
| AppSync | `appsync` |

## Messaging (Cosmos: fillColor=#BC1356, gradientColor=#FF4F8B)

| サービス | resIcon |
|---------|---------|
| SES | `simple_email_service` |

---

## 直接シェイプ（resourceIcon を使わないもの）

これらは `shape=mxgraph.aws4.<VALUE>` で直接指定する。`resourceIcon`/`resIcon` パターンは使わない。

| リソース | shape 値 | 備考 |
|----------|---------|------|
| Users | `mxgraph.aws4.users` | ユーザーグループ |
| User | `mxgraph.aws4.user` | 個人ユーザー |
| Client | `mxgraph.aws4.client` | クライアント端末 |
| Mobile Client | `mxgraph.aws4.mobile_client` | モバイル端末 |
| Internet | `mxgraph.aws4.internet` | インターネット |
| Internet Gateway | `mxgraph.aws4.internet_gateway` | IGW |
| NAT Gateway | `mxgraph.aws4.nat_gateway` | NAT GW |
| VPN Gateway | `mxgraph.aws4.vpn_gateway` | VPN GW |
| Lambda Function | `mxgraph.aws4.lambda_function` | Lambda 関数リソース |
| S3 Bucket | `mxgraph.aws4.bucket_with_objects` | S3 バケット |
| EC2 Instance | `mxgraph.aws4.instance2` | EC2 インスタンス |
| ALB | `mxgraph.aws4.application_load_balancer` | Application LB |
| NLB | `mxgraph.aws4.network_load_balancer` | Network LB |
| RDS Instance | `mxgraph.aws4.rds_instance` | DB インスタンス |
| DynamoDB Table | `mxgraph.aws4.dynamodb_table` | テーブル |
| SQS Queue | `mxgraph.aws4.sqs_queue` | キュー |
| SNS Topic | `mxgraph.aws4.sns_topic` | トピック |

直接シェイプのスタイル例：
```
sketch=0;outlineConnect=0;fontColor=#232F3E;
gradientColor=none;fillColor=#ED7100;strokeColor=none;
dashed=0;verticalLabelPosition=bottom;verticalAlign=top;
align=center;html=1;fontSize=12;fontStyle=0;aspect=fixed;
pointerEvents=1;shape=mxgraph.aws4.lambda_function;
```
`fillColor` はカテゴリカラーに合わせる。`strokeColor=none`。
