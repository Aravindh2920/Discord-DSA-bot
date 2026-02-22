from database import get_connection
import datetime

class SubmissionService:

    @staticmethod
    def has_submitted_today(discord_id):
        today = datetime.date.today()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM submissions
            WHERE discord_id = %s AND submission_date = %s
        """, (discord_id, today))

        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None

    @staticmethod
    def record_submission(discord_id, problem_id):
        today = datetime.date.today()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO submissions (discord_id, problem_id, submission_date, verified)
            VALUES (%s, %s, %s, %s)
        """, (discord_id, problem_id, today, True))

        conn.commit()
        cursor.close()
        conn.close()