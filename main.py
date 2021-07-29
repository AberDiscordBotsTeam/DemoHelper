import asyncio
import os

import logging
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from discord_slash import SlashCommand
from dotenv import load_dotenv

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
from cogs.slash.demonstrator_tools import DemonstratorTools
from cogs.slash.student_tools import StudentTools
from cogs.slash.utility import Utility
from helpers.messages import message__custom__error__check_failure, message__custom__error__missing_required_argument, \
    message__custom__error__command_not_found, message__custom__error__bad_argument, \
    message__custom__error__rate_limited, message__custom__error__unknown_error

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# load the private discord token from .env file.
load_dotenv()

# Initialise the Bot object with an accessible help Command object
helpCommand = DefaultHelpCommand()

bot = commands.Bot(
    command_prefix='dh~',
    intents=discord.Intents.all()
)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    """
    Do something when the bot is ready to use.
    """
    bot.loop.create_task(status_readout_loop())
    print(f'------------------------------------------------------------------------------'
          f'\n|  as of {datetime.utcnow()}, {bot.user.name} is operational  |'
          f'\n------------------------------------------------------------------------------')


async def status_readout_loop():
    """
    Cycles through different bot activities
    """
    await bot.wait_until_ready()
    i = 0
    while not bot.is_closed():
        member_count = 0
        for guild in bot.guilds: member_count += len(guild.members)

        status = [
            f'{len(bot.guilds)} servers',
            f'{member_count} members'
        ]

        if i >= len(status):
            i = 0

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[i]))

        i += 1

        await asyncio.sleep(5)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(embed=message__custom__error__check_failure(error))
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(embed=message__custom__error__missing_required_argument())
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(embed=message__custom__error__command_not_found())
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send(embed=message__custom__error__bad_argument())
    elif bot.is_ws_ratelimited():
        await ctx.send(embed=message__custom__error__rate_limited())
    else:
        await ctx.send(embed=message__custom__error__unknown_error())


if __name__ == '__main__':
    bot.add_cog(DemonstratorTools(bot))
    bot.add_cog(StudentTools(bot))
    bot.add_cog(Utility(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))
