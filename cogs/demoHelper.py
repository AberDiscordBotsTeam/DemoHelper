import asyncio

import discord
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import Context

import logging
import shelve

from helpers import listPrint

queues = {'dummy': []}
# Possible roles available for the user to add allowing them to use all the bot commands
adminRoles = ['Demonstrator', 'demonstrator', 'DEMONSTRATOR', 'Admin role', 'ADMIN ROLE', 'Admin', 'Devs', 'lecturer',
              'LECTURER', 'advisor']

# somewhere to store the last message sent per guild per channel.
# key used is the guild name + the channel name.
# using ctx.message.delete() to the message that called a particular command.
# any messages sent that you want cleared next time bot is used
# save into prevMessages e.g prevMessages[k] = await ctx.send(...)
prevMessages = {'dummy':None}

async def rmPrevMessage(ctx:Context,k):
    """
    remove the message associated with the key (k) from the store and delete it if it still exists on the server.
    called on the commands you want to remove the previous message before putting in new one.
    """
    if k in prevMessages.keys():
        prevM = prevMessages[k]
        if prevM:
            botPerms: Permissions = ctx.channel.permissions_for(ctx.me)
            if botPerms.manage_messages: # only do if bot has permission otherwise ignore
                try:
                    await prevM.delete()
                except:
                    pass  # ignore
            prevMessages[k] = None


async def rmCMDMessage(ctx:Context):
    """
    delete the command message for the context provided if bot has required perms.
    """
    botPerms: Permissions = ctx.channel.permissions_for(ctx.me)
    if botPerms.manage_messages: # only do if bot has permission otherwise ignore
        await ctx.message.delete()


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
            return 'Please join the `Wait for help` voice channel and wait to be moved to another voice channel'


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
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx,k)

        if len(getQueue(ctx.guild)) > 0:
            next = getQueue(ctx.guild).pop(0)
            logging.info('{0} next {1}'.format(ctx.guild, next))
            if next is not None:
                prevMessages[k] = await ctx.send(
                    'The next student in the queue is {0}, {1} will be with you shortly to signoff or help you.'.format(
                        next, ctx.message.author.mention))
        else:
            prevMessages[k] = await ctx.send('No more students in the queue.')
        await rmCMDMessage(ctx)

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def print(self, ctx: Context):
        """
        Print out the students in the queue.
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx,k)

        logging.info('{0} queue {1}'.format(ctx.guild, getQueue(ctx.guild)))
        queue = getQueue(ctx.guild)
        if queue is None or len(queue) == 0:
            prevMessages[k] = await ctx.send('No students in the Queue.')
        else:
            prevMessages[k] = await ctx.send('Remaining students in the queue are {0}'.format(listPrint(queue)))
        await rmCMDMessage(ctx)


    @commands.command()
    @commands.has_any_role(*adminRoles)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: Context):
        """
        Clears all messages that are less than 14 days old
        """
        counter = 0
        async for message in ctx.channel.history(limit=1000):
                counter += 1
        await ctx.channel.purge()
        await ctx.channel.send('Success! Messages deleted: `' + str(counter) + '`, this message will delete in 5 '
                                                                               'seconds')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)


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
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx,k)

        s = ctx.message.author.mention
        q = getQueue(ctx.guild)
        if s not in q:
            q.append(s)
            logging.info('{0} add {1}'.format(ctx.guild, s))
            prevMessages[k] = await ctx.send(s + ' has been added to the queue. ' + getCustomAddMessage(ctx.guild))
        else:
            prevMessages[k] = await ctx.send(s + ' is already in the queue.')
        await rmCMDMessage(ctx)

    @commands.command()
    async def remove(self, ctx: Context):
        """
        Removes the student from the help queue.
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx,k)

        s = ctx.message.author.mention
        q = getQueue(ctx.guild)
        if s in q:
            q.remove(s)
            logging.info('{0} remove {1}'.format(ctx.guild, s))
            prevMessages[k] = await ctx.send(s + ' has been removed from queue.')
        else:
            prevMessages[k] = await ctx.send(s + ' is not in the queue.')
        await rmCMDMessage(ctx)
