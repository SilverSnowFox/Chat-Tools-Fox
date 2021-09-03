import discord
import os
import simplejson as json
from discord.ext import commands


def get_prefix(client, message):
    with open('serverconfig/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix=get_prefix, intents=intents)
client.remove_command('help')

# Load commands and events
for category in os.listdir('commands/'):
    for filename in os.listdir(f'commands/{category}/'):
        if filename.endswith('.py'):
            client.load_extension(f'commands.{category}.{filename[:-3]}')

for filename in os.listdir('events/'):
    if filename.endswith('.py'):
        client.load_extension(f'events.{filename[:-3]}')


# Cog load, reload and unload
@client.command(aliases=["Cog"])
async def cog(ctx, action, cogType, folder, extension):

    # To check that cog exists
    if not os.path.isfile(f"{cogType}/{folder}/{extension}.py"):
        await ctx.send("Cog doesn't exist.")
        return

    try:
        # Checks that user is an admin
        with open("data/owners.json", "r") as file:
            admins = json.load(file)
            if str(ctx.message.author.id) not in admins:
                await ctx.send("This is an admin only command.")
                return

        # Checks for each Cog action. If use one cog more than the other can change their order.
        if action == "reload":
            client.unload_extension(f'{cogType}.{folder}.{extension}')
            client.load_extension(f'{cogType}.{folder}.{extension}')
            await ctx.send(f"Cog {extension} reloaded")
        elif action == "load":
            client.load_extension(f'{cogType}.{folder}.{extension}')
            await ctx.send(f"Cog {extension} loaded.")
        elif action == "unload":
            client.unload_extension(f'{cogType}.{folder}.{extension}')
            await ctx.send(f"Cog {extension} unloaded.")
        else:
            await ctx.send("That cog action doesn't exist.")

    except FileNotFoundError:
        await ctx.send("admin.json doesn't exist.")
    except discord.ext.commands.ExtensionAlreadyLoaded:
        await ctx.send(f"Cog {extension} already loaded.")
    except discord.ext.commands.ExtensionNotLoaded:
        await ctx.send(f"Cog {extension} already unloaded.")

# Loading token
with open("data/token.json") as json_file:
    token = json.load(json_file)

print("Loaded", ", ".join([cog[0] for cog in client.cogs.items()]))
print(f"{ len(client.cogs.items())} cogs loaded.")

client.run(token)
