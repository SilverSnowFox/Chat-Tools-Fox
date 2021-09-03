import discord
import simplejson as json
from discord.ext import commands

import functions.serverlogs
from functions import servermodules, getLang


class Scamlink(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True)
    async def on_message(self, message):
        """Module against scams"""
        # No PM and check the module is enabled
        if message.guild is None or not servermodules.getConfig(message.guild.id, "anti_scam"):
            return

        lang = getLang.getLang(message.guild.id)
        with open(f"embeds/{lang}/antiScam.json", "r") as f:
            scamData = json.load(f)

        try:
            with open("serverconfig/ScamLinks.json", "r") as f:
                links = json.load(f)

            # Checks for each link and stops at the first found
            for link in links:
                if link in message.content:
                    embed = scamData['embed']
                    embed['description'] = embed['description'].replace("%VAR", message.author.mention)
                    await message.channel.send(embed=discord.Embed.from_dict(embed))
                    await message.delete()

                    logChannel = self.client.get_channel(functions.serverlogs.getChannel(message.guild.id, "scam"))
                    if logChannel is not None:
                        logEmbed = discord.Embed.from_dict(embed)
                        logEmbed.add_field(name=scamData['Field'], value=message.content)
                        await logChannel.send(embed=logEmbed)
                    break

        except commands.errors.BotMissingPermissions:
            await message.channel.send(embed=discord.Embed.from_dict(scamData['BotMissingPermissions']))
        except:
            raise Exception


def setup(client):
    client.add_cog(Scamlink(client))
