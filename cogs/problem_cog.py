from discord.ext import commands, tasks
from services.problem_service import ProblemService
from config import CHANNEL_ID
from utils.scheduler import daily_task

class ProblemCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("ProblemCog loaded")
        self.daily_problem = daily_task(bot, self.send_daily_problem)
        self.daily_problem.start()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Bot working 🚀")

    async def send_daily_problem(self):
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            print("Channel not found.")
            return

        problem = ProblemService.get_today_problem()
        if not problem:
            print("No problem scheduled for today.")
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
        print("addproblem called")
        ProblemService.add_problem(title, difficulty, url)
        await ctx.send("Problem added ✅")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def queueproblem(self, ctx, problem_id: int, date: str):
        success, message = ProblemService.queue_problem(problem_id, date)

        if success:
            await ctx.send(f"✅ {message}")
        else:
            await ctx.send(f"❌ {message}")

async def setup(bot):
    await bot.add_cog(ProblemCog(bot))