"""Send time to RabbitMQ.

Maintainer:
    Name: Donghyun Kim
    Email: rkdqus2006@naver.com
"""
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def produce_time_to_queue(
    timezone: str,
    host: str,
    port: int,
    user: str,
    password: str,
    queue_name: str = "rabbitmq-demo-queue",
    exchange: str = "",
) -> None:
    """Publish KST time to rabbitmq.

    Parameters
    ----------
    timezone : str
        Available timezone string to be used by pytz.timezone. e.g. Asia/Seoul.
    host : str
        Rabbtmq host ip or URI.
    port : int
        Rabbtmq port.
        if your rabbitmq server running by basic settings, it would be 5672.
    user : str
        Rabbtmq user name.
    password : str
        Rabbtmq password.
    queue_name : str, optional
        Rabbtmq queue name if not exists create new queue, by default "rabbitmq-demo-queue"
    exchange : str, optional
        Rabbtmq queue exchange type., by default "" it means Direct Exchange type.
    """
    import datetime

    import pika
    import pytz

    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, "/", credentials)

    conn = pika.BlockingConnection(parameters)
    channel = conn.channel()
    channel.queue_declare(queue=queue_name)

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue_name,
        body=datetime.datetime.now(tz=pytz.timezone(timezone)).strftime("%y%m%d-%H:%M:%S"),
    )

    conn.close()


default_args = {
    "owner": "donghyunkim",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="produce-time-to-rabbitmq",
    default_args=default_args,
    schedule_interval=timedelta(minutes=1),
    start_date=datetime.today(),
    max_active_tasks=2,
) as dag:
    t1 = BashOperator(
        task_id="rabbitmq-health-check",
        bash_command='echo "check health state"',
    )

    t2 = PythonOperator(
        task_id="produce-time-to-queue",
        python_callable=produce_time_to_queue,
        op_kwargs={
            "timezone": "Asia/Seoul",
            "host": "rabbitmq",
            "port": 5672,
            "user": "rabbit",
            "password": "rabbit",
        },
        dag=dag,
    )

    t1 >> t2
