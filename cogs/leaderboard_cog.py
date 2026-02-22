from discord.ext import commands
from database import get_connection
from services.streak_service import StreakService
import discord

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

    @commands.command()
    async def stats(self, ctx):
        discord_id = str(ctx.author.id)

        stats = StreakService.get_user_stats(discord_id)

        if not stats:
            await ctx.send("No stats found. Submit a problem first 🔥")
            return

        embed = discord.Embed(
            title=f"📊 {ctx.author.name}'s Stats",
            color=0x00ff99
        )

        embed.add_field(
            name="🔥 Current Streak",
            value=str(stats["current_streak"]),
            inline=False
        )

        embed.add_field(
            name="🏆 Longest Streak",
            value=str(stats["longest_streak"]),
            inline=False
        )

        embed.add_field(
            name="📦 Total Submissions",
            value=str(stats["total_submissions"]),
            inline=False
        )

        embed.add_field(
            name="🥇 Rank",
            value=f"#{stats['rank']}",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))