from database import get_connection
import datetime

class ProblemService:

    @staticmethod
    def get_today_problem():
        today = datetime.date.today()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.id, p.title, p.difficulty, p.url
            FROM problem_queue pq
            JOIN problems p ON pq.problem_id = p.id
            WHERE pq.scheduled_date = %s
        """, (today,))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def add_problem(title, difficulty, url):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO problems (title, difficulty, url) VALUES (%s, %s, %s)",
            (title, difficulty, url)
        )

        conn.commit()
        cursor.close()
        conn.close()