"""Simple test.

Maintainer:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


def print_fruit(fruit_name: str) -> None:
    """Print fruit."""
    print("=" * 30)
    print(f"fruit_name: {fruit_name}")
    print("=" * 30)


default_args = {
    "owner": "dongminlee",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="simple-test",
    default_args=default_args,
    schedule_interval="@once",
    start_date=datetime.today() + timedelta(hours=9),
    max_active_tasks=2,
) as dag:
    t1 = PythonOperator(
        task_id="task_1",
        python_callable=print_fruit,
        op_kwargs={"fruit_name": "apple"},
        dag=dag,
    )

    t2 = BashOperator(task_id="task_2", bash_command="sleep 10", dag=dag)

    t3 = PythonOperator(
        task_id="task_3",
        python_callable=print_fruit,
        op_kwargs={"fruit_name": "banana"},
        dag=dag,
    )

    t4 = BashOperator(task_id="task_4", bash_command="sleep 5", dag=dag)

    t5 = PythonOperator(
        task_id="task_5",
        python_callable=print_fruit,
        op_kwargs={"fruit_name": "cherry"},
        dag=dag,
    )

    t1 >> [t2, t3] >> t4 >> t5
