from datetime import timedelta, datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from twitter_etl_pipeline import run_twitter_etl  # Import the ETL function from your pipeline

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 11, 3),
    'email': ['ryanknapp56@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Define the DAG
dag = DAG(
    'twitter_etl_dag',
    default_args=default_args,
    description='ETL Process to fetch tweets and save to CSV',
    schedule_interval=timedelta(days=1),  # Run the DAG every day
    catchup=False  # Don't backfill previous runs
)

# PythonOperator that calls the ETL function
run_etl = PythonOperator(
    task_id='complete_twitter_etl',  # Task ID for Airflow
    python_callable=run_twitter_etl,  # The function to call
    dag=dag,  # Assign this task to the DAG
)

#Just a single task, so no dependencies
run_etl