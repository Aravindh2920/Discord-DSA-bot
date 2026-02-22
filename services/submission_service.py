from database import get_connection
import datetime
from utils.time_utils import get_ist_today, is_before_deadline
from services.problem_service import ProblemService

class SubmissionService:

    @staticmethod
    def has_submitted_today(discord_id):
        today = get_ist_today()

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
        today = get_ist_today()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO submissions (discord_id, problem_id, submission_date, verified)
            VALUES (%s, %s, %s, %s)
        """, (discord_id, problem_id, today, True))

        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def validate_submission_time():
        return is_before_deadline()
    
    @staticmethod
    def validate_submission_link(link: str):
        """
        Ensures submitted link matches today's problem URL.
        """

        problem = ProblemService.get_today_problem()
        if not problem:
            return False, "No problem scheduled today."

        _, _, _, problem_url = problem

        # Basic validation: link must contain problem URL slug
        if problem_url not in link:
            return False, "Submitted link does not match today's problem."

        return True, "Valid submission."