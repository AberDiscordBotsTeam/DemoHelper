import os

from discord.ext.commands import Context
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!demoBot ')

queues = {'dummy':[]}


def getQueue(serverName:str):
    if serverName in queues.keys():
        return queues.get(serverName)
    else:
        queues[serverName] = []
        return queues.get(serverName)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command(name='add', help='- adds the student to the help queue')
async def add(ctx:Context):
    s =ctx.message.author.mention
    q = getQueue(ctx.guild)
    if s not in q:
        q.append(s)
        await ctx.send('added you to the queue')
    else:
        await ctx.send('already in queue')

@bot.command(name='next', help='- sees who\'s next in the queue')
@commands.has_any_role('Demonstrator','demonstrator','Admin role')
async def next(ctx):
    next = getQueue(ctx.guild).pop(0)
    if next is not None:
        await ctx.send('Next in queue is {0}'.format(next))
    else:
        await ctx.send('NO more in queue :)')

@bot.command(name='print', help='- sees who\'s next in the queue')
@commands.has_any_role('Demonstrator','demonstrator','Admin role')
async def printQ(ctx):
    await ctx.send('Remaining in queue are {0}'.format(getQueue(ctx.guild)))


bot.run(TOKEN)