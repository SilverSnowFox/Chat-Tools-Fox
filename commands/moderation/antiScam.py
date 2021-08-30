import discord
import simplejson as json
import functions
from discord.ext import commands


class Scamlink(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True)
    async def on_message(self, message):

        # No PM and check the module is enabled
        if message.guild is None or not functions.servermodules.getConfig(message.guild.id, "anti_scam"):
            return

        lang = functions.getLang.getLang(message.guild.id)
        with open(f"embeds/{lang}/antiScam.json", "r") as f:
            scamData = json.load(f)

        try:
            with open("serverconfig/ScamLinks.json", "r") as f:
                links = json.load(f)

            # Checks for each link and stops at the first found
            for link in links:
                if link in message.content:
                    embed = scamData['embed']
                    embed['description'].replace("%VAR", message.author.mention)
                    await message.channel.send(embed=discord.Embed.from_dict(embed))
                    await message.delete()
                    break
        except commands.errors.BotMissingPermissions:
            await message.channel.send(embed=discord.Embed.from_dict(scamData['BotMissingPermissions']))
        except:
            raise Exception


def setup(client):
    client.add_cog(Scamlink(client))
