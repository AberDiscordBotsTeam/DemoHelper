import os
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!demoBot ')

queue = []

def addToQueue(x:str):
    queue.append(x)


def nextInQueue():
    return queue.pop(0)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='add', help='- adds the student to the help queue')
async def nine_nine(ctx):
    addToQueue(ctx.message.author.mention)
    await ctx.send('added you to the queue')

@bot.command(name='next', help='- sees who\'s next in the queue')
@commands.has_role('Demonstrator')
async def roll(ctx):
    await ctx.send('Next in queue is {0}'.format(nextInQueue()))

@bot.command(name='printQueue', help='- sees who\'s next in the queue')
@commands.has_role('Demonstrator')
async def roll(ctx):
    await ctx.send('Remaining in queue are {0}'.format(queue))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)