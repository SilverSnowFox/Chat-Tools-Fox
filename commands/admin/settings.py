import discord
import simplejson as json
import functions
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Setings"])
    async def settings(self, ctx):

        # No PM
        if ctx.guild is None:
            return

        # Gets all the variables
        guildID = ctx.guild.id
        antiScam = functions.servermodules.getConfig(guildID, "anti_scam")
        ghostPing = functions.servermodules.getConfig(guildID, "ghost_ping")
        msgLinks = functions.servermodules.getConfig(guildID, "msg_links")
        improvedPins = functions.serverchannels.getChannel(guildID, "pins")
        suggestions = functions.serverchannels.getChannel(guildID, "suggestions")
        reports = functions.serverchannels.getChannel(guildID, "reports")

        # Gets data from JSON
        lang = functions.getLang.getLang(guildID)
        with open(f"embeds/{lang}/settings.json", "r") as f:
            settingData = json.load(f)
        moderation = settingData['Moderation']
        channels = settingData['Channels']

        def replaceThree(input: str, var1, var2, var3):
            return input.replace("%VAR1", var1).replace("%VAR2", var2).replace("%VAR3", var3)

        def emote(input: bool):
            if input:
                return ":green_square:"
            return ":red_square:"

        def channel(channel):
            if self.client.get_channel(channel) is not None:
                return self.client.get_channel(channel).mention
            return "`None`"

        # Embed
        settingsEmbed = discord.Embed(colour=discord.Colour.gold())
        settingsEmbed.title = settingData['Title'].replace("%VAR", ctx.guild.name)
        settingsEmbed.set_thumbnail(url=ctx.guild.icon_url)
        settingsEmbed.add_field(name=moderation['name'],
                                value=replaceThree(moderation['value'], emote(antiScam), emote(ghostPing), emote(msgLinks)),
                                inline=False)
        settingsEmbed.add_field(name=channels['name'],
                                value=replaceThree(channels['value'], channel(improvedPins), channel(suggestions), channel(reports)),
                                inline=False)
        settingsEmbed.set_footer(text=settingData['Footer'])

        await ctx.reply(embed=settingsEmbed, mention_author=False, components=[ActionRow(
            Button(label=settingData['Button']['Scam'], custom_id="anti-scam", style=ButtonStyle.blurple),
            Button(label=settingData['Button']['Ping'], custom_id="ghost-ping", style=ButtonStyle.blurple),
            Button(label=settingData['Button']['Link'], custom_id="msg-link", style=ButtonStyle.blurple)
        )], remove_after=20)

    @commands.Cog.listener('on_button_click')
    async def on_button_click(self, i: discord.Interaction, button):

        # Check user has permission
        if i.author.guild_permissions.manage_guild:

            # Check that the custom ID is the correct one
            if i.component.custom_id in ['anti-scam', 'ghost-ping', 'msg-link']:

                # Gets all the variables
                guildID = i.guild.id

                # Edits the embed depending on the button
                if i.component.custom_id == "anti-scam":
                    inverse = not functions.servermodules.getConfig(guildID, "anti_scam")
                    functions.servermodules.updateModule(guildID, "anti_scam", inverse)
                    antiScam = inverse
                    ghostPing = functions.servermodules.getConfig(guildID, "ghost_ping")
                    msgLinks = functions.servermodules.getConfig(guildID, "msg_links")
                elif i.component.custom_id == "ghost-ping":
                    inverse = not functions.servermodules.getConfig(guildID, "ghost_ping")
                    functions.servermodules.updateModule(guildID, "ghost_ping", inverse)
                    ghostPing = inverse
                    antiScam = functions.servermodules.getConfig(guildID, "anti_scam")
                    msgLinks = functions.servermodules.getConfig(guildID, "msg_links")
                else:
                    inverse = not functions.servermodules.getConfig(guildID, "msg_links")
                    functions.servermodules.updateModule(guildID, "msg_links", inverse)
                    msgLinks = inverse
                    antiScam = functions.servermodules.getConfig(guildID, "anti_scam")
                    ghostPing = functions.servermodules.getConfig(guildID, "ghost_ping")

                # The channels that don't change with the embed
                improvedPins = functions.serverchannels.getChannel(guildID, "pins")
                suggestions = functions.serverchannels.getChannel(guildID, "suggestions")
                reports = functions.serverchannels.getChannel(guildID, "reports")

                # Gets data from JSON
                lang = functions.getLang.getLang(guildID)
                with open(f"embeds/{lang}/settings.json", "r") as f:
                    settingData = json.load(f)
                moderation = settingData['Moderation']
                channels = settingData['Channels']

                def replaceThree(stringput: str, var1, var2, var3):
                    return stringput.replace("%VAR1", var1).replace("%VAR2", var2).replace("%VAR3", var3)

                def emote(boolinput: bool):
                    if boolinput:
                        return ":green_square:"
                    return ":red_square:"

                def channel(channel):
                    if channel != 0:
                        return self.client.get_channel(improvedPins).mention
                    return "`None`"

                # Embed
                settingsEmbed = discord.Embed(colour=discord.Colour.gold())
                settingsEmbed.title = settingData['Title'].replace("%VAR", i.guild.name)
                settingsEmbed.set_thumbnail(url=i.guild.icon_url)
                settingsEmbed.add_field(name=moderation['name'],
                                        value=replaceThree(moderation['value'], emote(antiScam), emote(ghostPing), emote(msgLinks)),
                                        inline=False)
                settingsEmbed.add_field(name=channels['name'],
                                        value=replaceThree(channels['value'], channel(improvedPins), channel(suggestions), channel(reports)),
                                        inline=False)
                settingsEmbed.set_footer(text=settingData['Footer'])

                await i.edit(embed=settingsEmbed)

        # In case the user doesn't have permissions and clicks the button
        elif i.component.custom_id == "anti-scam" or i.component.custom_id == "ghost-ping" or i.component.custom_id == "msg-link":
            lang = functions.getLang.getLang(i.guild.id)
            with open(f"embeds/{lang}/settings.json", "r") as f:
                settingsData = json.load(f)
            await i.respond(embeds=discord.Embed.from_dict(settingsData['UserMissingPermission']), hidden=True, delete_after=20)


def setup(client):
    client.add_cog(Settings(client))
