import simplejson as json
import discord
from functions.getLang import getLang
from discord.ext import commands
from discord import Button, ButtonStyle


class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Invite"])
    async def invite(self, ctx):
        lang = getLang(ctx.message.guild.id)

        with open(f"embeds/{lang}/inviting.json", "r") as f:
            inviting = json.load(f)

        await ctx.reply(embed=discord.Embed.from_dict(inviting[0]), components=[
            Button(label=inviting[1],
                   url="https://discord.com/api/oauth2/authorize?client_id=878533674042294292&permissions=8&scope=bot",
                   style=ButtonStyle.url
                   )
        ], mention_author=False)


def setup(client):
    client.add_cog(Invite(client))
