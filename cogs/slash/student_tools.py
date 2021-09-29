import newrelic.agent
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, ComponentContext, ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, wait_for_component, create_button

from helpers.queue_management import get_queue, _QUEUE


@newrelic.agent.background_task(name='cogs.slash.student_tools.add_to_queue', group='Task')
async def add_to_queue(ctx) -> str:
    queue = get_queue(ctx.guild.id)

    if ctx.author.voice is None:
        return f'You are not in a voice channel.'

    if ctx.author not in queue:
        _QUEUE[ctx.guild.id].append(ctx.author)
        return f'You have been added to the queue.'
    else:
        return f'You are already in the queue.'


@newrelic.agent.background_task(name='cogs.slash.student_tools.remove_from_queue', group='Task')
async def remove_from_queue(ctx) -> str:
    queue = get_queue(ctx.guild.id)
    user = ctx.author

    if user in queue:
        queue.remove(user)
        return f'You have been removed from the queue.'
    else:
        return f'You are not in the queue.'


@newrelic.agent.background_task(name='cogs.slash.student_tools.my_position_in_queue', group='Task')
async def my_position_in_queue(ctx, button_ctx) -> None:
    queue = get_queue(ctx.guild.id)
    user = ctx.author

    if user in queue:
        await button_ctx.edit_origin(
            content=f'You are in position `{queue.index(user)}`.',
            components=[]
        )
    else:
        await button_ctx.edit_origin(
            content=f'You are not in the queue.',
            components=[]
        )


class StudentTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name='student_tools',
        description='A collection of tools for students'
    )
    @newrelic.agent.background_task(name='cogs.slash.student_tools.StudentTools.command__slash__student_tools',
                                    group='Task')
    async def command__slash__student_tools(self, ctx: SlashContext) -> None:
        buttons = [
            create_button(style=ButtonStyle.blurple, label='Add To Queue', custom_id='Add To Queue'),
            create_button(style=ButtonStyle.blurple, label='Remove From Queue', custom_id='Remove From Queue'),
            create_button(style=ButtonStyle.blurple, label='My Position In Queue', custom_id='My Position In Queue')
        ]
        await ctx.send(content='Please select a utility.', components=[create_actionrow(*buttons)], hidden=True)

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(*buttons)])

        if button_ctx.custom_id == 'Add To Queue':
            await button_ctx.edit_origin(content=await add_to_queue(ctx), components=[])
        elif button_ctx.custom_id == 'Remove From Queue':
            await button_ctx.edit_origin(content=await remove_from_queue(ctx), components=[])
        elif button_ctx.custom_id == 'My Position In Queue':
            await my_position_in_queue(ctx, button_ctx)

    @cog_ext.cog_slash(
        name='add',
        description='Add yourself to the queue'
    )
    @newrelic.agent.background_task(name='cogs.slash.student_tools.StudentTools.command__slash__student_tools_add',
                                    group='Task')
    async def command__slash__student_tools_add(self, ctx: SlashContext) -> None:
        await ctx.send(content=await add_to_queue(ctx))

    @cog_ext.cog_slash(
        name='remove',
        description='Remove yourself from the queue'
    )
    @newrelic.agent.background_task(name='cogs.slash.student_tools.StudentTools.command__slash__student_tools_remove',
                                    group='Task')
    async def command__slash__student_tools_remove(self, ctx: SlashContext) -> None:
        await ctx.send(content=await remove_from_queue(ctx))
