import discord
from datetime import datetime
from functools import partial
from collections import deque
from urllib.parse import urlparse
from discord.ext import commands, tasks

from config import Client
from utils.internet import Download

class Archive(commands.Cog):
    volatile = (
        '4cdn.org',
        '4chan.org',
        '4channel.org',
        'cdn.discordapp.com',
        'i.redd.it',
        '8kun.top',
        '7chan.org',
        '2chan.net'
    ) # Most likely to least likely

    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.uploaded = {} # only meant to prevent abuse
        self.reset.start()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return
        if not isinstance(msg.channel, discord.TextChannel): return
        if not msg.content.startswith('http', 0, 4): return

        self.bot.to_thread(None, partial(self.archive, msg=msg))

    @tasks.loop(hours=21)
    async def reset(self):
        self.uploaded = {}

    def cog_unload(self):
        if self.reset.is_running():
            self.reset.cancel()

    def archive(self, msg):
        url = msg.content
        parsed = urlparse(url)
        guild = msg.channel.guild
        channel = msg.channel
        content = f'🔄 Posted by {msg.author.mention} from:\n```{url}```'

        if 'http' not in parsed.scheme: return
        if not any((x for x in self.volatile if x in parsed.netloc)): return

        if guild.id not in self.uploaded:
            self.uploaded[guild.id] = deque(maxlen=128)
        else:
            if url in self.uploaded[guild.id]: return

        with Download(url, max_size=Client.upload_limit) as dl:
            dl = Download(url)

            if not dl.is_media: return

            dl.get()

        task = self.bot.to_task(None, partial(channel.send, content=content,
            file=discord.File(dl, filename=dl.name)))
        task.add_done_callback(partial(self._callback, url, msg))

    def _callback(self, url, msg, _):
        if isinstance(msg.channel, discord.TextChannel):
            self.loop.create_task(msg.delete())

        self.uploaded[msg.channel.guild.id].append(url)

    @reset.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Archive(bot))
