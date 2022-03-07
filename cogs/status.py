import discord
from discord.ext import tasks, commands

from utils.shite import get_exchange_loop()

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.ruble_list = iter()
        self.bitcoin_list = iter(get_bitcoin_list())
        self.random_status.start()

    def cog_unload(self):
        self.random_status.stop()

    @tasks.loop(minutes=5)
    async def random_status(self):
        activity = discord.Activity(
            name=f'₿ at {next(self.bitcoin_list)}',
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
