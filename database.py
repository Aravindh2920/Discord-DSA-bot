import psycopg2
import os
from urllib.parse import urlparse

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL not set")

    # Normalize scheme if needed
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgres://", 1)

    # Parse URL manually for clarity
    parsed = urlparse(database_url)

    return psycopg2.connect(
        dbname=parsed.path.lstrip("/"),
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port,
        sslmode="require"   # 🔥 THIS IS THE IMPORTANT PART
    )