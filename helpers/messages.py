
import discord

# --------------------------------------------------

EMOTE_WARNING = ":warning:"
EMOTE_STOP = ":octagonal_sign:"
EMOTE_NO = ":no_entry:"
# EMOTE_NO = ":no_entry_sign:"
# EMOTE_NO = ":x:"
EMOTE_INFO = ":information_source:"


# --------------------------------------------------


def message__custom__error(message):
    return discord.Embed(
        title=f"{EMOTE_STOP} ERROR",
        description=f"""
        {message}
        """,
        colour=discord.Colour.red()
    )


def message__custom__warning(message):
    return discord.Embed(
        title=f"{EMOTE_WARNING} WARNING",
        description=f"""
        {message}
        """,
        colour=discord.Colour.orange()
    )


def message__custom__info(message):
    return discord.Embed(
        title=f"{EMOTE_INFO} INFORMATION",
        description=f"""
        {message}
        """,
        colour=discord.Colour.blue()
    )


# --------------------------------------------------


def message__warning__user_invalid_permissions():
    return message__custom__warning(f"""
    This action requires administrative privileges.
    Please contact your server administrator.
    """)


def message__info__about():
    return message__custom__warning(f"""
__**Demo Helper**__
DemoHelper is a queue system for online practical where students can add themselves to the
queue using `!add`.
    
When a demonstrator is free to help, they can call the `!next` command to get the next waiting student.
    
    
__Source__
This is a fork of demoHelperBot by the AberDiscordBotsTeam
Original creator: Nathan Williams and Joel Adams
https://github.com/AberDiscordBotsTeam/demoHelperBot
    """)


def message__info__feedback():
    return message__custom__warning(f"""
If the bot is non-functional or you have feedback you would like to submit.
Then please join https://discord.gg/b3EdxVK and send a message in the <#740966780079571105> or <#740967688876327012> channels'

Alternatively, if you request is urgent, please contact support@samlewis.dev
    """)
