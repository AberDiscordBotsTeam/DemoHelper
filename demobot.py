import os

import logging

from discord.ext import commands
from discord.ext.commands import Context, DefaultHelpCommand
from dotenv import load_dotenv

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Initialise the Bot object with an accessible help Command object
helpCommand = DefaultHelpCommand()

bot = commands.Bot(
    command_prefix='!',  # changing this prefix changes the way the bot is called. e.g. '$' = $add or '!' = !add
    help_command=helpCommand,
    description='Help command'
)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class General(commands.Cog):
    """
    General commands for everyone.
    """

    @commands.command()
    async def source(self, ctx: Context):
        """
        Link to the sourcecode
        """
        await ctx.send(content='Created by `Nathan Williams`\nMaintained by `Joel Adams`\n'
                               'https://github.com/AberDiscordBotsTeam/demoHelperBot')

    @commands.command()
    async def info(self, ctx: Context):
        """
        Display some info about how the bot works
        """
        await ctx.send('DemoHelper is a queue system for online practical where students can add themselves to the '
                       'queue using `!add`. When a demonstrator is free to help, they can call the `!next` command to '
                       'get the next waiting student.')

    @commands.command()
    async def feedback(self, ctx: Context):
        """
        Report feedback or issues with the bot
        """
        await ctx.send('If the bot is broken or you have any feedback you\'d like to submit please join '
                       'https://discord.gg/b3EdxVK and post a message in the <#740966780079571105> or '
                       '<#740967688876327012> channels')


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
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Sorry, I didn\'t get that.')
    else:
        await ctx.send('Something went wrong, please contact an Admin.')
        logging.error(error)


# Start the bot
bot.run(TOKEN)
