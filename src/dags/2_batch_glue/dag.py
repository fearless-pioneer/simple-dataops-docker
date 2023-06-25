"""Batch glue dag.

Maintainer:
    Name: Dongmin Lee
    Email: kid33629@gmail.com
"""
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "dongminlee",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "execution_timeout": timedelta(minutes=5),
}

with DAG(
    dag_id="batch-glue",
    default_args=default_args,
    schedule_interval="*/1 * * * *",
    start_date=datetime.today() + timedelta(hours=9) - timedelta(minutes=1),
    max_active_tasks=2,
) as dag:
    t1 = BashOperator(
        task_id="run-batch-glue",
        bash_command="python $AIRFLOW_HOME/dags/2_batch_glue/pipeline.py --task-time {{ ts }}",
    )
