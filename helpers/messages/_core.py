
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


def message__custom__stop(message):
    return discord.Embed(
        title=f"{EMOTE_NO} STOP",
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
