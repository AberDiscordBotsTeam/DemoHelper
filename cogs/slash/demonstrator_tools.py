
import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import bot
from discord_slash import SlashContext, cog_ext, ComponentContext, ButtonStyle
from discord_slash.utils.manage_components import create_select_option, create_select, create_actionrow, \
    wait_for_component, create_button

from helpers.management import pull_to_voice, assign_role, update_member
from helpers.messages import message__warning__user_invalid_permissions
from helpers.queue_management import get_queue


async def next_student(ctx):
    queue = get_queue(ctx.guild)

    if len(queue) == 0:
        await ctx.edit_origin(
            content=f'The queue is empty.',
            components=[]
        )
        return

    next_student = queue.pop(0)

    if next_student is None:
        await ctx.edit_origin(
            content=f'There are no more students in the queue.',
            components=[]
        )
        return

    next_student = update_member(ctx, next_student)
    message = f'The next student in the queue is {next_student.mention}, '
    if await pull_to_voice(ctx, next_student):
        message = message + 'They have been moved to your help voice channel. '
    if await assign_role(ctx, next_student):
        message = message + 'They have been assigned the role to view this channel. '
    if message[-2:-1] == ',':
        message = message + f'{ctx.message.author.mention} can now help you in {ctx.channel.mention}.'

    await ctx.edit_origin(
        content=message,
        components=[]
    )


async def display_queue(ctx):
    queue = get_queue(ctx.guild)

    if queue is None or len(queue) == 0:
        await ctx.edit_origin(
            content=f'No students in the Queue.',
            components=[]
        )
    else:
        temp = ''
        for list_item in queue:
            temp += f'° {str(list_item.name)}'

        await ctx.edit_origin(
            content=f'`{len(queue)}` students in the queue:\n{temp}',
            components=[]
        )


async def clear_queue(ctx):
    (get_queue(ctx.guild)).clear()
    await ctx.edit_origin(
        content=f'The queue has been cleared.',
        components=[]
    )


async def clear_role(ctx):
    for role in ctx.guild.roles:
        if role.name == ctx.channel.name:
            roles = ctx.author.roles
            roles = filter(lambda r: r.id != role.id, roles)
            await ctx.author.edit(reason="Added the help role.", roles=roles)
    await ctx.edit_origin(
        content=f'Role cleared for {ctx.author.mention}',
        components=[]
    )


async def purge_channel(ctx):
    buttons = [
        create_button(style=ButtonStyle.green, label="yes", custom_id="yes"),
        create_button(style=ButtonStyle.red, label="no", custom_id="no")
    ]
    action_row = create_actionrow(*buttons)
    await ctx.edit_origin(content="Please confirm whether you want to clear messages?", components=[action_row])

    if ctx.custom_id == 'yes':
        counter = await ctx.channel.purge()
        await ctx.edit_origin(
            content=f'`{len(counter)}` messages have been successfully deleted.',
            components=[]
        )
    else:
        await ctx.edit_origin(
            content=f'Aborted.',
            components=[]
        )


class DemonstratorTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="demonstrator_tools",
        description="A collection of tools for demonstrators."
    )
    async def command__slash__demonstrator_tools(self, ctx: SlashContext):
        select = create_select(
            options=[
                create_select_option("Next", value="Next", emoji="👩"),

                create_select_option("Display Queue", value="Display Queue", emoji="✉"),

                create_select_option("Clear Queue", value="Clear Queue", emoji="✉"),
                create_select_option("Clear Role", value="Clear Role", emoji="✉"),

                create_select_option("Purge Channel", value="Purge Channel", emoji="✉")
            ],
            placeholder="Utility selection",
            min_values=1,
            max_values=1
        )
        await ctx.send("Please select a utility.", components=[create_actionrow(select)], hidden=True)

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(select)])

        if button_ctx == 'Next': next_student(button_ctx)
        elif button_ctx == 'Display Queue': display_queue(button_ctx)
        elif button_ctx == 'Clear Role': clear_role(button_ctx)
        elif button_ctx == 'Clear Queue': clear_queue(button_ctx)
        elif button_ctx == 'Purge Channel': purge_channel(button_ctx)
