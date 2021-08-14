import math


def can_cast(val, instance):
    try:
        instance(val)
        return True
    except ValueError:
        return False

def convert_size(size_bytes):
    """
        Convert data usage value to human readable format.
        Source: https://stackoverflow.com/a/14822210
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
