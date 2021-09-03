import discord
import simplejson as json
import functions
from discord.ext import commands


class Ghostping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Event when user pings someone else and then deletes ping"""
        # Check that mentions have no bots
        def check_only_bot(m):
            for mention in m.mentions:
                if not mention.bot:
                    return False
            return True

        try:
            if functions.servermodules.getConfig(message.guild.id, "ghost_ping"):
                if message.mentions[0] == message.author or message.author.bot or check_only_bot(message):
                    return
                lang = functions.getLang.getLang(message.guild.id)
                with open(f"embeds/{lang}/ghost_ping.json", "r") as f:
                    data = json.load(f)

                embed = discord.Embed.from_dict(data['embed'])
                embed.add_field(name=data['fields'][0],
                                value=message.channel.mention, inline=True)
                embed.add_field(name=data['fields'][1],
                                value=" ".join([f'<@!{user.id}>' for user in message.mentions]),
                                inline=True)
                embed.set_author(name=f'{message.author.name}#{message.author.discriminator}',
                                 icon_url=message.author.avatar_url)

                await message.channel.send(embed=embed)
        except Exception as error:
            if isinstance(error, IndexError):
                pass
            else:
                raise error


def setup(client):
    client.add_cog(Ghostping(client))
