import datetime
import pytz
from discord.ext import tasks

IST = pytz.timezone("Asia/Kolkata")

def daily_task(bot, callback):
    """
    Creates a deterministic daily 6 AM IST task.
    The callback must be an async function.
    """

    @tasks.loop(time=datetime.time(hour=6, minute=00, tzinfo=IST))
    async def wrapper():
        await bot.wait_until_ready()
        await callback()

    return wrapper