import newrelic.agent

_QUEUE = {
    'dummy': []
}


@newrelic.agent.background_task(name='helpers.queue_management.get_queue', group='Task')
def get_queue(target_key: str):
    """
    Get the relevant queue for the server

    :param target_key: the server you want the queue for
    :return: The queue for the server
    """
    if target_key in _QUEUE.keys():
        return _QUEUE.get(target_key)
    else:
        _QUEUE[target_key] = []
        return _QUEUE.get(target_key)
