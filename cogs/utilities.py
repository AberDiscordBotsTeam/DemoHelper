import asyncio
import logging
import shelve

from discord.ext import commands
from discord.ext.commands import Context

from cogs import adminRoles, addMessageFile
from demobot import logger as logging

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
    @commands.bot_has_permissions(manage_messages=True, manage_roles=True)
    async def checkRoles(self, ctx: Context):
        # check server wide perms
        perms = None
        for r in ctx.me.roles:
            print(r, ctx.me.name)
            if r.name[0:4] == 'Demo': # need better way to do this crap.
                perms = r.permissions
                break
        # doesn't work.. perms = ctx.guild.permissions_for(ctx.me)
        if perms and not perms.move_members:
            await ctx.send('Bot requires Move Members permission(s)')
        else:
            await ctx.send(
                """
                If you are reading this demoBot has all the permissions it needs for: `nextV2`.
                
                Just double check the help voice and text channels have matching names: 
                e.g. `help-1` `help-1` and not `help 1` `help-1`.
                
                Optionally:
                You can hide the help channels for `@everyone` and `verified`.
                And create matching `help-1` roles that has the permissions for the user to view/join the corresponding 
                `help-1` text and voice channels. You can also set the `help-1` role to hide channel history so the 
                student can't see the message history of the channel.
                """)

    @commands.command(aliases=['cm'])
    @commands.has_any_role(*adminRoles)
    @commands.bot_has_permissions(manage_messages=True)
    async def clearMessages(self, ctx: Context):
        """
        *Warning* Clears all messages in a channel
        that are less than 14 days old
        """
        msg = await ctx.send('Are you sure you want to clear messages?')
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        def check(_, user):
            return user == ctx.message.author

        reaction, _ = await ctx.bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == '👍':
            logging.info('{0}: #{1} messages cleared by {2}'.format(ctx.guild, ctx.channel.name, ctx.message.author))
            counter = await ctx.channel.purge()
            msg = await ctx.channel.send(f'Success! Messages deleted: `{len(counter)}`, this message will delete in 5 seconds')
            await asyncio.sleep(5)
            await msg.delete()
        elif str(reaction.emoji) == '👎':
            await msg.delete()
            await ctx.send('Messages have not been cleared')

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def setAddMessage(self, ctx: Context, *, message: str):
        """
        Change the default add message
        :param message: The new add message to set.
        """
        logging.info('{0}: #{1} setAddMessage to "{2}" by {3}'.format(ctx.guild, ctx.channel.name, message, ctx.message.author))
        with shelve.open(addMessageFile) as db:
            db[str(ctx.guild)] = message
        await ctx.send('Anyone added to queue will see this msg:\n' + message)

    @commands.command()
    @commands.has_any_role(*adminRoles)
    async def resetAddMessage(self, ctx: Context):
        """
        Resets the custom add message
        """
        logging.info('{0}: #{1} resteAddMessage by {2}'.format(ctx.guild, ctx.channel.name, ctx.message.author))
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
        message = await ctx.send('pong. `DWSP latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms`')
        end_time = time.time()
        await message.edit(content='🏓 pong `DWSP latency: ' + str(round(ctx.bot.latency * 1000)) + 'ms` ' +
                                   '`Response time: ' + str(int((end_time - start_time) * 1000)) + 'ms`')
        logging.info('{0}: #{1} ping by {2}'.format(ctx.guild, ctx.channel.name, ctx.message.author))
        
    @commands.command()
    async def getBotLink(self, ctx: Context):
        """
        Returns the link to invite this bot to your server
        """
        await ctx.send('https://discord.com/oauth2/authorize?client_id=690608026285244447&permissions=3072&scope=bot')
