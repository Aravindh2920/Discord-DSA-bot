from discord.ext import commands
from services.problem_service import ProblemService
from services.submission_service import SubmissionService
from services.streak_service import StreakService

class SubmissionCog(commands.Cog):

    @commands.command()
    async def submit(self, ctx, link: str):
        discord_id = str(ctx.author.id)

        problem = ProblemService.get_today_problem()
        if not problem:
            await ctx.send("No problem scheduled today.")
            return

        problem_id = problem[0]

        if SubmissionService.has_submitted_today(discord_id):
            await ctx.send("You already submitted today ❌")
            return

        SubmissionService.record_submission(discord_id, problem_id)
        streak = StreakService.update_streak(discord_id)

        await ctx.send(f"Submission recorded 🔥 Current streak: {streak}")

async def setup(bot):
    await bot.add_cog(SubmissionCog())