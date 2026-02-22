import asyncio
import discord
from discord.ext import commands
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

async def load_cogs():
    await bot.load_extension("cogs.problem_cog")
    await bot.load_extension("cogs.submission_cog")
    await bot.load_extension("cogs.leaderboard_cog")
    await bot.load_extension("cogs.help_cog")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())