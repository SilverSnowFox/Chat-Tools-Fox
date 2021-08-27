import simplejson as json
import discord

from functions.getLang import getLang
from functions.replaceVar import replaceSingle
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Prefix"])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        # Change prefix
        with open('serverconfig/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        old_prefix = prefixes[str(ctx.guild.id)]
        prefixes[str(ctx.guild.id)] = prefix
        with open('serverconfig/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        # Get the server language
        lang = getLang(ctx.message.guild.id)

        # Get the embed of the right language and send with replaced variable
        with open(f"embeds/{lang}/prefix.json", "r") as f:
            embed = json.load(f)
        embed['description'] = replaceSingle(embed['description'], prefix)
        await ctx.send(embed=discord.Embed.from_dict(embed))

        # Logging embed
        log_embed = {
            "title": "Prefix",
            "color": 3974125,
            "description": f"`{old_prefix}` -> `{prefix}`",
            "author": {
                "name": f"{ctx.message.author.name} ({ctx.message.author.id})",
                "icon_url": ctx.message.author.avatar_url
            }
        }


    @prefix.error
    async def prefix_error(self, ctx, error):
        from functions.getLang import getLang
        lang = getLang(ctx.message.guild.id)

        if isinstance(error, commands.MissingPermissions):
            with open(f"embeds/{lang}/errors.json", "r") as f:
                errors = json.load(f)
            await ctx.send(embed=discord.Embed.from_dict(errors['admin-manage']))
        else:
            raise error


def setup(client):
    client.add_cog(Prefix(client))
