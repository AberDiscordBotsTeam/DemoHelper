import asyncio
import logging
import shelve

from discord.ext import commands
from discord.ext.commands import Context

from cogs import adminRoles, addMessageFile


def setup(bot):
    """
    Setup the cogs in this extension
    """
    bot.add_cog(Utilities(bot))


class Utilities(commands.Cog):
    """
    General Utilities
    """

    @commands.command()
    @commands.has_any_role(*adminRoles)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: Context):
        """
        Clears all messages in a channel that are less than 14 days old
        """
        counter = 0
        async for message in ctx.channel.history(limit=1000):
            counter += 1
        await ctx.channel.purge()
        await ctx.channel.send('Success! Messages deleted: `' + str(counter) + '`, this message will delete in 5 '
                                                                               'seconds')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def setAddMessage(self, ctx: Context, *, message: str):
        """
        Change the default add message
        :param message: The new add message to set.
        """
        logging.info('{0} setAddMessage {1}'.format(ctx.guild, message))
        with shelve.open(addMessageFile) as db:
            db[str(ctx.guild)] = message
        await ctx.send('Anyone added to queue will see this msg:\n' + message)

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def resetAddMessage(self, ctx: Context):
        """
        Resets the custom add message
        """
        serverName = ctx.guild
        with shelve.open(addMessageFile) as db:
            if str(serverName) in db:
                db.pop(str(serverName))
                return await ctx.send('Custom add message has been reset')

    @commands.command()
    async def ping(self, ctx: Context):
        """
        Status check
        """
        import time
        start_time = time.time()
        message = await ctx.send('pong. `DWSP latency: ' + str(round(ctx.bot.latency*1000)) + 'ms`')
        end_time = time.time()
        await message.edit(content='pong. `DWSP latency: ' + str(round(ctx.bot.latency*1000)) + 'ms` '
                            '`Response time: ' + str(round(end_time-start_time, 3)) + 'ms`')