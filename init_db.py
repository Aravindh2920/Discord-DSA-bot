# init_db.py

from database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        discord_id VARCHAR(50) UNIQUE NOT NULL,
        current_streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        last_submission_date DATE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        difficulty VARCHAR(20),
        url TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problem_queue (
        id SERIAL PRIMARY KEY,
        problem_id INTEGER REFERENCES problems(id) ON DELETE CASCADE,
        scheduled_date DATE NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id SERIAL PRIMARY KEY,
        discord_id VARCHAR(50),
        problem_id INTEGER REFERENCES problems(id),
        submission_date DATE,
        verified BOOLEAN DEFAULT FALSE
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()