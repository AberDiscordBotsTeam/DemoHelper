"""
Some helper functions
"""

def listPrint(list):
    """
    Prints out a list in a less developery way.
    :param list: the list to print
    :return: the generated string from the list.
    """
    out = ''
    for l in list:
        out = out + str(l) + ', '
    return out[:-2]