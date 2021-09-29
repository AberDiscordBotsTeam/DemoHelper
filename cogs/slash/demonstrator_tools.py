import newrelic.agent
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, ComponentContext, ButtonStyle
from discord_slash.utils.manage_components import create_select_option, create_select, create_actionrow, \
    wait_for_component, create_button

from helpers.management import pull_to_voice, assign_role, update_member
from helpers.permission_management import is_authorised_demonstrator
from helpers.queue_management import get_queue


@newrelic.agent.background_task(name='cogs.slash.demonstrator_tools.next_student', group='Task')
async def next_student(ctx) -> str:
    queue = get_queue(ctx.guild.id)

    if len(queue) == 0:
        return f'The queue is empty.'

    next_student_instance = queue.pop(0)

    if next_student_instance is None:
        return f'There are no more students in the queue.'

    next_member = update_member(ctx, next_student_instance)

    message = f'The next student in the queue is {next_member.mention}, '
    if await pull_to_voice(ctx, next_member):
        message = message + 'They have been moved to your help voice channel. '
    if await assign_role(ctx, next_member):
        message = message + 'They have been assigned the role to view this channel. '
    if message[-2:-1] == ',':
        message = message + f'{ctx.author.mention} can now help you in {ctx.channel.mention}.'

    return message


@newrelic.agent.background_task(name='cogs.slash.demonstrator_tools.display_queue', group='Task')
async def display_queue(ctx, button_ctx) -> None:
    queue = get_queue(ctx.guild.id)

    if queue is None or len(queue) == 0:
        await button_ctx.edit_origin(
            content=f'No students in the Queue.',
            components=[]
        )
    else:
        temp = ''
        for list_item in queue:
            temp += f'° {str(list_item.name)}\n'

        await button_ctx.edit_origin(
            content=f'`{len(queue)}` students in the queue:\n{temp}',
            components=[]
        )


@newrelic.agent.background_task(name='cogs.slash.demonstrator_tools.clear_queue', group='Task')
async def clear_queue(ctx, button_ctx) -> None:
    (get_queue(ctx.guild.id)).clear()
    await button_ctx.edit_origin(
        content=f'The queue has been cleared.',
        components=[]
    )


@newrelic.agent.background_task(name='cogs.slash.demonstrator_tools.clear_role', group='Task')
async def clear_role(ctx, button_ctx) -> None:
    for role in ctx.guild.roles:
        if role.name == ctx.channel.name:
            roles = ctx.author.roles
            roles = filter(lambda r: r.id != role.id, roles)
            await ctx.author.edit(reason="Added the help role.", roles=roles)
    await button_ctx.edit_origin(
        content=f'Role cleared for {ctx.author.mention}',
        components=[]
    )


@newrelic.agent.background_task(name='cogs.slash.demonstrator_tools.purge_channel', group='Task')
async def purge_channel(ctx, button_ctx) -> None:
    buttons = [
        create_button(style=ButtonStyle.green, label="yes", custom_id="yes"),
        create_button(style=ButtonStyle.red, label="no", custom_id="no")
    ]
    action_row = create_actionrow(*buttons)
    await button_ctx.edit_origin(content="Please confirm whether you want to clear messages?", components=[action_row])

    button_ctx: ComponentContext = await wait_for_component(ctx.bot, components=[action_row])

    if button_ctx.custom_id == 'yes':
        await button_ctx.edit_origin(
            content=f'Message deletion process has begun, '
                    f'if there are a lot of messages in this channel, '
                    f'this might take a while.',
            components=[]
        )

        await ctx.send(
            content=f'`{len(await ctx.channel.purge())}` messages have been successfully deleted.', hidden=True
        )
    else:
        await button_ctx.edit_origin(
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
    @newrelic.agent.background_task(
        name='cogs.slash.demonstrator_tools.DemonstratorTools.command__slash__demonstrator_tools', group='Task')
    async def command__slash__demonstrator_tools(self, ctx: SlashContext) -> None:
        if await is_authorised_demonstrator(ctx, 'NEW') is False: return

        select = create_select(
            options=[
                create_select_option('Next', value='Next', emoji="👩"),

                create_select_option('Display Queue', value='Display Queue', emoji="📟"),

                create_select_option('Clear Queue', value='Clear Queue', emoji="🧹"),
                create_select_option('Clear Role', value='Clear Role', emoji="🧹"),

                create_select_option('Purge Channel', value='Purge Channel', emoji="🧹")
            ],
            placeholder="Utility selection",
            min_values=1,
            max_values=1
        )
        await ctx.send("Please select a utility.", components=[create_actionrow(select)], hidden=True)

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(select)])

        if button_ctx.values[0] == 'Next':
            await button_ctx.edit_origin(content=await next_student(ctx), components=[])
        elif button_ctx.values[0] == 'Display Queue':
            await display_queue(ctx, button_ctx)
        elif button_ctx.values[0] == 'Clear Role':
            await clear_role(ctx, button_ctx)
        elif button_ctx.values[0] == 'Clear Queue':
            await clear_queue(ctx, button_ctx)
        elif button_ctx.values[0] == 'Purge Channel':
            await purge_channel(ctx, button_ctx)

    @cog_ext.cog_slash(
        name='next',
        description='Gets next student in the queue'
    )
    @newrelic.agent.background_task(
        name='cogs.slash.demonstrator_tools.DemonstratorTools.command__slash__demonstrator_tools_next', group='Task')
    async def command__slash__demonstrator_tools_next(self, ctx: SlashContext) -> None:
        await ctx.send(content=await next_student(ctx))
