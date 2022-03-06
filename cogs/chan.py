# Resources
# https://basc-py4chan.readthedocs.io/

import html
from typing import Tuple
import discord
import basc_py4chan
from random import shuffle, choice
from discord.ext import commands
from functools import partial

IMAGE_EXTS = frozenset({'.jpeg', '.jpg', '.png', '.gif'})
VIDEO_EXTS = frozenset({'.gif', '.webm', '.mp4'})

class Chan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = bot.loop

    @commands.is_nsfw()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.command(name='rp', brief='Random 4chan NSFW Post')
    @commands.has_permissions(send_messages=True)
    async def _random_nsfw(self, ctx):
        self.bot.to_thread(ctx, partial(self.random_post, ctx))

    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.command(name='rs', brief='Random 4chan SFW Post')
    @commands.has_permissions(send_messages=True)
    async def _random_sfw(self, ctx):
        self.bot.to_thread(ctx, partial(self.random_post, ctx, sfw=True))

    @commands.is_nsfw()
    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.command(name='rg', brief='Random 4chan /gif/')
    @commands.has_permissions(send_messages=True)
    async def _random_gif(self, ctx):
        self.bot.to_thread(ctx, partial(self.random_gif, ctx))

    @commands.cooldown(1, 7, commands.BucketType.user)
    @commands.command(name='rw', brief='Random 4chan /wsg/')
    @commands.has_permissions(send_messages=True)
    async def _random_wsg(self, ctx):
        self.bot.to_thread(ctx, partial(self.random_gif, ctx, sfw=True))

    def to_embed(self, board, post):
        title = f'/{board.name}/ No. {post.post_id}'
        color = 0xFFCCAA if not board.is_worksafe else 0xEEF2FF
        embed = discord.Embed(title=title, description=post.text_comment,
            colour=color, url=post.url, timestamp=post.datetime)
        
        if post.has_file:
            embed.set_image(url=post.file.file_url)
            
        name = html.unescape(post.name)

        if post.tripcode:
            name += f' {post.tripcode}'

        embed.set_footer(text=name)
        
        return embed

    def iter_random_posts(self, board, *, min_posts=14, has_file=False):
        thread_ids = board.get_all_thread_ids()
        shuffle(thread_ids)

        for thread in (board.get_thread(x) for x in thread_ids):
            if thread.sticky or len(thread.all_posts) <= min_posts:
                 continue

            shuffle(thread.all_posts)

            for post in thread.all_posts:
                if has_file and not post.has_file: continue
                yield post

    def _random(self, boards, *, text=True, image=True, video=True):
        found = False

        for board in boards:
            for post in self.iter_random_posts(board, has_file=True):
                ext = post.file.file_extension

                if image and ext in IMAGE_EXTS:
                    found = True
                elif video and ext in VIDEO_EXTS:
                    found = True
                elif text and post.text_comment:
                    found = True

                if found:
                    return (board, post)

        raise commands.CommandError('Could not find a post!')

    def random_post(self, ctx, *, sfw=False):
        boards = basc_py4chan.get_all_boards()
        if sfw: boards = [x for x in boards if x.is_worksafe]
        shuffle(boards)

        board, post = self._random(boards, video=False)
        self.bot.to_task(ctx, partial(ctx.send, embed=self.to_embed(board, post)))

    def random_gif(self, ctx, sfw=False):
        if not sfw:
            boards = basc_py4chan.get_boards(['gif'])
        else:
            boards = basc_py4chan.get_boards(['wsg'])

        _, post = self._random(boards, text=False, image=False)
        self.bot.to_task(ctx, partial(ctx.send, content=post.file.file_url))
        
def setup(bot):   
    bot.add_cog(Chan(bot))
    