import psycopg2

from dotenv import load_dotenv
import os
load_dotenv()

def connect_to_db():
    conn = psycopg2.connect(
        dbname = os.getenv('db_name'),
        user = os.getenv('db_user'),
        password = os.getenv('db_password'),
        port = os.getenv('db_port'),
        host = os.getenv('db_host')
    )
    cur = conn.cursor()

def add_data():

    None

