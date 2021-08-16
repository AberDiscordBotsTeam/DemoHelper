

import newrelic.agent
import os
from dotenv import load_dotenv
from helpers.messages._core import message__custom__info


@newrelic.agent.background_task(name='helpers.messages.about.message__info__about', group='Task')
def message__info__about() -> message__custom__info:
    return message__custom__info(f"""
__**Demo Helper**__
DemoHelper is a queue system for online practical where students can add themselves to the
queue using `!add`.
    
When a demonstrator is free to help, they can call the `!next` command to get the next waiting student.
    
    
__Source__
This is a fork of demoHelperBot by the AberDiscordBotsTeam
Original creator: Nathan Williams and Joel Adams
https://github.com/AberDiscordBotsTeam/demoHelperBot
    """)


@newrelic.agent.background_task(name='helpers.messages.about.message__info__feedback', group='Task')
def message__info__feedback() -> message__custom__info:
    return message__custom__info(f"""
If the bot is non-functional or you have feedback you would like to submit.
Then please join https://discord.gg/b3EdxVK and send a message in the <#740966780079571105> or <#740967688876327012> channels'

Alternatively, if you request is urgent, please contact support@samlewis.dev
    """)


@newrelic.agent.background_task(name='helpers.messages.about.message__info__invite_link', group='Task')
def message__info__invite_link() -> message__custom__info:
    load_dotenv()
    return message__custom__info(f"""
__DemoHelper Invite Link__:
{os.getenv('INVITE_URL')}
    """)
