from database import get_connection
import datetime

class StreakService:

    @staticmethod
    def update_streak(discord_id):
        today = datetime.date.today()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT current_streak, longest_streak, last_submission_date
            FROM users
            WHERE discord_id = %s
        """, (discord_id,))

        user = cursor.fetchone()

        if not user:
            current = 1
            longest = 1

            cursor.execute("""
                INSERT INTO users (discord_id, current_streak, longest_streak, last_submission_date)
                VALUES (%s, %s, %s, %s)
            """, (discord_id, current, longest, today))
        else:
            current, longest, last_date = user

            if last_date:
                if last_date == today - datetime.timedelta(days=1):
                    current += 1
                elif last_date < today - datetime.timedelta(days=1):
                    current = 1
            else:
                current = 1

            longest = max(longest, current)

            cursor.execute("""
                UPDATE users
                SET current_streak = %s,
                    longest_streak = %s,
                    last_submission_date = %s
                WHERE discord_id = %s
            """, (current, longest, today, discord_id))

        conn.commit()
        cursor.close()
        conn.close()

        return current
    
    @staticmethod
    def get_user_stats(discord_id: str):
        conn = get_connection()
        cursor = conn.cursor()

        # Get streak info
        cursor.execute("""
            SELECT current_streak, longest_streak
            FROM users
            WHERE discord_id = %s
        """, (discord_id,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return None

        current_streak, longest_streak = user

        # Total submissions
        cursor.execute("""
            SELECT COUNT(*)
            FROM submissions
            WHERE discord_id = %s
        """, (discord_id,))
        total_submissions = cursor.fetchone()[0]

        # Rank calculation
        cursor.execute("""
            SELECT COUNT(*) + 1
            FROM users
            WHERE current_streak > (
                SELECT current_streak FROM users WHERE discord_id = %s
            )
        """, (discord_id,))
        rank = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "total_submissions": total_submissions,
            "rank": rank
        }