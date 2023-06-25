"""Consume queued data from RabbitMQ.

Maintainer:
    Name: Donghyun Kim
    Email: rkdqus2006@naver.com
"""
from datetime import datetime

import boto3
import pika
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
from pytz import timezone

credentials = pika.PlainCredentials("rabbit", "rabbit")
parameters = pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)


MINIO_BUCKET = "bucket"
MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY_ID = "minio"
MINIO_SECRET_ACCESS_KEY = "minio123"

BOTO3_CLIENT = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY_ID,
    aws_secret_access_key=MINIO_SECRET_ACCESS_KEY,
)


def insert_into_target_storage_callback(
    ch: BlockingChannel,  # noqa: ARG001
    method: spec.Basic.Deliver,  # noqa: ARG001
    properties: spec.BasicProperties,  # noqa: ARG001
    body: bytes,
) -> None:
    """Insert queue data to MinIO."""
    _now = datetime.now(tz=timezone("Asia/Seoul"))
    print(f"[{_now}]: {body}")

    BOTO3_CLIENT.put_object(
        Bucket=MINIO_BUCKET,
        Key=f"{_now}.json",
        Body=body,
    )


def get_comsuming_channel() -> BlockingChannel:
    """Create or connect to rabbitmq queue and return channel.

    Returns
    -------
    BlockingChannel
        Consumer channel.
    """
    conn = pika.BlockingConnection(parameters)

    channel = conn.channel()
    channel.queue_declare("rabbitmq-simple-queue")
    channel.basic_consume(
        queue="rabbitmq-simple-queue",
        auto_ack=True,
        on_message_callback=insert_into_target_storage_callback,
    )
    return channel


def main() -> None:
    """Consumer data from rabbitmq."""
    channel = get_comsuming_channel()
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
