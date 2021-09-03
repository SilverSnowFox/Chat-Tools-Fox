import discord
import simplejson as json
from functions import serverlogs, getLang
from discord.ext import commands


class Log(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Log"])
    @commands.has_permissions(administrator=True)
    async def log(self, ctx, type, channel: discord.TextChannel=None):
        """Sets up the channels to the logs"""

        lang = getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/log.json", "r") as f:
            logData = json.load(f)

        if type == "types":
            await ctx.reply(embed=discord.Embed.from_dict(logData['Types']), mention_author=False, delete_after=20)

        elif channel is not None:
            if type == "messages":
                serverlogs.updateModule(ctx.guild.id, "msg_delete", channel.id)
                serverlogs.updateModule(ctx.guild.id, "msg_edit", channel.id)
                serverlogs.updateModule(ctx.guild.id, "msg_pin", channel.id)

                logEmbed = discord.Embed(color=3974125)
                logEmbed.title = logData['Messages']['title']
                logEmbed.description = logData['Messages']['description'].replace("%VAR", channel.mention)
            elif type == "channels":
                serverlogs.updateModule(ctx.guild.id, "channel", channel.id)

                logEmbed = discord.Embed(color=3974125)
                logEmbed.title = logData['Channels']['title']
                logEmbed.description = logData['Channels']['description'].replace("%VAR", channel.mention)
            elif type == "users":
                serverlogs.updateModule(ctx.guild.id, "join_leave", channel.id)
                serverlogs.updateModule(ctx.guild.id, "user_change", channel.id)
                serverlogs.updateModule(ctx.guild.id, "kick_ban", channel.id)

                logEmbed = discord.Embed(color=3974125)
                logEmbed.title = logData['Users']['title']
                logEmbed.description = logData['Users']['description'].replace("%VAR", channel.mention)
            elif type == "roles":
                serverlogs.updateModule(ctx.guild.id, "roles", channel.id)

                logEmbed = discord.Embed(color=3974125)
                logEmbed.title = logData['Roles']['title']
                logEmbed.description = logData['Roles']['description'].replace("%VAR", channel.mention)
            elif type == "scam":
                serverlogs.updateModule(ctx.guild.id, "scam", channel.id)

                logEmbed = discord.Embed(color=3974125)
                logEmbed.title = logData['Scam']['title']
                logEmbed.description = logData['Scam']['description'].replace("%VAR", channel.mention)
            elif type == "all":
                serverlogs.updateModule(ctx.guild.id, "msg_delete", channel.id)
                serverlogs.updateModule(ctx.guild.id, "msg_edit", channel.id)
                serverlogs.updateModule(ctx.guild.id, "msg_pin", channel.id)
                serverlogs.updateModule(ctx.guild.id, "channel", channel.id)
                serverlogs.updateModule(ctx.guild.id, "join_leave", channel.id)
                serverlogs.updateModule(ctx.guild.id, "user_change", channel.id)
                serverlogs.updateModule(ctx.guild.id, "kick_ban", channel.id)
                serverlogs.updateModule(ctx.guild.id, "roles", channel.id)
                serverlogs.updateModule(ctx.guild.id, "scam", channel.id)

                logEmbed = discord.Embed(color=3974125)
                logEmbed.title = logData['All']['title']
                logEmbed.description = logData['All']['description'].replace("%VAR", channel.mention)
            else:
                logEmbed = discord.Embed.from_dict(logData['Invalid-type'])
        else:
            logEmbed = discord.Embed.from_dict(logData['Invalid-channel'])

        await ctx.reply(embed=logEmbed, mention_author=False, delete_after=20)

    @log.error
    async def log_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            lang = getLang.getLang(ctx.guild.id)
            with open(f"embeds/{lang}/log.json", "r") as f:
                logData = json.load(f)
            await ctx.reply(embed=discord.Embed.from_dict(logData['Invalid-channel']),
                            mention_author=False, delete_after=20)


def setup(client):
    client.add_cog(Log(client))
