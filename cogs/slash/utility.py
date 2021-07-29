
import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord_slash import SlashContext, cog_ext, ComponentContext, ButtonStyle
from discord_slash.utils.manage_components import create_select_option, create_select, create_actionrow, \
    wait_for_component, create_button

from helpers.messages import message__warning__user_invalid_permissions


async def check_roles(ctx, button_ctx):
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


async def clear_messages(ctx, button_ctx):
    buttons = [
        create_button(style=ButtonStyle.green, label="yes", custom_id="yes"),
        create_button(style=ButtonStyle.red, label="no", custom_id="no")
    ]
    action_row = create_actionrow(*buttons)
    await button_ctx.edit_origin(content="Please confirm whether you want to clear messages?", components=[action_row])

    if button_ctx.custom_id == 'yes':
        counter = await ctx.channel.purge()
        await button_ctx.edit_origin(
            content=f'`{len(counter)}` messages have been successfully deleted.',
            components=[]
        )
    else:
        await button_ctx.edit_origin(
            content=f'Aborted.',
            components=[]
        )


async def demo_helper_invite_ink(button_ctx):
    await button_ctx.edit_origin(
        content=f'https://discord.com/oauth2/authorize?client_id=870279603103621162&permissions=3072&scope=bot%20applications.commands',
        components=[]
    )


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="utilities",
        description="A collection of utility actions for Demo Helper"
    )
    async def command__slash__utility__about(self, ctx: SlashContext):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send(embed=message__warning__user_invalid_permissions(), hidden=True)
            return
        select = create_select(
            options=[
                create_select_option("Check Roles", value="Check Roles", emoji="👩"),
                create_select_option("Clear Messages", value="Clear Messages", emoji="✉"),
                create_select_option("DemoHelper Invite Link", value="DemoHelper Invite Link", emoji="🌐")
            ],
            placeholder="Utility selection",
            min_values=1,
            max_values=1
        )
        await ctx.send("Please select a utility.", components=[create_actionrow(select)], hidden=True)

        button_ctx: ComponentContext = await wait_for_component(self.bot, components=[create_actionrow(select)])

        if button_ctx.values[0] == 'Check Roles': await check_roles(ctx, button_ctx)
        elif button_ctx.values[0] == 'Clear Messages': await clear_messages(ctx, button_ctx)
        elif button_ctx.values[0] == 'DemoHelper Invite Link': await demo_helper_invite_ink(button_ctx)
