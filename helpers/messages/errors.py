
import newrelic.agent
from helpers.messages._core import message__custom__error, message__custom__warning


@newrelic.agent.background_task(name='helpers.messages.errors.message__custom__error__check_failure', group='Task')
def message__custom__error__check_failure(error) -> message__custom__error:
    return message__custom__error(f"""
{error}
    """)


@newrelic.agent.background_task(name='helpers.messages.errors.message__custom__error__missing_required_argument', group='Task')
def message__custom__error__missing_required_argument() -> message__custom__error:
    return message__custom__error(f"""
You are missing a required argument.
    """)


@newrelic.agent.background_task(name='helpers.messages.errors.message__custom__error__command_not_found', group='Task')
def message__custom__error__command_not_found() -> message__custom__error:
    return message__custom__error(f"""
You are missing a required argument.
    """)


@newrelic.agent.background_task(name='helpers.messages.errors.message__custom__error__bad_argument', group='Task')
def message__custom__error__bad_argument() -> message__custom__error:
    return message__custom__error(f"""
Bad argument.
    """)


@newrelic.agent.background_task(name='helpers.messages.errors.message__custom__error__rate_limited', group='Task')
def message__custom__error__rate_limited() -> message__custom__warning:
    return message__custom__warning(f"""
DemoHelper is currently being rate limited by Discord due to high traffic.
    """)


@newrelic.agent.background_task(name='helpers.messages.errors.message__custom__error__unknown_error', group='Task')
def message__custom__error__unknown_error() -> message__custom__error:
    return message__custom__error(f"""
An unknown error occured.
Please contact support@samlewis.dev ASAP with details and screenshots of this incident.
    """)
