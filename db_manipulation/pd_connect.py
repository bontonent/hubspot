import psycopg2

from dotenv import load_dotenv
import os
load_dotenv()



def connect_to_db():
    return psycopg2.connect(
        dbname = os.getenv('db_name'),
        user = os.getenv('db_user'),
        password = os.getenv('db_password'),
        port = os.getenv('db_port'),
        host = os.getenv('db_host')
    )
    
    return conn, cur

# def code():
#     conn, cur = connect_to_db()
#     cur = conn.cursor()
#     conn = connect_to_db()

#     #code code code
    
#     cur.close()
#     conn.close()


if __name__ == "__main__":
    
