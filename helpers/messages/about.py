

import newrelic.agent
import os
from dotenv import load_dotenv
from helpers.messages._core import message__custom__info


@newrelic.agent.background_task(name='helpers.messages.about.message__info__about', group='Task')
def message__info__about() -> message__custom__info:
    return message__custom__info(f"""
__**Demo Helper**__
DemoHelper is a queue system for online practical where students can add themselves to the queue using the 
`/student_tools` menu, or simply through using `/add`.
    
When a demonstrator is free to help, they can get the next student using the `/demonstrator_tools` menu,
or simply through using `/next`.
    
    
__Source__
This was a fork of demoHelperBot by the AberDiscordBotsTeam
Original creator: Nathan Williams and Joel Adams
https://github.com/AberDiscordBotsTeam/demoHelperBot
Updates were made by https://github.com/Amheus


__Developers__
Amheus
Joel
Nathan
    """)


@newrelic.agent.background_task(name='helpers.messages.about.message__info__about', group='Task')
def message__info__help() -> message__custom__info:
    return message__custom__info(f"""
__**Demo Helper**__

**1. Commands**
1.1 `/add`
- This is used by users who want to add themselves to the queue.
- This function is also available under `/student_tools`.

1.2 `/demonstrator_tools`
- This is only usable to demonstrators.
- It holds relevant functions that a demonstrator would require.
- - `Next`
- - `Display Queue`
- - `Clear Queue`
- - `Clear Role`
- - `Purge Channel`

1.3 `/next`
- This is to make the bot easier to use.
- This function is also available under `/demonstrator_tools`.
- This is used for the demonstrator to get the next user the in the queue.

1.4 `/remove`
- This is used by users who want to remove themselves from the queue.
- This function is also available under `/student_tools`.

1.5 `/student_tools`
- This holds functions that students would require.
- - `Add To Queue`
- - `Remove From Queue`
- - `My Position In Queue`

1.6 `/utilities`
- This hold miscellaneous functions as listed below:
- - `Check Roles`
- - `Clear Messages`
- - `Ping`
- - `About`
- - `Feedback`
- - `Invite Link`
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
