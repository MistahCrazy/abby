import discord
from discord.ext import tasks, commands
from random import choice

from utils.exchange import get_exchange_rate, currencies

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.select_from = tuple(k for k, v in currencies.items() if v['crypto'] or k == 'RUB')
        self.select_to = tuple(k for k, v in currencies.items() if not v['crypto'] and k != 'RUB')

        self.random_status.start()

    def cog_unload(self):
        self.random_status.stop()

    @tasks.loop(minutes=2, seconds=30)
    async def random_status(self):
        sf = choice(self.select_from)
        st = choice(self.select_to)
        val = get_exchange_rate(sf, st)

        activity = discord.Activity(
            name=f'{currencies[sf]["symbol"]} at {val}',
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
