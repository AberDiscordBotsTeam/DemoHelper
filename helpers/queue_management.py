

_QUEUE = {'dummy': []}


def get_queue(guild_snowflake: str):
    """
    Get the relevant queue for the server

    :param guild_snowflake: the server you want the queue for
    :return: The queue for the server
    """
    if guild_snowflake in _QUEUE.keys():
        return _QUEUE.get(guild_snowflake)
    else:
        _QUEUE[guild_snowflake] = []
        return _QUEUE.get(guild_snowflake)
