import os

import logging
import shelve

from discord.ext.commands import Context
from dotenv import load_dotenv

from discord.ext import commands

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

queues = {'dummy':[]}

adminRoles = ['Demonstrator','demonstrator','Admin role','ADMIN ROLE','DEMONSTRATOR','admin role','adminrole']


def getQueue(serverName:str):
    if serverName in queues.keys():
        return queues.get(serverName)
    else:
        queues[serverName] = []
        return queues.get(serverName)


def getCustomAddMessage(serverName:str):
    with shelve.open('addMessage.shelve') as db:
        if str(serverName) in db:
            return db.get(str(serverName))
        else:
            return ''


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    else:
        await ctx.send('something went wrong, please contact the Admin')
        logging.error(error)


@bot.command(name='setAddMessage', help='- change the message displayed when a person is added to the queue')
@commands.has_any_role(*adminRoles)
async def setAddMessage(ctx,*,message:str):
    logging.info('{0} setAddMessage {1}'.format(ctx.guild, message))
    with shelve.open('addMessage.shelve') as db:
        db[str(ctx.guild)] = message
    await ctx.send('Anyone added to queue will see this msg:\n' + message)


@bot.command(name='add', help='- adds the student to the help queue')
async def add(ctx:Context):
    s =ctx.message.author.mention
    q = getQueue(ctx.guild)
    if s not in q:
        q.append(s)
        logging.info('{0} add {1}'.format(ctx.guild,s))
        await ctx.send('added you to the queue,\n' + getCustomAddMessage(ctx.guild))
    else:
        await ctx.send('already in queue')

@bot.command(name='remove', help='- remove self from the help queue')
async def add(ctx:Context):
    s = ctx.message.author.mention
    q = getQueue(ctx.guild)
    if s in q:
        q.remove(s)
        logging.info('{0} remove {1}'.format(ctx.guild, s))
        await ctx.send('removed you from queue')
    else:
        await ctx.send('you were not in the queue')

        
@bot.command(name='source', help='- link to my sourcecode')
async def source(ctx):
    await ctx.send('https://github.com/IdrisTheDragon/demoHelperBot')


@bot.command(name='next', help='- sees who\'s next in the queue')
@commands.has_any_role(*adminRoles)
async def next(ctx):
    if len(getQueue(ctx.guild)) > 0:
        next = getQueue(ctx.guild).pop(0)
        logging.info('{0} next {1}'.format(ctx.guild,next))
        if next is not None:
            await ctx.send('Next in queue is {0}, {1} will do your signoff/help.'.format(next,ctx.message.author.mention))
    else:
        await ctx.send('No more in queue :)')


@bot.command(name='print', help='- print out the queue')
@commands.has_any_role(*adminRoles)
async def printQ(ctx):
    logging.info('{0} queue {1}'.format(ctx.guild, getQueue(ctx.guild)))
    await ctx.send('Remaining in queue are {0}'.format(getQueue(ctx.guild)))

bot.run(TOKEN)
