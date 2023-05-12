from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv


load_dotenv()
db_url = getenv('DATABASE_URL')


def execute_all_sql_commands_from_file(file_path):
    with connect(db_url) as conn:
        with conn.cursor() as curs:
            with open(file_path) as f:
                curs.execute(f.read())


def set_data_to_table(sql, data):
    with connect(db_url) as conn:
        with conn.cursor() as curs:
            curs.execute(sql, data)


def get_one_value(sql, data):
    with connect(db_url) as conn:
        with conn.cursor() as curs:
            curs.execute(sql, data)

            return curs.fetchone()[0]


def get_one_row(sql, data):
    with connect(db_url) as conn:
        with conn.cursor() as curs:
            curs.execute(sql, data)

            return curs.fetchone()


def get_some_rows(sql, data):
    with connect(db_url) as conn:
        with conn.cursor() as curs:
            curs.execute(sql, data)

            return curs.fetchall()
