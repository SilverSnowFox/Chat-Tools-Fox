import discord
import simplejson as json
import functions
from discord.ext import commands


class Set(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Set"])
    @commands.has_permissions(manage_guild=True)
    async def set(self, ctx, category, channel: discord.TextChannel):
        """Sets the guild Suggestion, Report or Improved Pins"""
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/set.json", "r") as f:
            setData = json.load(f)
        channelID = channel.id

        if category.lower() == "suggestions":
            functions.serverchannels.updateModule(ctx.guild.id, "suggestions", channelID)
            await ctx.reply(setData['Suggestions'].replace('%VAR', channel.mention), delete_after=20)
        elif category.lower() == "reports":
            functions.serverchannels.updateModule(ctx.guild.id, "reports", channelID)
            await ctx.reply(setData['Reports'].replace('%VAR', channel.mention), delete_after=20)
        elif category.lower() == "improved-pins":
            functions.serverchannels.updateModule(ctx.guild.id, "pins", channelID)
            await ctx.reply(setData['ImprovedPins'].replace('%VAR', channel.mention), delete_after=20)

        # Invalid category
        else:
            await ctx.reply(embed=discord.Embed.from_dict(setData['InvalidCategory']), mention_author=False, delete_after=20)

    @set.error
    async def set_error(self, ctx, error):
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/set.json", "r") as f:
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
    client.add_cog(Set(client))
