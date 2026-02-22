from discord.ext import commands

class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helpme")
    async def custom_help(self, ctx):

        help_message = """
📘 **DSA Bot Help**

🔥 **Daily Flow**
• `!addproblem <title> <difficulty> <url>`  
   → Add a new problem (Admin only)

• `!queueproblem <problem_id> <YYYY-MM-DD>`  
   → Schedule a problem for a specific date (Admin only)

• `!submit <link>`  
   → Submit your solution link for today

🏆 **Tracking**
• `!leaderboard`  
   → View top streaks
• `!stats`  
   → View your stats

• `!ping`  
   → Check if bot is running

📌 Rules:
• Submissions close at 11:59 PM IST
• Only one submission per day
• Link must match today's problem
"""

        await ctx.send(help_message)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))