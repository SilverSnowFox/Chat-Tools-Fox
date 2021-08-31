import discord
import functions
import simplejson as json
from discord.ext import commands


class Remove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Remove"])
    @commands.has_permissions(manage_guild=True)
    async def remove(self, ctx, category):
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/remove.json", "r") as f:
            setData = json.load(f)

        if category.lower() == "suggestions":
            functions.serverchannels.updateModule(ctx.guild.id, "suggestions", 0)
            await ctx.reply(setData['Suggestions'], delete_after=20)
        elif category.lower() == "reports":
            functions.serverchannels.updateModule(ctx.guild.id, "reports", 0)
            await ctx.reply(setData['Reports'], delete_after=20)
        elif category.lower() == "improved-pins":
            functions.serverchannels.updateModule(ctx.guild.id, "pins", 0)
            await ctx.reply(setData['ImprovedPins'], delete_after=20)

        # Invalid category
        else:
            await ctx.reply(embed=discord.Embed.from_dict(setData['InvalidCategory']), mention_author=False,
                            delete_after=20)

    @remove.error
    async def set_error(self, ctx, error):
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/remove.json", "r") as f:
            setData = json.load(f)

        # Missing an argument
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(embed=discord.Embed.from_dict(setData['MissingRequiredArgument']), delete_after=20)

        # Missing manage guild permissions
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply(embed=discord.Embed.from_dict(setData['MissingPermissions']), delete_after=20)
        else:
            raise error


def setup(client):
    client.add_cog(Remove(client))
