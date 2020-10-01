from discord.ext import commands
from discord.ext.commands import Context


class General(commands.Cog):
    """
    General commands for everyone.
    """

    @commands.command()
    async def source(self, ctx: Context):
        """
        Print a link to the DemoHelper source code
        """
        await ctx.send(content='Created by `Nathan Williams`\nMaintained by `Joel Adams`\n'
                               'https://github.com/AberDiscordBotsTeam/demoHelperBot')

    @commands.command()
    async def info(self, ctx: Context):
        """
        Display some info about how the bot works
        """
        await ctx.send('DemoHelper is a queue system for online practical where students can add themselves to the '
                       'queue using `!add`. When a demonstrator is free to help, they can call the `!next` command to '
                       'get the next waiting student.')

    @commands.command()
    async def feedback(self, ctx: Context):
        """
        Report feedback or issues with the bot
        """
        await ctx.send('If the bot is broken or you have any feedback you\'d like to submit please join '
                       'https://discord.gg/b3EdxVK and post a message in the <#740966780079571105> or '
                       '<#740967688876327012> channels')

    @commands.command()
    async def ping(selfself, ctx:Context):
        """
        status check
        """
        await ctx.send('pong')
