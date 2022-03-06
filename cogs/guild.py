import json
from datetime import datetime, date, timedelta
from discord.ext import tasks, commands
from collections import Counter

from utils.duration import td_to_str
from config import Paths

is_guild = lambda x: x.guild is not None

class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = self.bot.loop
        self.log_dir = Paths.base / 'logs'

        self.log_users.start()

    # the times are wrong here... either Discord or discord.py is fucked
    @commands.cooldown(1, 7, commands.BucketType.guild)
    @commands.command(name='age', brief="A member's age")
    @commands.has_permissions(send_messages=True)
    @commands.check(is_guild)
    async def _get_age(self, ctx):
        now = datetime.utcnow()

        if len(ctx.message.mentions) > 0:
            members = ctx.message.mentions
        else:
            members = [ctx.message.author]

        for m in members:
            td = td_to_str(now - m.joined_at)
            await ctx.send(f'**{m.display_name}** has been here for:\n```{td}```')

    @commands.cooldown(1, 7, commands.BucketType.guild)
    @commands.command(name='up', alias='uptime', brief="The server's age")
    @commands.has_permissions(send_messages=True)
    @commands.check(is_guild)
    async def _get_uptime(self, ctx):
        td = td_to_str(datetime.utcnow() - ctx.guild.created_at)
        await ctx.send(f'**{ctx.guild.name}** has been around for:\n```{td}```')

    @commands.cooldown(1, 7, commands.BucketType.guild)
    @commands.command(name='all', alias='members', brief='All members by age')
    @commands.has_permissions(send_messages=True)
    @commands.check(is_guild)
    async def _get_members(self, ctx):
        out = []
        now = datetime.utcnow()
        members = sorted(ctx.guild.members, key=lambda x: x.joined_at)
        counts = Counter([x.display_name for x in members])

        for i, m in enumerate(members, start=1):
            td = td_to_str(now - m.joined_at, max_only=True)

            if counts[m.display_name] == 1:
                nick = m.display_name
            else:
                nick = f'{m.name}#{m.discriminator}'

            pos = f'[{i}]'

            out.append(f'{pos:>5} {nick} [{td}]')

        if not out:
            raise commands.CommandError('Oopsie!')

        await ctx.send('```ini\n{}\n```'.format('\n'.join(out)))
    
    # switch to database eventually
    def _log_users(self):
        for guild in self.bot.guilds:
            log_file = self.log_dir / f'{guild.name}.json'
            log_data = {}

            with open(log_file, 'a+', encoding='utf-8', newline='\n') as fp:
                try:
                    log_data = json.load(fp)
                except json.decoder.JSONDecodeError:
                    log_data = {}

                fp.truncate(0)

                if guild.id not in log_data:
                    log_data[guild.id] = {}
                    
                log_data[guild.id]['name'] = guild.name
                log_data[guild.id]['description'] = guild.description
                log_data[guild.id]['created_at'] = guild.created_at.isoformat()

                if 'members' not in log_data[guild.id]:
                    log_data[guild.id]['members'] = {}

                for member in guild.members:
                    log_data[guild.id]['members'][str(member.id)] = {
                        'bot': member.bot,
                        'name': member.name,
                        'discriminator': member.discriminator,
                        'nick': member.nick,
                        'joined_at': member.joined_at.isoformat(),
                        'created_at': member.created_at.isoformat(),
                    }

                json.dump(log_data, fp, indent=4, ensure_ascii=False)

    @tasks.loop(hours=14)
    async def log_users(self):
        self.loop.run_in_executor(None, self._log_users)

    @log_users.before_loop
    async def log_users_wait(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.log_users.cancel()

def setup(bot):
    bot.add_cog(Guild(bot))
