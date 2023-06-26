"""Send generated data to RabbitMQ.

Maintainer:
    Name: Donghyun Kim
    Email: rkdqus2006@naver.com
"""
from datetime import datetime, timedelta

import pika
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pymongo import MongoClient


def produce_data_to_queue(
    host: str,
    port: int,
    user: str,
    password: str,
    queue_name: str = "rabbitmq-simple-queue",
    exchange: str = "",
    **context,
) -> None:
    """Publish data to RabbitMQ queue.

    Parameters
    ----------
    host : str
        Rabbtmq host ip or URI.
    port : int
        Rabbtmq port.
        if your RabbitMQ server running by basic settings, it would be 5672.
    user : str
        Rabbtmq user name.
    password : str
        Rabbtmq password.
    queue_name : str, optional
        Rabbtmq queue name if not exists create new queue, by default "rabbitmq-simple-queue"
    exchange : str, optional
        Rabbtmq queue exchange type., by default "" it means Direct Exchange type.
    """
    # Connect to mongo client
    mongo_client = MongoClient(
        username="mongo",
        password="mongo",
        host="mongodb",
        port=27017,
        directConnection=True,
        ssl=False,
    )
    task_time = datetime.fromisoformat(context["ts"].split("+")[0])
    start_date = str(datetime.strptime(str(task_time), "%Y-%m-%d %H:%M:%S") + timedelta(hours=9))

    # Connect to queue
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, "/", credentials)
    conn = pika.BlockingConnection(parameters)

    # Create a new channel and declare a queue on RabbitMQ server
    channel = conn.channel()
    queue = channel.queue_declare(queue=queue_name)

    # Select documents from Mongo DB
    select_query = {"time": {"$gte": start_date}} if queue.method.message_count > 0 else {}
    docs = list(mongo_client["mongo"]["wine_data"].find(select_query))

    for doc in docs:
        features = doc["features"]

        # Publish the document to the queue
        channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=features,
        )

    # Close the connection with RabbitMQ server
    conn.close()


default_args = {
    "owner": "donghyunkim",
    "depends_on_past": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="batch-sqs",
    default_args=default_args,
    schedule_interval="*/1 * * * *",
    start_date=datetime.today() + timedelta(hours=9) - timedelta(minutes=1),
):
    t1 = BashOperator(
        task_id="guide-procduce-data-to-rabbitmq",
        bash_command='echo "Start producing data to rabbitmq... task time is.. {{ ts }}(UTC)"',
    )

    t2 = PythonOperator(
        task_id="produce-data-to-rabbitmq",
        python_callable=produce_data_to_queue,
        provide_context=True,
        op_kwargs={
            "host": "rabbitmq",
            "port": 5672,
            "user": "rabbit",
            "password": "rabbit",
        },
    )

    t1 >> t2
