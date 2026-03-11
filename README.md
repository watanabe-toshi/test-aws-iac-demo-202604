# AWS Terraform IaC Demo

## 概要

Terraform を利用して、AWS 上に AIチャット基盤を模したモック環境を構築するデモです。  
API Gateway、Lambda、S3、CloudWatch Logs を組み合わせ、FAQ ベースで回答する簡易 API を作成します。

## 技術スタック

- Terraform
- AWS API Gateway
- AWS Lambda
- Amazon S3
- Amazon CloudWatch Logs
- Python
- DynamoDB

## 構成

```text
[User]
   |
   v
API Gateway ---> Lambda(chat mock) ---> S3(knowledge docs)
                     |
                     +------------> DynamoDB(chat history)
                     |
                     v
              CloudWatch Logs
```

## 確認
```text
curl -X POST "$(terraform output -raw chat_api_url)" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data-binary @request.json
```

## 補足

本デモは学習用の最小構成です。  
本番環境では、Bedrock、認証認可、監視、セキュリティ強化などを追加して拡張します。
