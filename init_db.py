import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

with psycopg2.connect(DATABASE_URL) as conn:
    conn.autocommit = True
    with conn.cursor() as curs:
        with open('database.sql') as f:
            curs.execute(f.read())
