
from helpers.messages._core import message__custom__stop


def message__warning__user_invalid_permissions():
    return message__custom__stop(f"""
    This action requires administrative privileges.
    Please contact your server administrator.
    """)
