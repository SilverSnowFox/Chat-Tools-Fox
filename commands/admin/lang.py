import time
import simplejson as json
import discord
from discord import SelectMenu, SelectOption
from discord.ext import commands


class Lang(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Lang"], no_pm=True)
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
        select = await ctx.reply(embed=discord.Embed.from_dict(embed['list']).set_thumbnail(url=self.client.user.avatar_url),
                                components=[SelectMenu(custom_id='lang-menu', placeholder='Languages', options=[
                SelectOption(label='EN',
                             value='EN',
                             description='English'),
                SelectOption(label='ES',
                             value='ES',
                             description="Español")
            ])], mention_author=False, remove_after=20)

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
        msg = await ctx.send(embed=discord.Embed.from_dict(embed['change']))
        time.sleep(20)
        await msg.delete()

    @lang.error
    async def lang_error(self, ctx, error):
        from functions.getLang import getLang
        lang = getLang(ctx.message.guild.id)

        if isinstance(error, commands.MissingPermissions):
            with open(f"embeds/{lang}/language.json", "r") as f:
                errors = json.load(f)
            await ctx.reply(embed=discord.Embed.from_dict(errors['MissingPermissions']), mention_author=False, delete_after=20)
        else:
            raise error


def setup(client):
    client.add_cog(Lang(client))
