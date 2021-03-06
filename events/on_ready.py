import discord
from discord.ext import commands


class Start(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot is online. Logged in as {self.client.user.name}')
        print(f'Bot in {len(self.client.guilds)} guilds at {round(self.client.latency * 1000)} ms')
        await self.client.change_presence(status=discord.Status.online)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                                    name="chat | Mention for prefix!"))


def setup(client):
    client.add_cog(Start(client))
