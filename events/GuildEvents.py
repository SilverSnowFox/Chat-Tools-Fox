import json
from discord.ext import commands
import discord


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

        with open('serverconfig/lang.json', 'r') as f:
            language = json.load(f)
        language[str(guild.id)] = 'EN'
        with open('serverconfig/lang.json', 'w') as f:
            json.dump(language, f, indent=4)

        channel = discord.Client.get_channel(self.client, id=880568567702110258)
        await channel.send(f'Joined {guild.name} ({guild.id})')

    # Remove guild from prefix list
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('serverconfig/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('serverconfig/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        with open('serverconfig/lang.json', 'r') as f:
            language = json.load(f)
        language.pop(str(guild.id))
        with open('serverconfig/lang.json', 'w') as f:
            json.dump(language, f, indent=4)

        channel = discord.Client.get_channel(self.client, id=880568567702110258)
        await channel.send(f'Left {guild.name} ({guild.id})')


def setup(client):
    client.add_cog(GuildEvents(client))
