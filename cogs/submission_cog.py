from discord.ext import commands
from services.problem_service import ProblemService
from services.submission_service import SubmissionService
from services.streak_service import StreakService

class SubmissionCog(commands.Cog):

    @commands.command()
    async def submit(self, ctx, link: str):
        discord_id = str(ctx.author.id)

        if not SubmissionService.validate_submission_time():
            await ctx.send("Submission deadline passed ❌ (11:59 PM IST)")
            return

        # 🔥 NEW VALIDATION
        valid, message = SubmissionService.validate_submission_link(link)
        if not valid:
            await ctx.send(f"❌ {message}")
            return

        problem = ProblemService.get_today_problem()
        problem_id = problem[0]

        if SubmissionService.has_submitted_today(discord_id):
            await ctx.send("You already submitted today ❌")
            return

        SubmissionService.record_submission(discord_id, problem_id)
        streak = StreakService.update_streak(discord_id)

        await ctx.send(f"Submission verified ✅🔥 Current streak: {streak}")

async def setup(bot):
    await bot.add_cog(SubmissionCog())