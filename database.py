import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST") or os.getenv("DB_HOST"),
        user=os.getenv("PGUSER") or os.getenv("DB_USER"),
        password=os.getenv("PGPASSWORD") or os.getenv("DB_PASSWORD"),
        dbname=os.getenv("PGDATABASE") or os.getenv("DB_NAME"),
        port=os.getenv("PGPORT") or os.getenv("DB_PORT")
    )