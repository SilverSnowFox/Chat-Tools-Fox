import json
from discord.ext import commands


class GuildEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Add guild to prefix list
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('serverconfig/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "="

        with open('serverconfig/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    # Remove guild from prefix list
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


def setup(client):
    client.add_cog(GuildEvents(client))
