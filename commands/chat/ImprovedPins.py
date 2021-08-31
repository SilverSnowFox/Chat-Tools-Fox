import datetime
import discord
import simplejson as json
from functions import serverchannels, getLang
from discord.ext import commands


class ImprovedPins(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True, manage_webhooks=True)
    async def on_message_edit(self, before, after):
        lang = getLang.getLang(before.guild.id)

        # No PM
        if before.guild is None:
            return

        try:
            # Check that message wasn't pinned and now is, and that ImprovedPins are enabled
            channel = serverchannels.getChannel(before.guild.id, "pins")
            if not before.pinned and after.pinned and channel != 0:

                # Check that user set the channel
                channel = serverchannels.getChannel(before.guild.id, "pins")
                if channel == 0:
                    with open(f"embeds/{lang}/improvedPins.json", "r") as f:
                        await before.channel.send(embed=discord.Embed.from_dict(json.load(f)['NoPinChannel']))
                    return

                else:
                    # Gets the pins channel
                    pins_channel = self.client.get_channel(channel)
                    attachments = before.attachments

                    # Base embed
                    baseEmbed = {
                        "color": 3974125,
                        "title": "Pin",
                        "author": {"name": f"{before.author.name}#{before.author.discriminator}", "icon_url": f'{before.author.avatar_url}'},
                        "footer": {"text": f"#{before.channel.name}"}
                    }

                    # No attachments
                    if len(attachments) == 0:
                        # Creates and send
                        baseEmbed["description"] = f'{before.content}'
                        await pins_channel.send(embed=discord.Embed.from_dict(baseEmbed))

                    # 1+ Attachments
                    else:

                        # Split attachments into images and others
                        imageFiles = []
                        others_files = []
                        for file in attachments:
                            if 'image' in file.content_type:
                                imageFiles.append(file)
                            else:
                                others_files.append(await file.to_file())

                        # Using webhook, can send up to 4 images as 1 embed even though it is 4 in code from a list.
                        embeds = [baseEmbed]

                        # Check if has message content before picking if set the description
                        # Add any 'others.url' to description
                        if before.content != "":
                            embeds[0]['description'] = f'{before.content}'

                        # If contains any image
                        if len(imageFiles) > 0:
                            embeds[0]['image'] = {"url": f'{imageFiles[0].url}'}
                            embeds[0]['url'] = f"{imageFiles[0].url}"
                            # 1 < images < 5 set
                            if len(imageFiles) > 1:
                                for img in imageFiles[1:4]:
                                    imag = {"url": f'{imageFiles[0].url}', "image": {"url": f"{img.url}"}}
                                    embeds.append(imag)

                            # 5th image
                            if len(imageFiles) > 4:
                                imag5 = {
                                    "color": 3974125,
                                    "url": f'{imageFiles[4]}',
                                    "image": {"url": f'{imageFiles[4]}'},
                                    "description": "\u200b",
                                    "footer": {"text": f"#{before.channel.name}"}
                                }
                                embeds.append(imag5)

                                # 5 < images < 9 set
                                for img in imageFiles[5:8]:
                                    imag = {"url": f'{imageFiles[4].url}', "image": {"url": f"{img.url}"}}
                                    embeds.append(imag)

                        # Converts dict to embeds and adds timestamps
                        Embeds_final = [discord.Embed.from_dict(e) for e in embeds]
                        Embeds_final[0].timestamp = datetime.datetime.utcnow()
                        if len(Embeds_final) > 4:
                            Embeds_final[4].timestamp = datetime.datetime.utcnow()

                        # Creates webhook and sends
                        webhooks = await pins_channel.webhooks()
                        webhook = discord.utils.get(webhooks, name=self.client.user.name)
                        if webhook is None:
                            webhook = await pins_channel.create_webhook(name=self.client.user.name)
                        await webhook.send(embeds=Embeds_final,
                                           username=self.client.user.name,
                                           avatar_url=self.client.user.avatar_url)
                        if len(others_files) != 0:
                            await webhook.send(files=others_files)

                    await after.unpin(reason="ImprovedPins Active")

        except AttributeError:
            with open(f"embeds/{lang}/improvedPins.json", "r") as f:
                await before.channel.send(embed=discord.Embed.from_dict(json.load(f)['NoPinChannel']))
        except commands.errors.BotMissingPermissions or discord.errors.Forbidden:
            with open(f"embeds/{lang}/improvedPins.json", "r") as f:
                await before.channel.send(embed=discord.Embed.from_dict(json.load(f)['BotMissingPermissions']))
        except Exception:
            raise Exception


def setup(client):
    client.add_cog(ImprovedPins(client))
