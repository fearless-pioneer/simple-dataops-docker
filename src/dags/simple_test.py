"""Simple test."""
import time
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator


def print_fruit(fruit_name: str) -> None:
    """Print fruit."""
    print("=" * 30)
    print(f"fruit_name: {fruit_name}")
    print("=" * 30)


def sleep_seconds(seconds: int) -> None:
    """Sleep seconds."""
    print("=" * 30)
    print(f"seconds: {str(seconds)}")
    print("sleeping...")
    print("=" * 30)
    time.sleep(seconds)


default_args = {
    "owner": "dongminlee",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="simple_test",
    default_args=default_args,
    schedule_interval="@once",
    start_date=datetime.today(),
    max_active_tasks=2,
) as dag:
    t1 = PythonOperator(
        task_id="task_1",
        python_callable=print_fruit,
        op_kwargs={"fruit_name": "apple"},
        dag=dag,
    )

    t2 = PythonOperator(
        task_id="task_2",
        python_callable=print_fruit,
        op_kwargs={"fruit_name": "banana"},
        dag=dag,
    )

    t3 = PythonOperator(
        task_id="task_3",
        python_callable=sleep_seconds,
        op_kwargs={"seconds": 10},
        dag=dag,
    )

    t4 = PythonOperator(
        task_id="task_4",
        python_callable=print_fruit,
        op_kwargs={"fruit_name": "cherry"},
        dag=dag,
    )

    t1 >> [t2, t3] >> t4
