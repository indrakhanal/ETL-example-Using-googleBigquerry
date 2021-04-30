from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner':'airflow',
    'depend_on_past':False,
    'start_date':datetime(2018, 11, 5, 00,00,00),
    'retries':1,
    'retries-delay':timedelta(minutes=1)
}


def get_activated_source():
    request = "SELECT * FROM pet "
    pg_hook = PostgresHook(postgre_con_id='postgres_sql', schema='Pet')
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(request)
    pets = cursor.fetchall()
    for pet in pets:
        print(pet, '\n')
    return pets


with DAG('hook_dag', default_args=default_args, schedule_interval='@once', catchup=False) as dag:
    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id='fetch-data-from-hook', python_callable=get_activated_source)

start_task >> hook_task
