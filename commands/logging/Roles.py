import discord
import simplejson as json
from discord.ext import commands
from functions import serverlogs, getLang
from datetime import datetime


class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def log_role(self, role, type, channel, guild):
        """Creates the embed for the log and sends it to the right channel"""

        lang = getLang.getLang(guild.id)
        with open(f"embeds/{lang}/roleLogs.json", "r") as f:
            logData = json.load(f)

        if type == "Create":
            logEmbed = discord.Embed(color=logData['Create']['Colour'])
            logEmbed.title = logData['Create']['Title']
            description = role.mention
        elif type == "Delete":
            logEmbed = discord.Embed(color=logData['Delete']['Colour'])
            logEmbed.title = logData['Delete']['Title']
            description = role.mention
        elif type == "Update":
            logEmbed = discord.Embed(color=logData['Update']['Colour'])
            logEmbed.title = logData['Update']['Title']
            description = role.mention

        # Send message to log channel
        logEmbed.description = description
        logEmbed.timestamp = datetime.utcnow()
        await channel.send(embed=logEmbed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """When a role is created"""
        channel = self.client.get_channel(serverlogs.getChannel(role.guild.id, "roles"))
        if channel is not None:
            await self.log_role(role=role, type='Create', channel=channel, guild=role.guild)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """When a role is created"""
        channel = self.client.get_channel(serverlogs.getChannel(role.guild.id, "roles"))
        if channel is not None:
            await self.log_role(role=role, type='Delete', channel=channel, guild=role.guild)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """When a role is updated"""
        if before == after:
            return 0
        channel = self.client.get_channel(serverlogs.getChannel(after.guild.id, "roles"))
        if channel is not None:
            await self.log_role(role=after, type='Update', channel=channel, guild=after.guild)


def setup(client):
    client.add_cog(Roles(client))
