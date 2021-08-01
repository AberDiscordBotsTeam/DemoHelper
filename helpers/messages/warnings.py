
import newrelic.agent
from helpers.messages._core import message__custom__stop


@newrelic.agent.background_task(name='helpers.messages.warnings.message__warning__user_invalid_permissions_administrator', group='Task')
def message__warning__user_invalid_permissions_administrator():
    return message__custom__stop(f"""
    This action requires administrative privileges.
    Please contact your server administrator.
    """)


@newrelic.agent.background_task(name='helpers.messages.warnings.message__warning__user_invalid_permissions_demonstrator', group='Task')
def message__warning__user_invalid_permissions_demonstrator():
    return message__custom__stop(f"""
    This action requires demonstrator privileges.
    Please contact your server administrator.
    """)
