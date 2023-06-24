"""Consume queued data from RabbitMQ.

Maintainer:
    Name: Donghyun Kim
    Email: rkdqus2006@naver.com
"""
from datetime import datetime

import pika
from pika import spec
from pika.adapters.blocking_connection import BlockingChannel
from pytz import timezone

credentials = pika.PlainCredentials("rabbit", "rabbit")
parameters = pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)


def insert_into_target_storage_callback(
    ch: BlockingChannel,  # noqa: ARG001
    method: spec.Basic.Deliver,  # noqa: ARG001
    properties: spec.BasicProperties,  # noqa: ARG001
    body: bytes,
) -> None:
    """Insert queue data to MinIO."""
    print(f"[{datetime.now(tz=timezone('Asia/Seoul'))}]: {body}")

    # TODO: Parse data and push MinIO.


def consume_msg() -> None:
    """Create or connect to rabbitmq queue and consume data."""
    conn = pika.BlockingConnection(parameters)

    channel = conn.channel()
    channel.queue_declare("rabbitmq-demo-queue")
    channel.basic_consume(
        queue="rabbitmq-demo-queue",
        auto_ack=True,
        on_message_callback=insert_into_target_storage_callback,
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def main() -> None:
    """Consumer data from rabbitmq."""
    consume_msg()


if __name__ == "__main__":
    main()
