"""Batch glue dag.

Maintainer:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator

from src.dags.batch_glue.pipeline import run

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
    schedule_interval="0 * * * *",
    start_date=datetime.today(),
    max_active_tasks=2,
) as dag:
    t1 = PythonOperator(
        task_id="task_1",
        python_callable=run,
        op_kwargs={"fruit_name": "apple"},
        dag=dag,
    )
