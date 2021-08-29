import json
import discord
import functions
from discord.ext import commands


class GuildEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Add guild to prefix list
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Sets the default prefix to =
        with open('serverconfig/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes[str(guild.id)] = "="
            json.dump(prefixes, f, indent=4)

        # Sets the default language to EN
        with open('serverconfig/lang.json', 'r') as f:
            language = json.load(f)
            language[str(guild.id)] = 'EN'
            json.dump(language, f, indent=4)

        # Innitiated guild entries in modules and channels database
        functions.servermodules.innitiateGuild(guild.id)
        functions.serverchannels.innitiateGuild(guild.id)

        channel = discord.Client.get_channel(self.client, id=880568567702110258)
        await channel.send(f'Joined {guild.name} ({guild.id})')

    # Remove guild from prefix list
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # Removes guild from prefixes
        with open('serverconfig/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes.pop(str(guild.id))
            json.dump(prefixes, f, indent=4)

        # Removes server from languages
        with open('serverconfig/lang.json', 'r') as f:
            language = json.load(f)
            language.pop(str(guild.id))
            json.dump(language, f, indent=4)

        # Removes guild from the databases
        functions.servermodules.deleteGuild(guild.id)
        functions.serverchannels.deleteGuild(guild.id)

        channel = discord.Client.get_channel(self.client, id=880568567702110258)
        await channel.send(f'Left {guild.name} ({guild.id})')


def setup(client):
    client.add_cog(GuildEvents(client))
