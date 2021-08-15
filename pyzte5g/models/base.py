from ..exceptions import AccessError
import math


class Base():
    """ Base model class. """

    def __init__(self, session) -> None:
        self._session = session

    def _can_cast(self, val, instance):
        try:
            instance(val)
            return True
        except ValueError:
            return False

    def _bytes_to_human(self, size_bytes: int) -> str:
        """
            Convert bytes value to human readable format.
            Source: https://stackoverflow.com/a/14822210
        """
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def _cast_data_to_map(self, data: dict, map: tuple) -> dict:
        result = {}
        for key, api_key, instance in map:
            if data.get(api_key) and self._can_cast(data[api_key], instance):
                result[key] = instance(data[api_key])
        return result

    def _try_get_private(self, data: dict, key: str):
        result = data.get(key)
        if not result and not self._session.is_authenticated:
            raise AccessError('Attempted to access private value while session is not currently authenticated.')
        return result
