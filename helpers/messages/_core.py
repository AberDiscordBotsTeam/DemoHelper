
import newrelic.agent
import discord

# --------------------------------------------------

EMOTE_WARNING = ":warning:"
EMOTE_STOP = ":octagonal_sign:"
EMOTE_NO = ":no_entry:"
# EMOTE_NO = ":no_entry_sign:"
# EMOTE_NO = ":x:"
EMOTE_INFO = ":information_source:"


# --------------------------------------------------


@newrelic.agent.background_task(name='helpers.messages._core.message__custom__error', group='Task')
def message__custom__error(message: str) -> discord.Embed:
    return discord.Embed(
        title=f"{EMOTE_STOP} ERROR",
        description=f"""
        {message}
        """,
        colour=discord.Colour.red()
    )


@newrelic.agent.background_task(name='helpers.messages._core.message__custom__stop', group='Task')
def message__custom__stop(message: str) -> discord.Embed:
    return discord.Embed(
        title=f"{EMOTE_NO} STOP",
        description=f"""
        {message}
        """,
        colour=discord.Colour.red()
    )


@newrelic.agent.background_task(name='helpers.messages._core.message__custom__warning', group='Task')
def message__custom__warning(message: str) -> discord.Embed:
    return discord.Embed(
        title=f"{EMOTE_WARNING} WARNING",
        description=f"""
        {message}
        """,
        colour=discord.Colour.orange()
    )


@newrelic.agent.background_task(name='helpers.messages._core.message__custom__info', group='Task')
def message__custom__info(message: str) -> discord.Embed:
    return discord.Embed(
        title=f"{EMOTE_INFO} INFORMATION",
        description=f"""
        {message}
        """,
        colour=discord.Colour.blue()
    )


# --------------------------------------------------
