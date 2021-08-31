from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            pass


def setup(client):
    client.add_cog(ErrorHandler(client))
