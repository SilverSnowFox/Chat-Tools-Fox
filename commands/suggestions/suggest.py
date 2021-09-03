import json
import discord
import functions
from discord.ext import commands


class Suggest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Suggest"], no_pm=True)
    async def suggest(self, ctx, *, suggestion=""):
        """Command when user sends a suggestion"""
        # Gets all text and errors in the right language
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/suggestion.json", "r") as f:
            suggestData = json.load(f)

        try:
            if suggestion == "" and len(ctx.message.attachments) == 0:
                await ctx.reply(embed=discord.Embed.from_dict(suggestData["MissingRequiredArgument"]), delete_after=20)
                return

            # Get suggestion channel
            suggestionCh = self.client.get_channel(functions.serverchannels.getChannel(ctx.guild.id, "suggestions"))

            embed = discord.Embed(colour=44288)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.name}", icon_url=ctx.author.avatar_url)
            embed.title = suggestData['title']

            # Create description, then insert text at top
            description = []
            if len(ctx.message.attachments) > 0:
                description = [attachment.url for attachment in ctx.message.attachments]

            if suggestion != "":
                description.insert(0, suggestion)
            embed.description = "\n".join(description)

            msg = await suggestionCh.send(embed=embed)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            await ctx.reply(content=suggestData['Confirmed'], mention_author=False, delete_after=20)

        # No set channel
        except commands.errors.CommandInvokeError:
            await ctx.reply(embed=discord.Embed.from_dict(suggestData["CommandInvokeError"]), delete_after=20)
        except AttributeError:
            await ctx.reply(embed=discord.Embed.from_dict(suggestData["CommandInvokeError"]), delete_after=20)


def setup(client):
    client.add_cog(Suggest(client))
