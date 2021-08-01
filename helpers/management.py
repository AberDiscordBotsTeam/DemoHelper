
from discord import Member, ChannelType, Permissions
from discord.ext.commands import Context


add_message_file = 'addMessage.shelve'


async def move_user_to_voice_channel(ctx, user: Member):
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


async def pull_to_voice(ctx, user: Member):
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
            await user.move_to(voice_channel)
            return True
        else:
            print("no channel")
            return False
    else:
        print("user not in voice")
        return False


async def assign_role(ctx, member: Member):
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


def update_member(ctx, member: Member):
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

