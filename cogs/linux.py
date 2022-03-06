# pyright: reportMissingImports=false

import signal
import asyncio
from systemd import daemon
from discord.ext import tasks, commands

class Linux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.watchdog.start()

    # wtf does this do exactly???
    def shutdown(self):
        daemon.notify('STOPPING=1')

        for task in asyncio.all_tasks():
            task.cancel()

        self.loop.create_task(self.bot.close())
        self.loop.stop()

    def cog_unload(self):
        self.watchdog.cancel()

    @tasks.loop(minutes=4)
    async def watchdog(self):
        daemon.notify('WATCHDOG=1')

    @watchdog.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

        for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM, signal.SIGABRT):
            self.loop.add_signal_handler(sig, self.shutdown)

        daemon.notify('READY=1')

def setup(bot):
    bot.add_cog(Linux(bot))
