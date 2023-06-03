"""Send time to RabbitMQ.

Maintainer:
    Name: Donghyun Kim
    Email: rkdqus2006@naver.com
"""
# import time
from datetime import datetime, timedelta

# import pika
from airflow.models import DAG
from airflow.operators.python import PythonOperator


def establish_connect() -> None:
    """TBD."""


def set_msg_queue() -> None:
    """TBD."""


def produce_time_to_queue() -> None:
    """TBD."""


default_args = {
    "owner": "donghyunkim",
    "depends_on_past": False,
    "retries": 4,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="produce-time-to-rabbitmq",
    default_args=default_args,
    schedule_interval="@once",
    start_date=datetime.today(),
    max_active_tasks=2,
) as dag:
    t1 = PythonOperator(
        task_id="Establish-connection",
        python_callable=establish_connect,
        op_kwargs={"fruit_name": "apple"},
        dag=dag,
    )

    t2 = PythonOperator(
        task_id="make-msg-queue",
        python_callable=set_msg_queue,
        dag=dag,
    )

    t3 = PythonOperator(
        task_id="task_3",
        python_callable=produce_time_to_queue,
        op_kwargs={"timezone": "Asia/Seoul"},
        dag=dag,
    )

    t1 >> t2 >> t3
