import json
import functions
import discord
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow


class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Poll"], pass_context=True)
    async def poll(self, ctx, *, args):

        # Splits arguments in list items through separator $, where index 0 is the question
        arguments = args.split('$')

        if len(arguments) < 3 or len(arguments) > 11:
            lang = functions.getLang.getLang(ctx.guild.id)
            with open(f"embeds/{lang}/polls.json", "r") as f:
                await ctx.reply(embed=discord.Embed.from_dict(json.load(f)['LengthError']), mention_author=False)
            return

        # Define variables and lists will need after
        emotes = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':ten:']
        question = arguments[0]
        answers = {}
        description = []
        voters = {}

        # Creates embed description
        i = 0
        while i < len(arguments[1:]):
            answers[f'arg{i}'] = {"emote": emotes[i], "option": arguments[i+1], "count": 0}
            description.append(f"{emotes[i]} : {arguments[i+1]} - `0`")
            i += 1

        # Creates embed
        embed = discord.Embed(colour=discord.Colour.gold())
        embed.set_author(name=f"{ctx.message.author.name}#{ctx.message.author.discriminator}",
                         icon_url=ctx.message.author.avatar_url)
        embed.title = arguments[0]
        embed.description = "\n".join(description)

        actionRow1 = {'type': 1, 'components': []}
        actionRow2 = {'type': 1, 'components': []}

        # For buttons 1 to 5
        i = 0
        while i < 5 and i < len(arguments[1:]):
            actionRow1['components'].append({
                'type': 2,
                'style': 2,
                'label': f'{i+1}',
                'custom_id': f'arg{i}'
            })
            i += 1

        # For buttons 6 to 10
        if len(arguments) > 6:
            j = 0
            while j < 5 and j < len(arguments[5:8]):
                actionRow2['components'].append({
                    'type': 2,
                    'style': 2,
                    'label': f'{j + 6}',
                    'custom_id': f'arg{j+5}'
                })
                j += 1

        # Sends poll embed
        poll = await ctx.send(embed=embed, components=[ActionRow.from_dict(actionRow1),
                                                       ActionRow.from_dict(actionRow2),
                                                       ActionRow(Button(label="X", style=ButtonStyle.red, custom_id="vote-cancel"))])

        # Stores data for poll
        with open("serverdata/polls.json", "r") as f:
            pollData = json.load(f)
        pollData[str(poll.id)] = {"answers": answers, "voters": voters, "question": question}
        with open("serverdata/polls.json", "w") as f:
            json.dump(pollData, f, indent=4)

    @commands.Cog.listener('on_button_click')
    async def on_button_click(self, i: discord.Interaction, button):

        # Function to make new description
        def description(args: list) -> str:
            answerList = []
            for arg in args:
                answerList.append(f"{arg['emote']} : {arg['option']} - `{arg['count']}`")
            return "\n".join(answerList)

        # Checks that button  is one of a poll
        if i.component.custom_id.startswith("arg"):

            # Gets the poll information
            with open("serverdata/polls.json", "r") as f:
                pollData = json.load(f)

            # Poll messages
            lang = functions.getLang.getLang(i.guild.id)
            with open(f"embeds/{lang}/polls.json", "r") as f:
                pollResponses = json.load(f)

            # Checks that user hasn't already voted
            if str(i.author.id) not in pollData[str(i.message.id)]['voters'].keys():

                # Adds to voter list and vote count
                pollData[str(i.message.id)]['voters'][str(i.author.id)] = i.component.custom_id
                pollData[str(i.message.id)]['answers'][i.component.custom_id]["count"] += 1

                # Edit poll embed
                embed = i.message.embeds[0]
                arguments = pollData[str(i.message.id)]['answers'].values()
                embed.description = description(arguments)

                with open("serverdata/polls.json", "w") as f:
                    json.dump(pollData, f, indent=4)

                await i.message.edit(embed=embed)
                await i.respond(pollResponses['voted'], delete_after=10, hidden=True)
            else:
                await i.respond(pollResponses['already-voted'], delete_after=10, hidden=True)

        elif i.component.custom_id == "vote-cancel":

            # Gets the poll information
            with open("serverdata/polls.json", "r") as f:
                pollData = json.load(f)

            # Poll messages
            lang = functions.getLang.getLang(i.guild.id)
            with open(f"embeds/{lang}/polls.json", "r") as f:
                pollResponses = json.load(f)

            # Check if user has already voted
            if str(i.author.id) in pollData[str(i.message.id)]['voters'].keys():

                # Removes voter and voter count
                customID = pollData[str(i.message.id)]['voters'][str(i.author.id)]
                pollData[str(i.message.id)]['voters'].pop(str(i.author.id))
                pollData[str(i.message.id)]['answers'][customID]["count"] -= 1

                # Edit poll embed
                embed = i.message.embeds[0]
                arguments = pollData[str(i.message.id)]['answers'].values()
                embed.description = description(arguments)

                with open("serverdata/polls.json", "w") as f:
                    json.dump(pollData, f, indent=4)

                await i.message.edit(embed=embed)
                await i.respond(pollResponses['cancel'], delete_after=10, hidden=True)
            else:
                await i.respond(pollResponses['no-vote'], delete_after=10, hidden=True)


def setup(client):
    client.add_cog(Poll(client))
