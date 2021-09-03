import discord
import simplejson as json
from discord.ext import commands
from functions import serverlogs, getLang
from datetime import datetime


class Users(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def log_user(self, member, type, channel, guild, before=None):
        """Creates the embed for the log and sends it to the right channel"""

        bot_user = ""
        if member.bot:
            bot_user = " (bot)"

        lang = getLang.getLang(guild.id)
        with open(f"embeds/{lang}/userLogs.json", "r") as f:
            logData = json.load(f)

        if type == "Join":
            # When a user joins the server
            description = member.mention
            logEmbed = discord.Embed(color=logData['Join']['Colour'])
            logEmbed.title = logData['Join']['Title']
            logEmbed.description = description

        elif type == "Leave":
            # When a user leaves the server
            description = member.mention
            logEmbed = discord.Embed(color=logData['Leave']['Colour'])
            logEmbed.title = logData['Leave']['Title']
            logEmbed.description = description

        elif type == "Update":
            # When a user changes name, discriminator or avatar
            logEmbed = discord.Embed(color=logData['Update']['Colour'])
            logEmbed.title = logData['Update']['Title']

            logEmbed.add_field(name=logData['Update']['Before'],
                               value=f"{before.name}#{before.discriminator}\n\n{before.nick}\n\n{', '.join([role.mention for role in before.roles])}",
                               inline=True)
            logEmbed.add_field(name=logData['Update']['After'],
                               value=f"{member.name}#{member.discriminator}\n\n{member.nick}\n\n{', '.join([role.mention for role in member.roles])}",
                               inline=True)

        elif type == "Ban":
            # When a user is banned
            description = member.mention

            logEmbed = discord.Embed(color=logData['Ban']['Colour'])
            logEmbed.title = logData['Ban']['Title']
            logEmbed.description = description

        elif type == "Unban":
            # When user is unbanned
            description = member.mention

            logEmbed = discord.Embed(color=logData['Unban']['Colour'])
            logEmbed.title = logData['Unban']['Title']
            logEmbed.description = description

        # Send message to log channel
        logEmbed.set_author(name=f"{member.name}{bot_user}", icon_url=member.avatar_url)
        logEmbed.set_thumbnail(url=member.avatar_url)
        logEmbed.timestamp = datetime.utcnow()
        await channel.send(embed=logEmbed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """When a user is banned"""
        channel = self.client.get_channel(serverlogs.getChannel(guild.id, "kick_ban"))
        if channel is not None:
            await self.log_user(member=user, type='Ban', channel=channel, guild=guild)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """When a user is unbanned"""
        channel = self.client.get_channel(serverlogs.getChannel(guild.id, "kick_ban"))
        if channel is not None:
            await self.log_user(member=user, type='Unban', channel=channel, guild=guild)

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member):
        """When a member joined the server"""
        channel = self.client.get_channel(serverlogs.getChannel(member.guild.id, "join_leave"))
        if channel is not None:
            await self.log_user(member=member, type='Join', channel=channel, guild=member.guild)

    @commands.Cog.listener('on_member_remove')
    async def on_member_remove(self, member):
        """When a user leaves the server"""
        channel = self.client.get_channel(serverlogs.getChannel(member.guild.id, "join_leave"))
        if channel is not None:
            await self.log_user(member=member, type='Leave', channel=channel, guild=member.guild)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """When a user updates their profile"""
        if before == after:
            return 0
        # Avatar, username, discriminator
        channel = self.client.get_channel(serverlogs.getChannel(before.guild.id, "user_change"))
        if channel is not None:
            await self.log_user(member=after, type='Update', channel=channel, guild=before.guild, before=before)


def setup(client):
    client.add_cog(Users(client))
