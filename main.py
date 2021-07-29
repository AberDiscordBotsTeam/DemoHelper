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
from cogs.slash.general import General
from cogs.slash.student_tools import StudentTools
from cogs.slash.utility import Utility

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
    bot.loop.create_task(activity_loop())
    print(f'------------------------------------------------------------------------------'
          f'\n|  as of {datetime.utcnow()}, {bot.user.name} is operational  |'
          f'\n------------------------------------------------------------------------------')


async def activity_loop():
    """
    Cycles through different bot activities
    """
    await bot.wait_until_ready()
    i = 0
    while not bot.is_closed():

        if i > 2:
            i = 0
        '''
        memb = set()
        for guild in bot.guilds:
            memb.update(guild.members)
        '''

        status = [
            f'{len(bot.guilds)} servers',
            f'{1300} members',
            '!help | !feedback'
        ]

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[i]))
        i += 1

        await asyncio.sleep(4)


@bot.event
async def on_command_error(ctx, error):
    """
    Handle the Error message in a nice way.
    """
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandNotFound):
        pass
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send('Please input a users @username instead. e.g. !clearRole @Joel Adams')
        ''' # TODO: implement rate limiting
    elif client.is_ws_ratelimited():
        await ctx.send("The bot is currently being rate limited due to high traffic, please wait a few seconds and try again")
        '''
    else:
        await ctx.send('Something went wrong, please contact an Admin.')
        logging.error(error)


if __name__ == '__main__':
    bot.add_cog(DemonstratorTools(bot))
    bot.add_cog(StudentTools(bot))
    bot.add_cog(General(bot))
    bot.add_cog(Utility(bot))
    bot.run(os.getenv('DISCORD_TOKEN'))
