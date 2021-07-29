from discord import Member, ChannelType
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import Context

import logging
import shelve
from main import prefix

from cogs import admin_roles, add_message_file
from main import logger as logging

queues = {'dummy': []}

# somewhere to store the last message sent per guild per channel.
# key used is the guild name + the channel name.
# using ctx.message.delete() to the message that called a particular command.
# any messages sent that you want cleared next time bot is used
# save into prevMessages e.g prevMessages[k] = await ctx.send(...)
previous_messages = {'dummy': None}


async def remove_previous_message(ctx: Context, previous_messages_keys):
    """
    remove the message associated with the key (k) from the store and delete it if it still exists on the server.
    called on the commands you want to remove the previous message before putting in new one.
    """
    if previous_messages_keys in previous_messages.keys():
        previous_message = previous_messages[previous_messages_keys]
        if previous_message:
            bot_permissions: Permissions = ctx.channel.permissions_for(ctx.me)
            if bot_permissions.manage_messages:  # only do if bot has permission otherwise ignore
                try:
                    await previous_message.delete()
                except:
                    pass  # ignore
            previous_messages[previous_messages_keys] = None


async def remove_command_message(ctx: Context):
    """
    delete the command message for the context provided if bot has required perms.
    """
    bot_permissions: Permissions = ctx.channel.permissions_for(ctx.me)
    if bot_permissions.manage_messages:  # only do if bot has permission otherwise ignore
        await ctx.message.delete()


def setup(bot):
    """
    Setup the cogs in this extension
    """
    bot.add_cog(Students(bot))
    bot.add_cog(Demonstrators(bot))


def get_queue(server_name: str):
    """
    Get the relevant queue for the server

    :param server_name: the server you want the queue for
    :return: The queue for the server
    """
    if server_name in queues.keys():
        return queues.get(server_name)
    else:
        queues[server_name] = []
        return queues.get(server_name)


def list_print(list):
    """
    Prints out a list in a less developery way.
    :param list: the list to print
    :return: the generated string from the list.
    """
    temp = ''
    for list_item in list:
        temp += f'{str(list_item.name)}, '
    return temp[:-2]


def get_custom_add_message(server_name: str):
    """
    Gets the custom add message for the server

    :param server_name: the server you want the queue for
    :return: The add message for this server.
    """
    with shelve.open(add_message_file) as db:
        if str(server_name) in db:
            return db.get(str(server_name))
        else:
            return 'Please join the `Wait for help` voice channel and wait to be moved to another voice channel.'


def update_member(ctx: Context, member: Member):
    """
    If you have a member object from a previous command that needs updating. This function is for you.

    :param ctx: the discord message context to get updated member form
    :param member: the outdated member object,
        it uses id to get the members so you could pass a simple m.id = 2324534 object if you really want to.
    """
    for guild_member in ctx.guild.members:
        if guild_member.id == member.id:
            return guild_member
    return member


async def pull_to_voice(ctx: Context, user: Member):
    """
    Attempts to pull a user to a voice channel with the same name as the current text channel.

    :param ctx: context of the current command from a text channel
    :param user: the user to move
    :returns: true or false based on whether the move was a success.
    """

    # check user is in a voice channel
    if user.voice and user.voice.channel:
        # find the relevant voice channel based on the text channel name
        voice_channel = None
        for channel in ctx.guild.channels:
            if channel.name == ctx.channel.name and channel.type is ChannelType.voice:
                voice_channel = channel
                break
        # move the user to the help channel
        if voice_channel:
            # check we have correct perms
            bot_perms: Permissions = voice_channel.permissions_for(ctx.me)
            if bot_perms.move_members:
                print(bot_perms.move_members)
                await user.move_to(voice_channel)
                return True
            print("no perms")

            return False
        else:
            print("no channel")
            return False
    else:
        print("user not in voice")
        return False


