

_QUEUE = {'dummy': []}


def get_queue(server_name: str):
    """
    Get the relevant queue for the server

    :param server_name: the server you want the queue for
    :return: The queue for the server
    """
    if server_name in _QUEUE.keys():
        return _QUEUE.get(server_name)
    else:
        _QUEUE[server_name] = []
        return _QUEUE.get(server_name)
