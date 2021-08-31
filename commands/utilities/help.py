import discord
import functions
import simplejson as json
from discord.ext import commands
from discord import ActionRow, Button, ButtonStyle


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Help"])
    async def help(self, ctx):
        # Get language
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/help.json", "r") as f:
            helpData = json.load(f)

        helpEmbed = discord.Embed(color=3974125)
        helpEmbed.title = helpData['Main']['Title']
        helpEmbed.description = helpData['Main']['Description']
        helpEmbed.set_thumbnail(url=self.client.user.avatar_url)
        helpEmbed.add_field(name=helpData['Main']['Servers'], value=f"{len(self.client.guilds)}", inline=True)
        helpEmbed.add_field(name=helpData['Main']['Latency'], value=f"{round(self.client.latency * 1000)} ms", inline=True)
        helpEmbed.add_field(name=helpData['Main']['Users'], value=f"{sum([len(guild.members) for guild in self.client.guilds])}", inline=True)

        await ctx.reply(embed=helpEmbed, components=[
            ActionRow().from_dict(helpData['Main-ActionRow'])
        ], mention_author=False)

    @commands.Cog.listener('on_button_click')
    async def on_button_click(self, i: discord.Interaction, button):
        lang = functions.getLang.getLang(i.guild.id)

        if i.component.custom_id in ['Utilities', 'Admin', 'Modules']:
            with open(f"embeds/{lang}/help.json", "r") as f:
                helpData = json.load(f)
            embed = discord.Embed.from_dict(helpData[i.component.custom_id])
            embed.set_thumbnail(url=self.client.user.avatar_url)
            await i.message.edit(embed=embed)
            await i.defer()


def setup(client):
    client.add_cog(Help(client))
