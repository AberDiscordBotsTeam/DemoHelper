import os

import logging

from discord.ext import commands
from discord.ext.commands import Context, DefaultHelpCommand
from dotenv import load_dotenv
from cogs.general import General

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('CMD_PREFIX')


# Initialise the Bot object with an accessible help Command object
helpCommand = DefaultHelpCommand()

# check if prefix set in the .env otherwise use default.
# changing the prefix changes the way the bot is called. e.g. '$' = $add or '!' = !add
prefix = PREFIX
if not prefix:
    prefix = '!'

bot = commands.Bot(
    command_prefix=prefix,
    help_command=helpCommand,
    description=''
)

# Setup the General cog with the help command
generalCog = General()
bot.add_cog(generalCog)
helpCommand.cog = generalCog

# load other cogs
bot.load_extension("cogs.demoHelper")


@bot.event
async def on_ready():
    """
    Do something when the bot is ready to use.
    """
    print(f'{bot.user.name} has connected to Discord!')


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
    else:
        await ctx.send('Something went wrong, please contact an Admin.')
        logging.error(error)


# Start the bot
bot.run(TOKEN)
