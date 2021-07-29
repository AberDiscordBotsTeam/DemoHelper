from datetime import time

import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_components import create_select_option, create_select, create_actionrow

from helpers.messages import message__info__about, message__info__feedback


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="about",
        description="About DemoHelper."
    )
    async def command__slash__utility__about(self, ctx: SlashContext):
        await ctx.send(embed=message__info__about())

    @cog_ext.cog_slash(
        name="feedback",
        description="Do you have any reports or suggestions?"
    )
    async def command__slash__utility__feedback(self, ctx: SlashContext):
        await ctx.send(embed=message__info__feedback())

    @cog_ext.cog_slash(
        name="ping",
        description=""
    )
    async def command__slash__utility__ping(self, ctx: SlashContext):
        start_time = time()
        message = await ctx.send(
            f'pong. `DWSP latency: {str(round(ctx.bot.latency * 1000))}ms`'
        )
        end_time = time()
        await message.edit(
            content=
            f'🏓 pong `DWSP latency: {str(round(ctx.bot.latency * 1000))}ms` '
            + f'`Response time: {str(int((end_time - start_time) * 1000))}ms`')
