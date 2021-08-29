import discord
import functions.getLang
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow



class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Poll"])
    async def poll(self, ctx, *, args):
        lang = functions.getLang.getLang(ctx.guild.id)
        # Splits arguments in list items through separator $, where index 0 is the question
        arguments = args.split('$')

        if len(arguments) < 2:
            # Error that need question and at least 2 options split by $
            pass
            return

        # Author of Embed
        # Title = question
        # Arguments
        ## Emote - option - count "Arg1": {emote: "", option: "", count: ""}
        # ActionRow with buttons 1 to 5
        # ActionRow with buttons 6: 10
        # Button to delete poll
        # Button to end poll
        # Edit embed with new count for each time an interaction
        # Keep track of voters to avoid double vote [Voter]



        embed = discord.Embed(colour=discord.Colour.gold())
        embed.set_author(name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
                         icon_url=ctx.message.author.avatar_url)
        embed.title = arguments[0]

        emotes = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':ten:']
        entries = []
        for option, emote in zip(arguments[1:], emotes):
            entries.append(f"{emote} : {option}")
        embed.description = "\n".join(entries)

        actionRow1 = {
            'type': 1,
            'components': []
        }
        actionRow2 = {
            'type': 1,
            'components': []
        }

        i = 0
        while i < 5 and i < len(arguments[1:]):
            actionRow1['components'].append({
                'type': 2,
                'style': 2,
                'label': f'{i+1}',
                'custom_id': f'{emotes[i]}'
            })
            i += 1

        if len(arguments) > 6:
            j = 0
            while j < 5 and j < len(arguments[5:8]):
                actionRow2['components'].append({
                    'type': 2,
                    'style': 2,
                    'label': f'{j + 6}',
                    'custom_id': f'{emotes[5+j]}'
                })
                j += 1

        voters = {}
        poll = await ctx.send(embed=embed, components=[ActionRow.from_dict(actionRow1),
                                                       ActionRow.from_dict(actionRow2),
                                                       ActionRow(Button(label="?", style=ButtonStyle.blurple, custom_id="?"))])

        def _check(i: discord.Interaction, b):
            return i.message == poll and i.message.author not in voters.keys()

        interaction, button = await self.client.wait_for('button_click', check=_check)

def setup(client):
    client.add_cog(Poll(client))
