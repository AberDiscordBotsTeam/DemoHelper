
import newrelic.agent
newrelic.agent.initialize("newrelic.ini", "production")
app = newrelic.agent.register_application(timeout=10.0)

import os

import logging
from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import DefaultHelpCommand
from discord_slash import SlashCommand
from dotenv import load_dotenv

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
from cogs.slash.demonstrator_tools import DemonstratorTools
from cogs.slash.student_tools import StudentTools
from cogs.slash.utility import Utility
from helpers.messages.errors import message__custom__error__check_failure, \
    message__custom__error__missing_required_argument, message__custom__error__command_not_found, \
    message__custom__error__bad_argument, message__custom__error__rate_limited, message__custom__error__unknown_error

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
    command_prefix='dh:',
    intents=discord.Intents.all()
)
slash = SlashCommand(bot, sync_commands=True)

bot_metrics = {}
current_status_index = 0


@newrelic.agent.background_task(name='main.on_ready', group='Task')
@bot.event
async def on_ready() -> None:
    """
    Do something when the bot is ready to use.
    """
    get_bot_metrics.start()
    status_readout_loop.start()
    print(f'------------------------------------------------------------------------------'
          f'\n|  as of {datetime.utcnow()}, {bot.user.name} is operational  |'
          f'\n------------------------------------------------------------------------------')


@newrelic.agent.background_task(name='main.get_bot_metrics', group='Task')
@tasks.loop(hours=24)
async def get_bot_metrics() -> None:
    await bot.wait_until_ready()
    if bot.is_closed(): return

    guilds = bot.guilds
    member_count = 0
    temp_member_set = {None}

    for guild in bot.guilds:
        members = guild.members
        member_count += len(members)
        temp_member_set.clear()
        for member in members:
            temp_member_set.add(member.name)

    bot_metrics["guild_count"] = len(guilds)
    bot_metrics["total_user_count"] = member_count
    bot_metrics["unique_user_count"] = len(temp_member_set)


@newrelic.agent.background_task(name='main.status_readout_loop', group='Task')
@tasks.loop(seconds=10)
async def status_readout_loop() -> None:
    global current_status_index

    await bot.wait_until_ready()
    if bot.is_closed(): return

    status = [
        f'{bot_metrics.get("guild_count")} servers',
        f'{bot_metrics.get("total_user_count")} members',
        f'{bot_metrics.get("unique_user_count")} unique members'
    ]

    if current_status_index >= len(status): current_status_index = 0

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=status[current_status_index]
        )
    )

    current_status_index += 1


@newrelic.agent.background_task(name='main.on_command_error', group='Task')
@bot.event
async def on_command_error(ctx, error) -> None:
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
