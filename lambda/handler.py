import json
import os
import uuid
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")


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


def save_chat_history(session_id, message, result):
    table_name = os.environ["HISTORY_TABLE"]
    table = dynamodb.Table(table_name)

    timestamp = datetime.now(timezone.utc).isoformat()

    table.put_item(
        Item={
            "session_id": session_id,
            "timestamp": timestamp,
            "question": message,
            "answer": result["answer"],
            "source": result["source"],
            "confidence": str(result["confidence"]),
            "mode": "mock"
        }
    )

    return timestamp


def lambda_handler(event, context):
    raw_body = event.get("body")

    try:
        body = raw_body or "{}"
        if isinstance(body, str):
            body = json.loads(body)

        message = body.get("message", "")
        session_id = body.get("session_id", str(uuid.uuid4()))

        faq_items = load_faq()
        result = find_answer(message, faq_items)
        timestamp = save_chat_history(session_id, message, result)

        response = {
            "answer": result["answer"],
            "source": result["source"],
            "confidence": result["confidence"],
            "model": "mock-llm-v1",
            "mode": "mock",
            "input": message,
            "session_id": session_id,
            "timestamp": timestamp
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
                    "raw_body": raw_body,
                    "mode": "mock"
                },
                ensure_ascii=False
            )
        }
