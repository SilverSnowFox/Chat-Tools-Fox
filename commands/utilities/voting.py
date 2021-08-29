import discord
import simplejson as json
import time
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

        embed = discord.Embed.from_dict(voting)
        embed.set_thumbnail(url=self.client.user.avatar_url)

        msg = await ctx.reply(embed=embed, components=[ActionRow(
            Button(label="Top.gg", url="https://bit.do/YeetYeet", style=ButtonStyle.url),
            Button(label="DisBotList.xyz", url="https://bit.do/YeetYeet", style=ButtonStyle.url),
        )], mention_author=False)
        time.sleep(60)
        await msg.edit(embed=embed, components=[ActionRow(
            Button(label="Top.gg", url="https://bit.do/YeetYeet", style=ButtonStyle.url),
            Button(label="DisBotList.xyz", url="https://bit.do/YeetYeet", style=ButtonStyle.url),
        ).disable_all_buttons()], mention_author=False)


def setup(client):
    client.add_cog(Vote(client))