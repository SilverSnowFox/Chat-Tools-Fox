import simplejson as json
import discord
import re
import functions
from discord.ext import commands


class msgLink(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True, manage_webhooks=True)
    async def on_message(self, message):
        # No PM, no bot and check that enabled
        if message.guild is None or message.author.bot or not functions.servermodules.getConfig(message.guild.id, "msg_links"):
            return
        try:
            links = re.findall(r"https://discord\.com/channels/................../................../..................", message.content)

            # Checks that there exists at least 1 link
            if len(links) != 0:
                content = message.content
                for x in links:
                    content = content.replace(x, "")

                webhooks = await message.channel.webhooks()
                webhook = discord.utils.get(webhooks, name="Curse Fox")

                # Creates the webhook if not exists
                if webhook is None:
                    webhook = await message.channel.create_webhook(name="Curse Fox")

                await webhook.send(content, username=message.author.display_name, avatar_url=message.author.avatar_url)

                # Attachments if user sent a text
                for im in message.attachments:
                    await webhook.send(im.url, username=message.author.display_name, avatar_url=message.author.avatar_url)

                for l in links:
                    x = l.split('/')

                    if int(x[4]) == message.guild.id:
                        messageRef = await self.client.get_guild(int(x[4])).get_channel(int(x[5])).fetch_message(int(x[6]))

                        embed = discord.Embed(colour=16777215)
                        embed.set_author(name=messageRef.author.name, icon_url=messageRef.author.avatar_url)
                        embed.description = messageRef.content
                        embed.add_field(name="\u200b", value=f"[Link]({l})")
                        embed.set_footer(text=messageRef.channel.name)

                        await webhook.send(embed=embed, username=message.author.display_name, avatar_url=message.author.avatar_url)

        except commands.BotMissingPermissions or discord.errors.Forbidden:
            lang = functions.getLang.getLang(message.guild.id)
            with open(f"embeds/{lang}/msgLink.json", "r") as f:
                await message.channel.send(json.load(f)['BotMissingPermissions'])
        except Exception as e:
            raise e


def setup(client):
    client.add_cog(msgLink(client))
