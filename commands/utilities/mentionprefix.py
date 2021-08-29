import simplejson as json
import functions
from discord.ext import commands


class Mention(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            lang = functions.getLang.getLang(message.guild.id)
            with open("serverconfig/prefixes.json", "r") as f:
                prefix = json.load(f)[str(message.guild.id)]
            with open(f"embeds/{lang}/mentionPrefix.json", "r") as f:
                msg = json.load(f)

            await message.reply(msg.replace("%VAR", prefix), mention_author=False)


def setup(client):
    client.add_cog(Mention(client))
