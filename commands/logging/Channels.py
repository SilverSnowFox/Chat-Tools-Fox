import discord
import simplejson as json
from discord.ext import commands
from functions import serverlogs, getLang
from datetime import datetime


class Channels(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def log_channel(self, ch, type, channel, guild):
        """Creates the embed for the log and sends it to the right channel"""

        lang = getLang.getLang(guild.id)
        with open(f"embeds/{lang}/roleLogs.json", "r") as f:
            logData = json.load(f)

        if type == "Create":
            logEmbed = discord.Embed(color=logData['Create']['Colour'])
            logEmbed.title = logData['Create']['Title']
            description = ch.mention

        elif type == "Delete":
            logEmbed = discord.Embed(color=logData['Delete']['Colour'])
            logEmbed.title = logData['Delete']['Title']
            description = ch.mention

        elif type == "Update":
            logEmbed = discord.Embed(color=logData['Update']['Colour'])
            logEmbed.title = logData['Update']['Title']
            description = ch.mention

        # Send message to log channel
        logEmbed.description = description
        logEmbed.timestamp = datetime.utcnow()
        await channel.send(embed=logEmbed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ch):
        """When a role is created"""
        channel = self.client.get_channel(serverlogs.getChannel(ch.guild.id, "channel"))
        if channel is not None:
            await self.log_channel(ch=ch, type='Create', channel=channel, guild=ch.guild)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, ch):
        """When a role is created"""
        channel = self.client.get_channel(serverlogs.getChannel(ch.guild.id, "channel"))
        if channel is not None:
            await self.log_channel(ch=ch, type='Delete', channel=channel, guild=ch.guild)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """When a role is updated"""
        channel = self.client.get_channel(serverlogs.getChannel(after.guild.id, "channel"))
        if channel is not None:
            await self.log_channel(ch=after, type='Update', channel=channel, guild=after.guild)


def setup(client):
    client.add_cog(Channels(client))
