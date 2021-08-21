import json
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Prefix"])
    async def prefix(self, ctx, prefix):
        if ctx.message.author.guild_permissions.administrator:
            with open('data/prefixes.json', 'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open('data/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
        else:
            await ctx.send("You need administration permissions to change the prefix")


def setup(client):
    client.add_cog(Prefix(client))
