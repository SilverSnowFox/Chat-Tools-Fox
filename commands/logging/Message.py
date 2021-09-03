import discord
import simplejson as json
import datetime
from functions import serverlogs, getLang
from discord.ext import commands


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def log_message(self, message, type, channel, before=None, attachments_old=None):
        """Gather information from the message and format it before
        sending it to message log channel
        """

        # Differentiate between bots and normal users
        bot_user = ""
        if message.author.bot:
            bot_user = " (bot)"

        # Check for attachments in the message
        # Discord for desktop and web do not have the ability to send
        # multiple images within the same message. However, this is
        # possible on the mobile versions of discord and through bots.
        try:
            attachments = ""
            count = 1
            for a in message.attachments:
                attachments += f"\n[Attachment {count}]({a.url})"
                count += 1
        except Exception:
            attachments = ""

        lang = getLang.getLang(message.guild.id)
        with open(f"embeds/{lang}/msgLogs.json", "r") as f:
            logData = json.load(f)

        # Action dependent
        description = ""
        if type == 'Edited':

            description = logData['Edit']['Description'].replace("%VAR1", before.content)
            description = description.replace("%VAR2", attachments_old)
            description = description.replace("%VAR3", message.content)
            description = description.replace("%VAR4", attachments)
            description = description.replace("%VAR5", message.channel.mention)
            description += f"\n[Link]({message.jump_url})"

            logEmbed = discord.Embed(color=logData['Edit']['Colour'])
            logEmbed.title = logData['Edit']['Title']

        elif type == 'Deleted':

            description = logData['Delete']['Description'].replace("%VAR1", message.content)
            description = description.replace("%VAR2", attachments)
            description = description.replace("%VAR3", message.channel.mention)
            description += f"\n[Link]({message.jump_url})"

            logEmbed = discord.Embed(color=logData['Delete']['Colour'])
            logEmbed.title = logData['Delete']['Title']

        elif type == "Pinned":

            description = logData['Pinned']['Description'].replace("%VAR1", message.content)
            description = description.replace("%VAR2", attachments)
            description = description.replace("%VAR3", message.channel.mention)
            description += f"\n[Link]({message.jump_url})"

            logEmbed = discord.Embed(color=logData['Pinned']['Colour'])
            logEmbed.title = logData['Pinned']['Title']

        # Send message to log channel
        logEmbed.description = description
        logEmbed.set_author(name=f"{message.author.name}{bot_user}", icon_url=message.author.avatar_url)
        logEmbed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=logEmbed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Detect Messages Deleted"""

        # Avoids logging self or PM
        if message.author.id == self.client.user.id or message.guild is None:
            return 0

        # Makes sure that channel is correctly set
        channel = self.client.get_channel(serverlogs.getChannel(message.guild.id, "msg_delete"))
        if channel is not None:
            await self.log_message(message=message, type='Deleted', channel=channel)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Logs message pins"""
        # Avoids logging self or PM
        if before.author.id == self.client.user.id or before.guild is None:
            return 0

        channel = self.client.get_channel(serverlogs.getChannel(before.guild.id, "msg_pin"))
        if not before.pinned and after.pinned and before.content == after.content:
            if channel is not None:
                await self.log_message(message=after, type='Pinned', channel=channel)
        elif before.pinned and not after.pinned:
            return 0
        elif channel is not None:

            # Check for any attachments in the old message. The new message
            # will be checked in log_message()
            try:
                attachments_old = ""
                count = 1
                for a in before.attachments:
                    attachments_old += f"\n[Attachment {count}]({a.url})"
                    count += 1
            except Exception:
                attachments_old = ""

            await self.log_message(message=after, type='Edited', before=before,
                                   attachments_old=attachments_old, channel=channel)


def setup(client):
    client.add_cog(Messages(client))
