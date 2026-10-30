
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def run_hcpcs_pipeline():
    from hcpcs_pipeline.pipeline import run_pipeline
    return run_pipeline()


with DAG(
    dag_id="hcpcs_data_pipeline",
    description="Extract, transform, load and validate HCPCS data",
    start_date=datetime(2025, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    default_args={
        "owner": "data-engineering",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    pipeline_task = PythonOperator(
        task_id="run_hcpcs_pipeline",
        python_callable=run_hcpcs_pipeline,
    )
