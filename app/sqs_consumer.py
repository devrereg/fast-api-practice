import os
import threading
import boto3
import json
import time
from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.getenv('QUEUE_URL')
REGION = os.getenv('REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')


def crawl(url: str):
    print(f"[크롤링 시작] URL: {url}")
    # selenium 작업을 여기에 연결하면 됨
    time.sleep(2)
    print(f"[크롤링 완료] URL: {url}")


def poll_sqs():
    print("SQS consumer 시작됨")
    sqs = boto3.client(
        "sqs",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION
    )

    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=2,
            WaitTimeSeconds=10
        )
        messages = response.get("Messages", [])
        print(f"messages: {messages}")
        instagram_ids = []
        for message in messages:
            body = json.loads(message["Body"])
            id = body.get("instagramId")
            instagram_ids.append(id)
            if id:
                crawl(id)

            # 메시지 삭제
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"]
            )


def start_consumer_in_background():
    thread = threading.Thread(target=poll_sqs, daemon=True)
    thread.start()
