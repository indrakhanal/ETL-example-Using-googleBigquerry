import psycopg2
from datetime import datetime


def postgres_table():
    connection = psycopg2.connect(user="postgres",
                                  password="admin",
                                  host="localhost",
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
    connection.commit()
    print('sucessfully created table', '\n', 'PARSED QUERRY', sql)

    postgres_insert_query = """ INSERT INTO person (p_id, name, person_address, birth_date,contact ) VALUES (%s,%s,%s, %s, %s)"""
    record_to_insert = (5, 'Ram', 'ktm', datetime(2021, 4, 22), '9846718211')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into mobile table")


postgres_table()