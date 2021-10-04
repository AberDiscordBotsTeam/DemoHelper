from discord import Member, ChannelType
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import Context

import logging
import shelve
from demobot import prefix

from cogs import adminRoles, addMessageFile
from demobot import logger as logging

queues = {'dummy': []}

# somewhere to store the last message sent per guild per channel.
# key used is the guild name + the channel name.
# using ctx.message.delete() to the message that called a particular command.
# any messages sent that you want cleared next time bot is used
# save into prevMessages e.g prevMessages[k] = await ctx.send(...)
prevMessages = {'dummy': None}


async def rmPrevMessage(ctx: Context, k):
    """
    remove the message associated with the key (k) from the store and delete it if it still exists on the server.
    called on the commands you want to remove the previous message before putting in new one.
    """
    if k in prevMessages.keys():
        prevM = prevMessages[k]
        if prevM:
            botPerms: Permissions = ctx.channel.permissions_for(ctx.me)
            if botPerms.manage_messages:  # only do if bot has permission otherwise ignore
                try:
                    await prevM.delete()
                except:
                    pass  # ignore
            prevMessages[k] = None


async def rmCMDMessage(ctx: Context):
    """
    delete the command message for the context provided if bot has required perms.
    """
    botPerms: Permissions = ctx.channel.permissions_for(ctx.me)
    if botPerms.manage_messages:  # only do if bot has permission otherwise ignore
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


def listPrint(list):
    """
    Prints out a list in a less developery way.
    :param list: the list to print
    :return: the generated string from the list.
    """
    out = ''
    for l in list:
        out = out + str(l.name) + ', '
    return out[:-2]


def getCustomAddMessage(serverName: str):
    """
    Gets the custom add message for the server

    :param serverName: the server you want the queue for
    :return: The add message for this server.
    """
    with shelve.open(addMessageFile) as db:
        if str(serverName) in db:
            return db.get(str(serverName))
        else:
            return 'Please join the `Wait for help` voice channel and wait to be moved to another voice channel'


def updateMember(ctx: Context, m: Member):
    """
    If you have a member object from a previous command that needs updating. This function si for you.

    :param ctx: the discord message context to get updated member form
    :param m: the outdated member object,
        it uses id to get the members so you could pass a simple m.id = 2324534 object if you really want to.
    """
    for m1 in ctx.guild.members:
        if m1.id == m.id:
            return m1
    return m


async def pullToVoice(ctx: Context, user: Member):
    """
    Attempts to pull a user to a voice channel with the same name as the current text channel.

    :param ctx: context of the current command from a text channel
    :param user: the user to move
    :returns: true or false based on whether the move was a success.
    """

    # check user is in a voice channel
    if user.voice and user.voice.channel:
        # find the relevant voice channel based on the text channel name
        voiceChannel = None
        for channel in ctx.guild.channels:
            if channel.name == ctx.channel.name and channel.type is ChannelType.voice:
                voiceChannel = channel
                break
        # move the user to the help channel
        if voiceChannel:
            # check we have correct perms
            botPerms: Permissions = voiceChannel.permissions_for(ctx.me)
            if botPerms.move_members:
                print(botPerms.move_members)
                await user.move_to(voiceChannel)
                return True
            print("no perms")

            return False
        else:
            print("no channel")
            return False
    else:
        print("user not in voice")
        return False


async def assignRole(ctx: Context, member: Member):
    """
    Attempts to assign a member a role with the same name as the channel name the command was sent in.

    :param ctx: context of the command
    :param member: the member to assign the role to
    :returns: true or false depending on if the assignment was successful
    """

    # check we have correct perms
    botPerms: Permissions = ctx.channel.permissions_for(ctx.me)
    if not botPerms.manage_roles:
        return False

    # resolve the role name into a role object
    for role in ctx.guild.roles:
        if role.name == ctx.channel.name:
            # get the members role
            roles = member.roles
            # add the relevant role
            alreadyHasRole = False
            for r in roles:
                if r.id == role.id:
                    alreadyHasRole = True
            if not alreadyHasRole:
                roles.append(role)
                # replace their existing role list with updated one
                await member.edit(reason="adding help role", roles=roles)
            return True
    return False


