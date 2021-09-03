import json
import discord
import time
from datetime import timedelta
from discord.ext import commands
from functions.getLang import getLang
from discord import Button, ButtonStyle

startTime = time.time()


class Botinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Botinfo"])
    async def botinfo(self, ctx):
        """Sends the bot information"""
        lang = getLang(ctx.message.guild.id)

        with open(f"embeds/{lang}/botinfo.json", "r") as f:
            botcategories = json.load(f)

        with open(f"serverconfig/prefixes.json", "r") as f:
            prefixes = json.load(f)
            prefix = prefixes[str(ctx.message.guild.id)]

        embed = discord.Embed.from_dict(botcategories['embed'])
        embed.add_field(name=botcategories['fields'][0], value=f"{self.client.user.name}#{self.client.user.discriminator} ({self.client.user.id})", inline=False)
        embed.add_field(name=botcategories['fields'][1], value=prefix)
        embed.add_field(name=botcategories['fields'][2], value=f"{round(self.client.latency * 1000)} ms")
        embed.add_field(name=botcategories['fields'][3], value=f"{len(self.client.guilds)}")
        embed.add_field(name=botcategories['fields'][4], value=f"{timedelta(seconds=round(time.time() - startTime))}")
        embed.add_field(name=botcategories['fields'][5], value="SevenTails#7757", inline=False)
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.reply(embed=embed, components=[Button(
            label=botcategories['button'],
            url="https://discord.com/api/oauth2/authorize?client_id=878533674042294292&permissions=8&scope=bot",
            style=ButtonStyle.url
        )], mention_author=False, delete_after=20)


def setup(client):
    client.add_cog(Botinfo(client))
