from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 26),
    'retries': 1,
}

dag = DAG(
    'my_postgres_dag',
    default_args=default_args,
    description='A simple PostgreSQL DAG',
    schedule_interval=None,
)

# Konfigurieren Sie Ihre Verbindungsinformationen hier
connection_id = 'my_postgres_connection'

create_table_sql = """
CREATE TABLE IF NOT EXISTS meine_tabelle (
    datum timestamp,
    supermarkt text,
    artikelnummer text,
    umsatz numeric
);
"""

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id=connection_id,  # Verbindungs-ID aus Ihrer Airflow-Konfiguration
    sql=create_table_sql,
    dag=dag,
)

create_table_task