class Demonstrators(commands.Cog):
    """
    Commands for demonstrators and Admins
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['n'])
    @commands.has_any_role(*adminRoles)
    async def next(self, ctx: Context):
        """
        Gets next student in the queue and moves them to the vc 
        
        (Aliases: n)
        If this doesn't work use !checkRoles to see if the bot has sufficient roles to do this
        It will attempt to assign a role with a matching name.
        You can use !clearRole command to clear the role if one was set.
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx, k)

        queue = getQueue(ctx.guild)

        if len(queue) > 0:
            nextStudent = queue.pop(0)
            logging.info('{0}: #{1} next student is {2} by {3}'.format(ctx.guild, ctx.channel.name, nextStudent, ctx.message.author))
            if nextStudent is not None:
                nextStudent = updateMember(ctx, nextStudent)
                message = 'The next student in the queue is {0}, '.format(
                    nextStudent.mention)
                if await pullToVoice(ctx, nextStudent):
                    message = message + 'They have been moved to your help voice channel. '
                if await assignRole(ctx, nextStudent):
                    message = message + 'They have been assigned the role to view this channel. '
                if message[-2:-1] == ',':
                    message = message + '{0} can now help you in {1}.' \
                        .format(ctx.message.author.mention, ctx.channel.mention)
                prevMessages[k] = await ctx.send(message)
        else:
            prevMessages[k] = await ctx.send('No more students in the queue.')
        await rmCMDMessage(ctx)

    @commands.command(aliases=['cr'])
    @commands.has_any_role(*adminRoles)
    @commands.bot_has_permissions(manage_roles=True)
    async def clearRole(self, ctx: Context, user: Member):
        """
        Clear the role matching the channel name from a User

        (Aliases: cr)
        :param ctx: Context
        :param user: The user to remove the role from  use ( @User ) syntax
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx, k)
        for role in ctx.guild.roles:
            if role.name == ctx.channel.name:
                roles = user.roles
                roles = filter(lambda r: r.id != role.id, roles)
                await user.edit(reason="adding help role", roles=roles)
        await ctx.send(f'Role cleared for {format(user.mention)}')
        logging.info('{0}: #{1} cleared roles for {2} by {3}'.format(ctx.guild, ctx.channel.name, user, ctx.message.author))
        await rmCMDMessage(ctx)

    @commands.command(aliases=['cq'])
    @commands.has_any_role(*adminRoles)
    async def clearQueue(self, ctx: Context):
        """
        Clears the queue (Aliases: cq)
        """
        logging.info('{0}: #{1} cleared queue by {2}'.format(ctx.guild, ctx.channel.name, ctx.message.author))
        q = getQueue(ctx.guild)
        q.clear()
        await ctx.send('The queue has been cleared')

    @commands.command(aliases=['queue'])
    @commands.has_any_role(*adminRoles)
    async def printUsers(self, ctx: Context):
        """
        Print out the students in the queue (Aliases: queue)
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx, k)

        logging.info('{0}: #{1} print users {2}'.format(ctx.guild, ctx.channel.name, getQueue(ctx.guild)))
        queue = getQueue(ctx.guild)
        temp = []
        for x in queue:
            temp.append(x)
        queue = temp
        if queue is None or len(queue) == 0:
            await ctx.send('No students in the Queue.')
        else:
            await ctx.send('`{0}` students in the queue: {1}'.format(len(queue), listPrint(queue)))
        await rmCMDMessage(ctx)

class Students(commands.Cog):
    """
    Commands for students
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['a'])
    async def add(self, ctx: Context):
        """
        Adds the student to the help queue (Aliases: a)
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx, k)

        s = ctx.message.author
        q = getQueue(ctx.guild)
        if s not in q:
            q.append(s)
            logging.info('{0}: #{1} added student to queue {2}'.format(ctx.guild, ctx.channel.name, s))
            prevMessages[k] = await ctx.send('{0}, you have been added to the queue at position `{1}`. {2}'.format(s.mention, (q.index(s) + 1), getCustomAddMessage(ctx.guild)))
        else:
            logging.info('{0}: #{1} added student to queue (already in queue) {2}'.format(ctx.guild, ctx.channel.name, s))
            prevMessages[k] = await ctx.send('{0}, you are already in the queue at position `{1}`.'.format(s.mention, (q.index(s) + 1)))
        await rmCMDMessage(ctx)

    @commands.command(aliases=['r'])
    async def remove(self, ctx: Context):
        """
        Removes the student from the help queue (Aliases: r)
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx, k)

        s = ctx.message.author
        q = getQueue(ctx.guild)
        if s in q:
            q.remove(s)
            logging.info('{0}: #{1} removed {2}'.format(ctx.guild, ctx.channel.name, s))
            prevMessages[k] = await ctx.send('{0}, you have been removed from queue.'.format(s.mention))
        else:
            logging.info('{0}: #{1} removed (not in queue) {2}'.format(ctx.guild, ctx.channel.name, s))
            prevMessages[k] = await ctx.send('{0}, you are not in the queue.'.format(s.mention))
        await rmCMDMessage(ctx)

    @commands.command(aliases=['p'])
    async def print(self, ctx: Context):
        """
        Print out the student's position in the queue (Aliases: p)
        """
        k = ctx.guild.name + ctx.channel.name
        await rmPrevMessage(ctx, k)

        s = ctx.message.author
        q = getQueue(ctx.guild)
        if s in q:
            logging.info('{0}: #{1} student print {2}'.format(ctx.guild, ctx.channel.name, s))
            await ctx.send('{0}, you are in position `{1}` in the queue'.format(s.mention, (q.index(s) + 1)))
        else:
            logging.info('{0}: #{1} student print (not in queue) {2}'.format(ctx.guild, ctx.channel.name, s))
            await ctx.send('{0}, you are not in the queue. Please add yourself using {1}add'.format(s.mention, prefix))
        await rmCMDMessage(ctx)