async def assign_role(ctx: Context, member: Member):
    """
    Attempts to assign a member a role with the same name as the channel name the command was sent in.

    :param ctx: context of the command
    :param member: the member to assign the role to
    :returns: true or false depending on if the assignment was successful
    """

    # check we have correct perms
    bot_perms: Permissions = ctx.channel.permissions_for(ctx.me)
    if not bot_perms.manage_roles:
        return False

    # resolve the role name into a role object
    for guild_role in ctx.guild.roles:
        if guild_role.name == ctx.channel.name:
            # get the members role
            roles = member.roles
            # add the relevant role
            already_has_role = False
            for role in roles:
                if role.id == guild_role.id:
                    already_has_role = True
            if not already_has_role:
                roles.append(guild_role)
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
    @commands.has_any_role(*admin_roles)
    async def next(self, ctx: Context):
        """
        Gets next student in the queue and moves them to the vc 
        
        (Aliases: n)
        If this doesn't work use !checkRoles to see if the bot has sufficient roles to do this
        It will attempt to assign a role with a matching name.
        You can use !clearRole command to clear the role if one was set.
        """
        k = ctx.guild.name + ctx.channel.name
        await remove_previous_message(ctx, k)

        queue = get_queue(ctx.guild)

        if len(queue) > 0:
            next_student = queue.pop(0)
            logging.info(f'{ctx.guild}: #{ctx.channel.name} next student is {next_student} by {ctx.message.author}')
            if next_student is not None:
                next_student = update_member(ctx, next_student)
                message = f'The next student in the queue is {next_student.mention}, '
                if await pull_to_voice(ctx, next_student):
                    message = message + 'They have been moved to your help voice channel. '
                if await assign_role(ctx, next_student):
                    message = message + 'They have been assigned the role to view this channel. '
                if message[-2:-1] == ',':
                    message = message + f'{ctx.message.author.mention} can now help you in {ctx.channel.mention}.'
                previous_messages[k] = await ctx.send(message)
        else:
            previous_messages[k] = await ctx.send('No more students in the queue.')
        await remove_command_message(ctx)

    @commands.command(aliases=['cr'])
    @commands.has_any_role(*admin_roles)
    @commands.bot_has_permissions(manage_roles=True)
    async def clear_role(self, ctx: Context, user: Member):
        """
        Clear the role matching the channel name from a User

        (Aliases: cr)
        :param ctx: Context
        :param user: The user to remove the role from  use ( @User ) syntax
        """
        k = ctx.guild.name + ctx.channel.name
        await remove_previous_message(ctx, k)
        for role in ctx.guild.roles:
            if role.name == ctx.channel.name:
                roles = user.roles
                roles = filter(lambda r: r.id != role.id, roles)
                await user.edit(reason="adding help role", roles=roles)
        await ctx.send(f'Role cleared for {user.mention}')
        logging.info(
            f'{ctx.guild}: #{ctx.channel.name} cleared roles for {user} by {ctx.message.author}')
        await remove_command_message(ctx)

    @commands.command(aliases=['cq'])
    @commands.has_any_role(*admin_roles)
    async def clear_queue(self, ctx: Context):
        """
        Clears the queue (Aliases: cq)
        """
        logging.info(f'{ctx.guild}: #{ctx.channel.name} cleared queue by {ctx.message.author}')
        (get_queue(ctx.guild)).clear()
        await ctx.send('The queue has been cleared.')

    @commands.command(aliases=['queue'])
    @commands.has_any_role(*admin_roles)
    async def print_users(self, ctx: Context):
        """
        Print out the students in the queue (Aliases: queue)
        """
        k = ctx.guild.name + ctx.channel.name
        await remove_previous_message(ctx, k)

        logging.info(f'{ctx.guild}: #{ctx.channel.name} print users {get_queue(ctx.guild)}')
        queue = get_queue(ctx.guild)
        temp = []
        for queue_item in queue:
            temp.append(queue_item)
        queue = temp
        if queue is None or len(queue) == 0:
            await ctx.send('No students in the Queue.')
        else:
            await ctx.send(f'`{len(queue)}` students in the queue: {list_print(queue)}')
        await remove_command_message(ctx)


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
        await remove_previous_message(ctx, k)

        s = ctx.message.author
        q = get_queue(ctx.guild)
        if s not in q:
            q.append(s)
            logging.info(f'{ctx.guild}: #{ctx.channel.name} added student to queue {s}')
            previous_messages[k] = await ctx.send(
                f'{s.mention}, you have been added to the queue at position {q.index(s)}. {get_custom_add_message(ctx.guild)}'
            )
        else:
            logging.info(
                f'{ctx.guild}: #{ctx.channel.name} added student to queue (already in queue) {s}'
            )
            previous_messages[k] = await ctx.send(
                f'{s.mention}, you are already in the queue at position `{s}`.'
            )
        await remove_command_message(ctx)

    @commands.command(aliases=['r'])
    async def remove(self, ctx: Context):
        """
        Removes the student from the help queue (Aliases: r)
        """
        k = ctx.guild.name + ctx.channel.name
        await remove_previous_message(ctx, k)

        s = ctx.message.author
        q = get_queue(ctx.guild)
        if s in q:
            q.remove(s)
            logging.info(f'{ctx.guild}: #{ctx.channel.name} removed {s}')
            previous_messages[k] = await ctx.send(f'{s.mention}, you have been removed from queue.')
        else:
            logging.info(f'{ctx.guild}: #{ctx.channel.name} removed (not in queue) {s}')
            previous_messages[k] = await ctx.send(f'{s.mention}, you are not in the queue.')
        await remove_command_message(ctx)

    @commands.command(aliases=['p'])
    async def print(self, ctx: Context):
        """
        Print out the student's position in the queue (Aliases: p)
        """
        k = ctx.guild.name + ctx.channel.name
        await remove_previous_message(ctx, k)

        s = ctx.message.author
        q = get_queue(ctx.guild)
        if s in q:
            logging.info(f'{ctx.guild}: #{ctx.channel.name} student print {s}')
            await ctx.send(f'{s.mention}, you are in position `{q.index(s)}` in the queue')
        else:
            logging.info(f'{ctx.guild}: #{ctx.channel.name} student print (not in queue) {s}')
            await ctx.send(f'{s.mention}, you are not in the queue. Please add yourself using {prefix}add')
        await remove_command_message(ctx)
