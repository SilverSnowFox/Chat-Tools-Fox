import discord
import functions.getLang
import simplejson as json
from discord.ext import commands
from discord import Button, ButtonStyle


class InviteList(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["invitelist", "Invitelist", "Invites"])
    @commands.bot_has_permissions(manage_guild=True, manage_channels=True)
    async def invites(self, ctx, user: discord.User=None):
        lang = functions.getLang.getLang(ctx.guild.id)
        if user is not None:
            totalInvites = 0
            invite_url = []

            for i in await ctx.guild.invites():
                if i.inviter == user:
                    totalInvites += 1
                    invite_url.append(i.url)

            with open(f"embeds/{lang}/invites.json", "r") as f:
                singleUser = json.load(f)['single']

            singleUser['description'] = singleUser['description'].replace("%USER", user.name)
            singleUser['description'] = singleUser['description'].replace("%LINKS", str(totalInvites))
            singleUser['description'] = singleUser['description'].replace("%INVITES", "\n".join(invite_url))

            embed = discord.Embed.from_dict(singleUser)
            embed.set_author(name=f'{user.name}#{user.discriminator} ({user.id})', icon_url=user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

        else:
            with open(f"embeds/{lang}/invites.json", "r") as f:
                top25 = json.load(f)['top25']

            embed = discord.Embed.from_dict(top25)

            allInvites = [f'{i.inviter.name}#{i.inviter.discriminator} ({i.inviter.id}): {i.url}' for i in await ctx.guild.invites()]
            embed.description = "\n".join(allInvites)

            await ctx.reply(embed=embed, mention_author=False)

    @invites.error
    async def invites_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            lang = functions.getLang.getLang(ctx.guild.id)
            with open(f"embeds/{lang}/errors.json") as f:
                await ctx.reply(embed=json.load(f)['bot-manage-guild-and-channels'], mention_author=False)
        else:
            raise error


def setup(client):
    client.add_cog(InviteList(client))
