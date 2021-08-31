import discord
import functions.getLang
import simplejson as json
from discord.ext import commands


class InviteList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["invitelist", "Invitelist", "Invites"], no_pm=True)
    @commands.bot_has_permissions(manage_guild=True, manage_channels=True)
    async def invites(self, ctx, user: discord.User = None):

        # Get language and JSON
        lang = functions.getLang.getLang(ctx.guild.id)
        with open(f"embeds/{lang}/invitelist.json", "r") as f:
            invitesData = json.load(f)

        # If mentions user
        if user is not None:
            totalInvites = 0
            invite_url = []

            # Counts and gets list of invites
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    totalInvites += 1
                    invite_url.append(i.url)

            # Creates embed from dict
            singleUser = invitesData['single']
            singleUser['description'] = singleUser['description'].replace("%USER", user.name)
            singleUser['description'] = singleUser['description'].replace("%LINKS", str(totalInvites))
            singleUser['description'] = singleUser['description'].replace("%INVITES", "\n".join(invite_url))
            embed = discord.Embed.from_dict(singleUser)
            embed.set_author(name=f'{user.name}#{user.discriminator} ({user.id})', icon_url=user.avatar_url)

            await ctx.reply(embed=embed, mention_author=False, remove_after=20)

        # No user is mentioned
        else:
            # Creates embed from dict
            embed = discord.Embed.from_dict(invitesData['top25'])
            allInvites = [f'{i.inviter.name}#{i.inviter.discriminator} ({i.inviter.id}): {i.url}' for i in await ctx.guild.invites()]
            embed.description = "\n".join(allInvites)

            await ctx.reply(embed=embed, mention_author=False, remove_after=20)

    @invites.error
    async def invites_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            lang = functions.getLang.getLang(ctx.guild.id)
            with open(f"embeds/{lang}/invitelist.json") as f:
                await ctx.reply(embed=json.load(f)['BotMissingPermissions'], mention_author=False, remove_after=20)
        else:
            raise error


def setup(client):
    client.add_cog(InviteList(client))
