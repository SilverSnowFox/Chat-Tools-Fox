import json

import discord
from discord.ext import commands
from functions.getLang import getLang


class Userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Userinfo", "user", "User"])
    async def userinfo(self, ctx, user: discord.Member = None):
        lang = getLang(ctx.message.guild.id)

        if user is None:
            user = ctx.author

        print(user.created_at)

        with open(f"embeds/{lang}/userinfo.json", "r") as f:
            data = json.load(f)


def setup(client):
    client.add_cog(Userinfo(client))
