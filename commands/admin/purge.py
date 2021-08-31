import discord
import simplejson as json
import functions
import time
from discord.ext import commands


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Purge"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, number: int, user: discord.Member = None):
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/purge.json") as f:
            purgeData = json.load(f)

        if user is None:
            deleted = await ctx.channel.purge(limit=number, bulk=True)
            send = purgeData['DeleteNoUser'].replace("%VAR", str(len(deleted)))
            msg = await ctx.send(send)

        else:
            def is_user(m):
                return m.author == user

            deleted = await ctx.channel.purge(limit=number, bulk=True, check=is_user)
            send = purgeData['DeleteWithUser'].replace("%VAR1", str(len(deleted)))
            msg = await ctx.send(send.replace("%VAR2", user.mention))

        time.sleep(10)
        await ctx.message.delete()
        await msg.delete()

    @purge.error
    async def purge_error(self, ctx, error):
        lang = functions.getLang.getLang(ctx.guild.id)
        if isinstance(error, commands.errors.BotMissingPermissions):
            with open(f"embeds/{lang}/purge.json") as f:
                await ctx.reply(embed=discord.Embed.from_dict(json.load(f)['BotMissingPermissions']),
                                mention_author=False,
                                delete_after=20)

        elif isinstance(error, commands.errors.MissingPermissions):
            with open(f"embeds/{lang}/purge.json") as f:
                await ctx.reply(embed=discord.Embed.from_dict(json.load(f)['MissingPermissions']),
                                mention_author=False,
                                delete_after=20)

        elif isinstance(error, commands.errors.UserNotFound):
            with open(f"embeds/{lang}/purge.json") as f:
                await ctx.reply(embed=discord.Embed.from_dict(json.load(f)['UserNotFound']),
                                mention_author=False,
                                delete_after=20)



def setup(client):
    client.add_cog(Purge(client))
