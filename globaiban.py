"""
GlobaIban plugin for Unifier - prank your friends
Copyright (C) 2024  Green

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord
from discord.ext import commands
import time

class GlobaiBan(commands.Cog):
    """we do a lil trolling"""
    
    def __init__(self,bot):
        self.bot = bot

    @commands.command(hidden=True,name='globaIban')
    async def globaiban(self,ctx,*,target):
        if not ctx.author.id in self.bot.moderators:
            return
        reason = ''
        parts = target.split(' ')
        forever = False
        if len(parts) >= 2:
            if len(parts)==2:
                reason = ''
            else:
                reason = target.replace(f'{parts[0]} {parts[1]} ','',1)
            target = parts[0]
            duration = parts[1]
            if (duration.lower()=='inf' or duration.lower()=='infinite' or
                duration.lower()=='forever' or duration.lower()=='indefinite'):
                forever = True
                duration = 0
            else:
                try:
                    duration = timetoint(duration)
                except:
                    return await ctx.send('Invalid duration!')
        else:
            return await ctx.send('Invalid duration!')
        try:
            userid = int(target.replace('<@','',1).replace('!','',1).replace('>','',1))
        except:
            userid = target
            if not len(userid) == 26:
                return await ctx.send('Invalid user/server!')
        if userid in self.bot.moderators and not ctx.author.id == self.bot.config['owner']:
            return await ctx.send('You cannot punish other moderators!')
        obvious = False
        if '-obvious' in reason:
            obvious = True
            reason = reason.replace('-obvious','',1)
            if reason.startswith(' '):
                reason = reason.replace(' ','',1)
        ct = round(time.time())
        nt = ct + duration
        if forever:
            nt = 0
        if ctx.author.discriminator=='0':
            mod = f'@{ctx.author.name}'
        else:
            mod = f'{ctx.author.name}#{ctx.author.discriminator}'
        if reason=='':
            embed = discord.Embed(title=f'You\'ve been __global restricted__ by {mod}!',description=f'no reason given',color=0xffcc00)
        else:
            embed = discord.Embed(title=f'You\'ve been __global restricted__ by {mod}!',description=reason,color=0xffcc00)
        if obvious:
            embed.title = 'This is a global restriction TEST!'
            embed.colour = 0x00ff00
        embed.set_author(name=mod,icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        if obvious:
            if forever:
                embed.add_field(name='Actions taken',value=f'- :white_check_mark: NOTHING - this is only a test! ("Expiry" should be never, otherwise something is wrong.)',inline=False)
            else:
                embed.add_field(name='Actions taken',value=f'- :white_check_mark: NOTHING - this is only a test! ("Expiry" should be <t:{nt}:R>, otherwise something is wrong.)',inline=False)
        else:
            if forever:
                embed.colour = 0xff0000
                embed.add_field(name='Actions taken',value=f'- :zipper_mouth: Your ability to text and speak have been **restricted indefinitely**. This will not automatically expire.\n- :white_check_mark: You must contact a moderator to appeal this restriction.',inline=False)
            else:
                embed.add_field(name='Actions taken',value=f'- :warning: You have been **warned**. Further rule violations may lead to sanctions on the Unified Chat global moderators\' discretion.\n- :zipper_mouth: Your ability to text and speak have been **restricted** until <t:{nt}:f>. This will expire <t:{nt}:R>.',inline=False)
        user = self.bot.get_user(userid)
        if obvious:
            embed.set_footer(text='Please send what you see to the developers!')
        else:
            embed.set_footer(text='lol just kidding ;)')
        if not user:
            try:
                user = self.bot.revolt_client.get_user(userid)
                return await user.send(f'## {embed.title}\n{embed.description}\n\n**Actions taken**\n{embed.fields[0].value}\n\n{embed.footer.text}')
            except:
                return
        if not user==None:
            try:
                await user.send(embed=embed)
            except:
                return await ctx.send('target has their dms with bot off, sadge')
        await ctx.send('hehe')

def setup(bot):
    bot.add_cog(GlobaiBan(bot))
