import discord
import simplejson as json
from functions.getLang import getLang
from discord.ext import commands


class Serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Serverinfo"], no_pm=True)
    async def serverinfo(self, ctx):
        """Returns an embed with the guild's information"""
        guild = ctx.message.guild
        lang = getLang(guild.id)

        with open(f"embeds/{lang}/serverinfo.json", "r") as f:
            data = json.load(f)

        embed = discord.Embed.from_dict(data['embed'])
        listItems = data['fields']

        embed.add_field(name=listItems[0], value=f'{guild.name} ({guild.id})', inline=False)
        embed.add_field(name=listItems[1], value=guild.member_count, inline=True)
        embed.add_field(name=listItems[2], value=len(guild.roles), inline=True)
        embed.add_field(name=listItems[3], value=len(guild.text_channels), inline=True)
        embed.add_field(name=listItems[4], value=len(guild.voice_channels), inline=True)
        embed.add_field(name=listItems[5], value=len(guild.emojis), inline=True)
        embed.add_field(name=listItems[6], value=guild.premium_subscription_count, inline=True)
        embed.add_field(name=listItems[7], value=f'<@!{guild.owner_id}>', inline=True)
        embed.add_field(name=listItems[8], value=guild.region, inline=True)
        embed.add_field(name=listItems[9], value=guild.created_at.date().strftime("%b %d, %Y"), inline=True)
        embed.add_field(name=listItems[10], value=guild.verification_level, inline=True)
        embed.set_thumbnail(url=guild.icon_url)

        await ctx.reply(embed=embed, mention_author=False, delete_after=30)


def setup(client):
    client.add_cog(Serverinfo(client))
