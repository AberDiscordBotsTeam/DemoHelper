
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord_slash import SlashContext, cog_ext, ComponentContext, ButtonStyle
from discord_slash.utils.manage_components import create_select_option, create_select, create_actionrow, \
    wait_for_component, create_button

from helpers.queue_management import get_queue


async def add_to_queue(ctx):
    queue = get_queue(ctx.guild)
    user = ctx.message.author

    if user not in queue:
        queue.append(user)
        await ctx.edit_origin(
            content=f'You have been added to the queue',
            components=[]
        )
    else:
        await ctx.edit_origin(
            content=f'You are already in the queue.',
            components=[]
        )


async def remove_from_queue(ctx):
    queue = get_queue(ctx.guild)
    user = ctx.message.author

    if user in queue:
        queue.remove(user)
        await ctx.edit_origin(
            content=f'You have been removed from the queue.',
            components=[]
        )
    else:
        await ctx.edit_origin(
            content=f'You are not in the queue.',
            components=[]
        )


async def my_position_in_queue(ctx):
    queue = get_queue(ctx.guild)
    user = ctx.message.author

    if user in queue:
        await ctx.edit_origin(
            content=f'You are in position `{queue.index(user)}`.',
            components=[]
        )
    else:
        await ctx.edit_origin(
            content=f'You are not in the queue.',
            components=[]
        )


class StudentTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="student_tools",
        description="A collection of tools for students"
    )
    async def command__slash__student_tools(self, ctx: SlashContext):
        buttons = [
            create_button(style=ButtonStyle.blurple, label="Add To Queue", custom_id="Add To Queue"),
            create_button(style=ButtonStyle.blurple, label="Remove From Queue", custom_id="Remove From Queue"),
            create_button(style=ButtonStyle.blurple, label="My Position In Queue", custom_id="My Position In Queue")
        ]
        await ctx.send(content='Please select a utility.', components=[create_actionrow(*buttons)], hidden=True)

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(*buttons)])

        if button_ctx.values[0] == 'Add To Queue': await add_to_queue(button_ctx)
        elif button_ctx.values[0] == 'Remove From Queue': await remove_from_queue(button_ctx)
        elif button_ctx.values[0] == 'My Position In Queue"': await my_position_in_queue(button_ctx)
