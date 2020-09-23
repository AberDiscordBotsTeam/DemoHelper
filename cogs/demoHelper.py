from discord.ext import commands
from discord.ext.commands import Context

import logging
import shelve

from helpers import listPrint

queues = {'dummy': []}
# Possible roles available for the user to add allowing them to use all the bot commands
adminRoles = ['Demonstrator', 'demonstrator', 'DEMONSTRATOR', 'Admin role', 'ADMIN ROLE', 'Admin', 'Devs', 'lecturer',
              'LECTURER']


def setup(bot):
    """
    Setup the cogs in this extension
    """
    bot.add_cog(Students(bot))
    bot.add_cog(Demonstrators(bot))


def getQueue(serverName: str):
    """
    Get the relevant queue for the server
    :param serverName: the server you want the queue for
    :return: The queue for the server
    """
    if serverName in queues.keys():
        return queues.get(serverName)
    else:
        queues[serverName] = []
        return queues.get(serverName)


def getCustomAddMessage(serverName: str):
    """
    Gets the custom add message for the server
    :param serverName: the server you want the queue for
    :return: The add message for this server.
    """
    with shelve.open('addMessage.shelve') as db:
        if str(serverName) in db:
            return db.get(str(serverName))
        else:
            return 'Please join the `Wait for help` voice channel and wait to moved to another voice channel'


class Demonstrators(commands.Cog):
    """
    Commands for demonstrators and Admins.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def setAddMessage(self, ctx: Context, *, message: str):
        """
        Change the default add message.
        :param message: The new add message to set.
        """
        logging.info('{0} setAddMessage {1}'.format(ctx.guild, message))
        with shelve.open('addMessage.shelve') as db:
            db[str(ctx.guild)] = message
        await ctx.send('Anyone added to queue will see this msg:\n' + message)

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def next(self, ctx: Context):
        """
        Get the next student in the queue.
        """
        if len(getQueue(ctx.guild)) > 0:
            next = getQueue(ctx.guild).pop(0)
            logging.info('{0} next {1}'.format(ctx.guild, next))
            if next is not None:
                await ctx.send(
                    'The next student in the queue is {0}, {1} will be with you shortly to signoff or help you.'.format(
                        next, ctx.message.author.mention))
        else:
            await ctx.send('No more students in the queue.')

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def print(self, ctx: Context):
        """
        Print out the students in the queue.
        """
        logging.info('{0} queue {1}'.format(ctx.guild, getQueue(ctx.guild)))
        queue = getQueue(ctx.guild)
        if queue is None or len(queue) == 0:
            await ctx.send('No students in the Queue.')
        else:
            await ctx.send('Remaining students in the queue are {0}'.format(listPrint(queue)))


class Students(commands.Cog):
    """
    Commands for students
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx: Context):
        """
        Adds the student to the help queue.
        """
        s = ctx.message.author.mention
        q = getQueue(ctx.guild)
        if s not in q:
            q.append(s)
            logging.info('{0} add {1}'.format(ctx.guild, s))
            await ctx.send(s + ' has been added to the queue. ' + getCustomAddMessage(ctx.guild))
        else:
            await ctx.send(s + ' is already in the queue.')

    @commands.command()
    async def remove(self, ctx: Context):
        """
        Removes the student from the help queue.
        """
        s = ctx.message.author.mention
        q = getQueue(ctx.guild)
        if s in q:
            q.remove(s)
            logging.info('{0} remove {1}'.format(ctx.guild, s))
            await ctx.send(s + ' has been removed from queue.')
        else:
            await ctx.send(s + ' is not in the queue.')
