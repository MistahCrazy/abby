import discord
from discord.ext import tasks, commands
from random import choice
from typing import Tuple
from functools import cached_property

from utils.exchange import get_exchange_rate, currencies

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_exchange = ('', '')

        self.random_status.start()

    def cog_unload(self):
        self.random_status.stop()

    @cached_property
    def _exchange_from(self) -> Tuple[str, ...]:
        return tuple(k for k, v in currencies.items() if v['crypto'] or k == 'RUB')

    @cached_property
    def _exchange_to(self) -> Tuple[str, ...]:
        return tuple(k for k, v in currencies.items() if not v['crypto'] and k != 'RUB')

    def get_random_exchange(self) -> Tuple[str, str]:
        ex = ('BTC', 'USD')

        for _ in range(7):
            ex = (choice(self._exchange_from), choice(self._exchange_to))

            if ex[0] != self._last_exchange[0]:
                break

        return ex

    @tasks.loop(minutes=3, seconds=33)
    async def random_status(self):
        cf, ct = self.get_random_exchange()

        activity = discord.Activity(
            name=f'{currencies[cf]["symbol"]} at {get_exchange_rate(cf, ct)}',
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
