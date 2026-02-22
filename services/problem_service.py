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

    @staticmethod
    def queue_problem(problem_id: int, date_str: str):
        """
        Queues a problem for a specific date (YYYY-MM-DD).
        """

        try:
            scheduled_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD."

        if scheduled_date < datetime.date.today():
            return False, "Cannot schedule for past dates."

        conn = get_connection()
        cursor = conn.cursor()

        # Check if problem exists
        cursor.execute(
            "SELECT id FROM problems WHERE id = %s",
            (problem_id,)
        )
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Problem ID does not exist."

        # Check if date already scheduled
        cursor.execute(
            "SELECT id FROM problem_queue WHERE scheduled_date = %s",
            (scheduled_date,)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "A problem is already scheduled for this date."

        # Insert queue entry
        cursor.execute(
            "INSERT INTO problem_queue (problem_id, scheduled_date) VALUES (%s, %s)",
            (problem_id, scheduled_date)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return True, "Problem scheduled successfully."