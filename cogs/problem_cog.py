from discord.ext import commands, tasks
from services.problem_service import ProblemService
from config import CHANNEL_ID

class ProblemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_problem.start()

    @tasks.loop(hours=24)
    async def daily_problem(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        problem = ProblemService.get_today_problem()
        if not problem:
            return

        _, title, difficulty, url = problem

        await channel.send(
            f"🔥 **DSA Challenge of the Day**\n\n"
            f"📌 {title}\n"
            f"🎯 Difficulty: {difficulty}\n"
            f"🔗 {url}"
        )

    @commands.command()
    async def addproblem(self, ctx, title: str, difficulty: str, url: str):
        ProblemService.add_problem(title, difficulty, url)
        await ctx.send("Problem added ✅")

async def setup(bot):
    await bot.add_cog(ProblemCog(bot))