
from helpers.messages._core import message__custom__stop


def message__warning__user_invalid_permissions_administrator():
    return message__custom__stop(f"""
    This action requires administrative privileges.
    Please contact your server administrator.
    """)


def message__warning__user_invalid_permissions_demonstrator():
    return message__custom__stop(f"""
    This action requires demonstrator privileges.
    Please contact your server administrator.
    """)
