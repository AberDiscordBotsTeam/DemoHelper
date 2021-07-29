
from helpers.messages._core import message__custom__error, message__custom__warning


def message__custom__error__check_failure(error):
    return message__custom__error(f"""
{error}
    """)


def message__custom__error__missing_required_argument():
    return message__custom__error(f"""
You are missing a required argument.
    """)


def message__custom__error__command_not_found():
    return message__custom__error(f"""
You are missing a required argument.
    """)


def message__custom__error__bad_argument():
    return message__custom__error(f"""
Bad argument.
    """)


def message__custom__error__rate_limited():
    return message__custom__warning(f"""
DemoHelper is currently being rate limited by Discord due to high traffic.
    """)


def message__custom__error__unknown_error():
    return message__custom__error(f"""
An unknown error occured.
Please contact support@samlewis.dev ASAP with details and screenshots of this incident.
    """)
