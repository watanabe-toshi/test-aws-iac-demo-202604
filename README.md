# AWS Terraform IaC Demo for New Hires

## 概要

このリポジトリは、新入社員向けの IaC 学習用デモです。  
Terraform を利用して、AWS 上に「AIチャット基盤のモック環境」を構築します。

今回は本物の生成AIは利用せず、API Gateway で受け付けたリクエストを Lambda が処理し、S3 に配置した FAQ データを参照して回答を返します。  
AI基盤の考え方を学ぶための最小構成として作成しています。

---

## 技術スタック

- **Terraform**
  - AWS リソースの構築と管理
- **AWS API Gateway**
  - 外部からのリクエストを受け付ける API の入口
- **AWS Lambda**
  - チャット処理を行うアプリケーション本体
- **Amazon S3**
  - FAQ やナレッジデータの保存先
- **Amazon CloudWatch Logs**
  - Lambda の実行ログ確認
- **Python**
  - Lambda 関数の実装言語

---

## 構成

```text
[User]
   |
   v
API Gateway  ---> Lambda(chat mock) ---> S3(knowledge docs)
                      |
                      v
               CloudWatch Logs

