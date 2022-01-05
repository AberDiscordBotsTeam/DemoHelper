import newrelic.agent
from discord import Member, ChannelType, Permissions

add_message_file = 'addMessage.shelve'


@newrelic.agent.background_task(name='helpers.management.move_user_to_voice_channel', group='Task')
async def move_user_to_voice_channel(ctx, user: Member) -> bool:
    """
    This function is responsible for moving the user to a voice channel.
    :param ctx:
    :param user:
    :return: was the movement successful?
    """
    if user.voice and user.voice.channel:
        voice_channel = None
        for channel in ctx.guild.channels:
            if channel.name == ctx.channel.name and channel.type is ChannelType.voice:
                voice_channel = channel
                break

        if voice_channel:
            bot_perms: Permissions = voice_channel.permissions_for(ctx.me)
            if bot_perms.move_members:
                await user.move_to(voice_channel)
                return True
    return False


@newrelic.agent.background_task(name='helpers.management.pull_to_voice', group='Task')
async def pull_to_voice(ctx, user: Member) -> (bool, str):
    """
    Attempts to pull a user to a voice channel with the same name as the current text channel.

    :param ctx: context of the current command from a text channel
    :param user: the user to move
    :returns: true or false based on whether the move was a success.
    """

    if user.voice:
        # find the relevant voice channel based on the text channel name
        voice_channel = None
        for channel in ctx.guild.channels:
            if channel.name == ctx.channel.name and channel.type is ChannelType.voice:
                voice_channel = channel
                break
        # move the user to the help channel
        if voice_channel:
            await user.move_to(voice_channel)
            return True, ''
        else:
            return False, 'channel does not exist'
    else:
        return False, 'user not in voice channel'


@newrelic.agent.background_task(name='helpers.management.assign_role', group='Task')
async def assign_role(ctx, member: Member) -> bool:
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


@newrelic.agent.background_task(name='helpers.management.update_member', group='Task')
def update_member(ctx, member: Member) -> Member:
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
