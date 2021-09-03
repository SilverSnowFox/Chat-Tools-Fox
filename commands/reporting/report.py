import time
import discord
import functions
import json
from discord.ext import commands


class Report(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Report"], no_pm=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def report(self, ctx, *, report=""):
        """Command when user sends a report"""
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/report.json", "r") as f:
            reportData = json.load(f)

        try:
            # Just to make sure that the sure sent at least text or an image
            if report == "" and len(ctx.message.attachments) == 0:
                await ctx.reply(embed=discord.Embed.from_dict(reportData["MissingRequiredArgument"]), delete_after=20)
                return

            # Get suggestion channel
            suggestionCh = self.client.get_channel(functions.serverchannels.getChannel(ctx.guild.id, "reports"))

            # Creates embed
            embed = discord.Embed(colour=15794176)
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.name}", icon_url=ctx.author.avatar_url)
            embed.title = reportData['title']

            # Create description, then insert text at top
            description = []
            if len(ctx.message.attachments) > 0:
                description = [attachment.url for attachment in ctx.message.attachments]

            if report != "":
                description.insert(0, report)
            embed.description = "\n".join(description)

            await suggestionCh.send(embed=embed)
            await ctx.reply(content=reportData['Confirmed'], mention_author=False)
            await ctx.message.delete()

        # No set channel
        except commands.errors.CommandInvokeError:
            await ctx.reply(embed=discord.Embed.from_dict(reportData["CommandInvokeError"]), delete_after=20)
            await ctx.message.delete()
        except commands.errors.BotMissingPermissions:
            await ctx.reply(embed=discord.Embed.from_dict(reportData["BotMissingPermissions"]), delete_after=20)
            await ctx.message.delete()

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandInvokeError):
            lang = functions.getLang.getLang(ctx.guild.id)
            with open(f"embeds/{lang}/report.json", "r") as f:
                await ctx.reply(embed=discord.Embed.from_dict(json.load(f)["CommandInvokeError"]), delete_after=20)
                await ctx.message.delete()
        else:
            raise error


def setup(client):
    client.add_cog(Report(client))
