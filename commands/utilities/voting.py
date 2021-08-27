import discord
import simplejson as json
from functions.getLang import getLang
from discord.ext import commands
from discord import ActionRow, Button, ButtonStyle


class Vote(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Vote"])
    async def vote(self, ctx):
        lang = getLang(ctx.message.guild.id)

        with open(f"embeds/{lang}/vote.json", "r") as f:
            voting = json.load(f)

        await ctx.send(embed=discord.Embed.from_dict(voting), components=[ActionRow(
            Button(label="Top.gg", url="https://bit.do/YeetYeet", style=ButtonStyle.url),
            Button(label="DisBotList.xyz", url="https://bit.do/YeetYeet", style=ButtonStyle.url)
        )])


def setup(client):
    client.add_cog(Vote(client))