import json
import os
import boto3

s3 = boto3.client("s3")


def load_faq():
    bucket = os.environ["KNOWLEDGE_BUCKET"]
    key = os.environ["KNOWLEDGE_KEY"]

    response = s3.get_object(Bucket=bucket, Key=key)
    body = response["Body"].read().decode("utf-8")
    return json.loads(body)


def find_answer(message, faq_items):
    message_lower = message.lower()

    for item in faq_items:
        keywords = item.get("keywords", [])
        if any(keyword.lower() in message_lower for keyword in keywords):
            return {
                "answer": item["answer"],
                "source": item["source"],
                "confidence": 0.93
            }

    return {
        "answer": "申し訳ありません。該当情報が見つかりませんでした。担当部署へお問い合わせください。",
        "source": "knowledge/faq.json",
        "confidence": 0.42
    }


def lambda_handler(event, context):
    try:
        body = event.get("body") or "{}"
        if isinstance(body, str):
            body = json.loads(body)

        message = body.get("message", "")

        faq_items = load_faq()
        result = find_answer(message, faq_items)

        response = {
            "answer": result["answer"],
            "source": result["source"],
            "confidence": result["confidence"],
            "model": "mock-llm-v1",
            "mode": "mock",
            "input": message
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(
                {
                    "error": str(e),
                    "mode": "mock"
                },
                ensure_ascii=False
            )
        }