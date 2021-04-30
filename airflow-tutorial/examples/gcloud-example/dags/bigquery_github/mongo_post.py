from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
# from airflow.operators.postgres_operator import PostgresOperator
import psycopg2
import pendulum

local_tz = pendulum.timezone("Europe/Amsterdam")

# importing module
# from pymongo import MongoClient

# def mongo_connect():
#     client=MongoClient()
#     client = MongoClient("mongodb://localhost:27017/")
#     mydatabase = client['Example']
#     mycollection=mydatabase['pet']
#     rec={
#     'title': 'MongoDB and Python',
#     'description': 'MongoDB is no SQL database',
#     'tags': ['mongodb', 'database', 'NoSQL'],
#     'viewers': 104
#     }
#
#     record = mydatabase.pet.insert(rec)
#     print('sucess')


def postgres_table():
    connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="192.168.1.88",
                                  port="5432",
                                  database="Pet")
    cursor = connection.cursor()

    sql = """ 
            CREATE TABLE IF NOT EXISTS person (
            p_id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            person_address VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            contact VARCHAR NOT NULL
            );
          """

    cursor.execute(sql)
    print('sucessfully created table', '\n', 'PARSED QUERRY', sql)


def postgres_connection():
        connection = psycopg2.connect(user="postgres",
                                    password="admin",
                                    host="localhost",
                                    port="5432",
                                    database="Pet")
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO pet (pet_id, name, pet_type, birth_date,owner ) VALUES (%s,%s,%s, %s, %s)"""
        record_to_insert = (5, 'puppy', 'Dog', datetime(2021, 4, 22),'man')
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 8,  tzinfo=local_tz),
    'email': ['indrakhanal@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'schedule_interval': '@hourly',
    'retry_delay': timedelta(seconds=5),
}

dag = DAG('mongoDB', 
default_args=default_args,
schedule_interval = '@once',)

t1 = BashOperator(
    task_id='Start',
    bash_command='date',
    dag=dag)

t2 = PythonOperator(dag=dag,
     task_id='create-table',
     python_callable=postgres_table,
     )

t3 = PythonOperator(dag=dag,
     task_id='Insert-into-Postgres',
     python_callable=postgres_connection, 
     )

t1 >> t2 >> t3
