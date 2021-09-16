
from discord.ext import commands
from discord.ext.commands import Context


class Standard(commands.Cog):
    """
    General Utilities
    """

    @commands.command()
    async def help(self, ctx: Context):
        await ctx.send(
            """
DemoHelper now utilises slash commands.
For more information, use `/utilities` and select `help` from the menu!
            """
        )