from discord.ext import commands
from database import get_connection

class LeaderboardCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leaderboard(self, ctx):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT discord_id, current_streak
            FROM users
            ORDER BY current_streak DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            await ctx.send("No leaderboard data yet.")
            return

        message = "🏆 **Leaderboard**\n\n"
        for i, (uid, streak) in enumerate(rows, 1):
            user = await self.bot.fetch_user(int(uid))
            message += f"{i}. {user.name} — {streak} 🔥\n"

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))