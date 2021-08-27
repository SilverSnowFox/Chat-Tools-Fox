import simplejson as json
import discord
from discord import SelectMenu, SelectOption
from discord.ext import commands


class Lang(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Lang"])
    @commands.has_permissions(manage_guild=True)
    async def lang(self, ctx):
        # Get server language
        with open('serverconfig/lang.json', 'r') as f:
            language = json.load(f)
        old_language = language[str(ctx.guild.id)]

        # Get embed
        with open(f'embeds/{old_language}/language.json', 'r') as f:
            embed = json.load(f)

        # Send embed with select menu
        select = await ctx.send(embed=discord.Embed.from_dict(embed['list']),
                                components=[SelectMenu(custom_id='help_menu', placeholder='Languages', options=[
                SelectOption(label='EN',
                             value='EN',
                             description='English'),
                SelectOption(label='ES',
                             value='ES',
                             description="Español")
            ])])

        # Check select menu
        def check_selection(i: discord.Interaction, select_menu):
            return i.message == select and i.author.id == ctx.message.author.id
        interaction, select_menu = await self.client.wait_for('selection_select', check=check_selection)
        lang = select_menu.values[0]
        await select.delete()

        # Update language
        language[str(ctx.guild.id)] = lang
        with open('serverconfig/lang.json', 'w') as f:
            json.dump(language, f, indent=4)

        # Gets and sends embed of new language
        with open(f"embeds/{lang}/language.json", "r") as f:
            embed = json.load(f)
        await ctx.send(embed=discord.Embed.from_dict(embed['change']))

        # Logging embed
        log_embed = {
            "title": "Language",
            "color": 3974125,
            "description": f"`{old_language}` -> `{language}`",
            "author": {
                "name": f"{ctx.message.author.name} ({ctx.message.author.id})",
                "icon_url": ctx.message.author.avatar_url
            }
        }

    @lang.error
    async def lang_error(self, ctx, error):
        from functions.getLang import getLang
        lang = getLang(ctx.message.guild.id)

        if isinstance(error, commands.MissingPermissions):
            with open(f"embeds/{lang}/errors.json", "r") as f:
                errors = json.load(f)
            await ctx.send(embed=discord.Embed.from_dict(errors['admin-manage']))
        else:
            raise error


def setup(client):
    client.add_cog(Lang(client))
