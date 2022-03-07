#!/usr/bin/env venv/bin/python

import os
import asyncio
import discord
from config import Client
from functools import partial
from discord.ext import commands
from discord.ext.commands import errors
from traceback import print_exception
from concurrent.futures import ThreadPoolExecutor
from collections.abc import Callable

from config import Client

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.loop.set_default_executor(self.thread_pool)

        self.load_cogs()

    async def on_message(self, msg: discord.Message):
        if msg.author.bot: return
        if not isinstance(msg.channel, discord.TextChannel): return

        await self.process_commands(msg)

    async def on_command(self, ctx: commands.Context):
        await self.wait_to_delete(ctx.message, Client.command_timeout)

    async def on_command_error(self, ctx: commands.Context, err: Exception):
        output = ''

        if hasattr(err, 'original'):
            output = 'An unknown error occured!'
            print_exception(err.original)
        elif isinstance(err, (errors.CheckFailure, errors.CheckAnyFailure)):
            output = 'Command is currently unavailable!'
        elif isinstance(err, errors.CommandError):
            output = str(err)
        else:
            output = 'An unknown error occured!'
            print_exception(err)

        message = await ctx.send(f'```{output}```')

        if not isinstance(err, commands.CommandOnCooldown):
            timeout = Client.error_timeout
        else:
            timeout = err.retry_after

        await self.wait_to_delete(message, timeout)

    async def wait_to_delete(self, msg: discord.Message, wait_for: int):
        if not isinstance(msg.channel, discord.TextChannel): return
        # need to check if bot can acutally delete the message

        await asyncio.sleep(wait_for)

        try:
            await msg.delete()
        except discord.errors.NotFound: # things change...
            pass

    def load_cogs(self):
        """Loads cogs (modules) individually without halting program"""

        for file in os.listdir('cogs'):
            if not file.endswith('.py'):
                continue

            name = file.replace('.py', '')

            try:
                self.load_extension(f'cogs.{name}')
            except Exception as e:
                print(f'Failed to load extension {name}: {e}')

    def to_task(self, ctx: commands.Context|None, fn: Callable) -> asyncio.Task:
        """Default method for creating new tasks in blocking code"""

        task = self.loop.create_task(fn())
        task.add_done_callback(partial(self._task_handler, ctx))

        return task

    def to_thread(self, ctx: commands.Context|None, fn: Callable) -> asyncio.Future:
        """Reserve for I/O bottlenecked tasks"""

        thread = self.loop.run_in_executor(self.thread_pool, fn)
        thread.add_done_callback(partial(self._task_handler, ctx))

        return thread

    def _task_handler(self, ctx: commands.Context, future: asyncio.Task|asyncio.Future):
        """Future / Task callback for exposing hidden runtime errors"""

        if err := future.exception():
            if isinstance(ctx, commands.Context):
                self.dispatch('command_error', ctx, err)
            else:
                print_exception(err)

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True

    bot = Bot(
        command_prefix=Client.prefix,
        description=Client.description,
        intents=intents
    )

    bot.run(Client.token)