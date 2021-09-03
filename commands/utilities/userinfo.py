import simplejson as json
import discord
from discord.ext import commands
from functions.getLang import getLang


class Userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Userinfo", "user", "User"])
    async def userinfo(self, ctx, user: discord.Member = None):
        """Returns an embed with the member's information"""
        lang = getLang(ctx.message.guild.id)

        if user is None:
            user = ctx.author

        with open(f"embeds/{lang}/userinfo.json", "r") as f:
            data = json.load(f)

        embed = discord.Embed.from_dict(data['embed'])
        listItems = data['fields']

        embed.add_field(name=listItems[0], value=f'{user.name}#{user.discriminator} ({user.id})', inline=False)
        embed.add_field(name=listItems[1], value=user.status, inline=True)
        embed.add_field(name=listItems[2], value=user.activity, inline=True)
        embed.add_field(name=listItems[3], value=user.bot, inline=True)
        embed.add_field(name=listItems[4], value=user.nick, inline=True)
        embed.add_field(name=listItems[5], value=user.created_at.date().strftime("%b %d, %Y"), inline=True)
        embed.add_field(name=listItems[6], value=user.joined_at.date().strftime("%b %d, %Y"), inline=True)
        if ctx.guild is not None:
            embed.add_field(name=listItems[7], value=" ".join([f'<@&{role.id}>' for role in user.roles]), inline=False)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.reply(embed=embed, mention_author=False, delete_after=30)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        lang = getLang(ctx.message.guild.id)
        if isinstance(error, commands.errors.MemberNotFound):
            with open(f"embeds/{lang}/userinfo.json", "r") as f:
                await ctx.reply(embed=discord.Embed.from_dict(json.load(f)['MemberNotFound']), mention_author=False, delete_after=20)
        else:
            raise error


def setup(client):
    client.add_cog(Userinfo(client))
