import discord
import simplejson as json
import functions.servermodules
from discord.ext import commands


class Scamlink(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if functions.servermodules.getConfig(message.guild.id, "anti_scam"):
            with open("serverconfig/ScamLinks.json", "r") as f:
                links = json.load(f)

            for link in links:
                if link in message.content:
                    lang = functions.getLang.getLang(message.guild.id)
                    with open(f"embeds/{lang}/scam.json", "r") as f:
                        embed = json.load(f)

                    embed['description'].replace("%VAR", message.author.mention)
                    print(embed['description'])

                    await message.channel.send(embed=discord.Embed.from_dict(embed))
                    await message.delete()
                    break

def setup(client):
    client.add_cog(Scamlink(client))
