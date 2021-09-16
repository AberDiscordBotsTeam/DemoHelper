import newrelic.agent
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, ComponentContext
from discord_slash.utils.manage_components import create_select_option, create_select, create_actionrow, \
    wait_for_component

from helpers.messages.about import message__info__about, message__info__feedback, message__info__invite_link, \
    message__info__help
from helpers.permission_management import is_authorised_demonstrator


@newrelic.agent.background_task(name='cogs.slash.utility.check_roles', group='Task')
async def check_roles(ctx, button_ctx) -> None:
    if await is_authorised_demonstrator(ctx, 'EDIT', button_ctx) is False: return
    perms = None
    for role in ctx.me.roles:
        print(role, ctx.me.name)
        if role.name[0:4] == 'Demo':  # need better way to do this crap.
            perms = role.permissions
            break
    # doesn't work.. perms = ctx.guild.permissions_for(ctx.me)
    if perms and not perms.move_members:
        await button_ctx.edit_origin(
            content=f'Bot requires Move Members permission(s)',
            components=[]
        )
    else:
        await button_ctx.edit_origin(
            content="""
            If you are reading this demoBot has all the permissions it needs for: `nextV2`.

            Just double check the help voice and text channels have matching names: 
            e.g. `help-1` `help-1` and not `help 1` `help-1`.

            Optionally:
            You can hide the help channels for `@everyone` and `verified`.
            And create matching `help-1` roles that has the permissions for the user to view/join the corresponding 
            `help-1` text and voice channels. You can also set the `help-1` role to hide channel history so the 
            student can't see the message history of the channel.
            """,
            components=[]
        )


@newrelic.agent.background_task(name='cogs.slash.utility.ping_test', group='Task')
async def ping_test(ctx, button_ctx) -> None:
    message_content = f'pong. `DWSP latency: {str(round(ctx.bot.latency * 1000))}ms`'
    await button_ctx.edit_origin(
        content=message_content,
        components=[]
    )


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="utilities",
        description="A collection of utility actions for Demo Helper"
    )
    @newrelic.agent.background_task(name='cogs.slash.utility.Utility.command__slash__utility', group='Task')
    async def command__slash__utility(self, ctx: SlashContext) -> None:
        select = create_select(
            options=[
                create_select_option('Check Roles', value='Check Roles', emoji='👩'),

                create_select_option('Ping', value='Ping', emoji='🏓'),
                create_select_option('About', value='About', emoji='ℹ'),
                create_select_option('Help', value='Help', emoji='ℹ️'),
                create_select_option('Feedback', value='Feedback', emoji='📣'),
                create_select_option('Invite Link', value='Invite Link', emoji='🌐')
            ],
            placeholder="Utility selection",
            min_values=1,
            max_values=1
        )
        await ctx.send(content="Please select a utility.", components=[create_actionrow(select)], hidden=True)

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(select)])

        if button_ctx.values[0] == 'Check Roles':
            await check_roles(ctx, button_ctx)

        elif button_ctx.values[0] == 'Ping':
            await ping_test(ctx, button_ctx)
        elif button_ctx.values[0] == 'About':
            await button_ctx.edit_origin(embed=message__info__about(), content='', components=[])
        elif button_ctx.values[0] == 'Help':
            await button_ctx.edit_origin(embed=message__info__help(), content='', components=[])
        elif button_ctx.values[0] == 'Feedback':
            await button_ctx.edit_origin(embed=message__info__feedback(), content='', components=[])
        elif button_ctx.values[0] == 'Invite Link':
            await button_ctx.edit_origin(embed=message__info__invite_link(), content='', components=[])
