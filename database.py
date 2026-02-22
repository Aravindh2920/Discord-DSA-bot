import psycopg2
import os

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL not set")

    return psycopg2.connect(database_url)