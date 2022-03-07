import discord
from discord.ext import tasks, commands
from random import choice

from utils.exchange import get_exchange_loop

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.exchange_loops = (
            iter(get_exchange_loop('RUB', '₽ at ')),
            iter(get_exchange_loop('BTC', '₿ at '))
        )
        self.random_status.start()

    def cog_unload(self):
        self.random_status.stop()

    @tasks.loop(minutes=5)
    async def random_status(self):
        activity = discord.Activity(
            name=next(choice(self.exchange_loops)),
            type=discord.ActivityType.watching
        )

        await self.bot.change_presence(
            activity=activity,
            status=discord.Status.do_not_disturb
        )

    @random_status.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Status(bot))
