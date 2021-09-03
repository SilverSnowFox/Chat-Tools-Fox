import discord
import simplejson as json
from functions import serverlogs, getLang
from discord.ext import commands


class ShowLogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Show-logs", "show-logs"])
    @commands.has_permissions(manage_guild=True)
    async def show_logs(self, ctx):
        users = serverlogs.getChannel(ctx.guild.id, "join_leave")
        channels = serverlogs.getChannel(ctx.guild.id, "channel")
        roles = serverlogs.getChannel(ctx.guild.id, "roles")
        messages = serverlogs.getChannel(ctx.guild.id, "msg_edit")
        scam = serverlogs.getChannel(ctx.guild.id, "scam")

        def channel(channel):
            if self.client.get_channel(channel) is not None:
                return self.client.get_channel(channel).mention
            return "`None`"

        description = f"Users: {channel(users)}\nChannels: {channel(channels)}\nRoles: {channel(roles)}\nMessages: {channel(messages)}\nScam: {channel(scam)}"
        embed = discord.Embed(color=discord.Colour.gold())
        embed.title = "Logs"
        embed.description = description
        await ctx.reply(embed=embed, mention_author=False, delete_after=20)

    @show_logs.error
    async def show_logs_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            lang = getLang.getLang(ctx.guild.id)
            with open(f"embeds/{lang}/showLogs.json", "r") as f:
                logData = json.load(f)
            await ctx.reply(embed=discord.Embed.from_dict(logData['Invalid-channel']),
                            mention_author=False, delete_after=20)


def setup(client):
    client.add_cog(ShowLogs(client))
