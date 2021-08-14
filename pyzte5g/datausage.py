from urllib.parse import urlencode
from cachetools import cached, TTLCache
from .tools import can_cast, convert_size


class DATAUsage():
    """ Implements methods to fetch data usage metrics from the ZTE modem API. """

    DATA_USAGE_CMDS = [
        'datausage_remainamount',
        'datausage_remaindays',
        'datausage_remainrate',
        'datausage_lowbalance',
        'datausage_preactive',
        'datausage_syncresult',
        'datausage_prepaid',
        'datausage_rechargesiteurl',
        'datausage_plantype',
        'datausage_allotedamount',
        'datausage_usedamount',
        'datausage_usedrate',
    ]
    DATA_USAGE_VAL_MAP = [
        ('used_bytes', 'datausage_usedamount', int),
        ('remaining_bytes', 'datausage_remainamount', int),
        ('used_percent', 'datausage_usedrate', float),
        ('remaining_percent', 'datausage_remainrate', float),
        ('total_bytes', 'datausage_allotedamount', int),
        ('remaining_days', 'datausage_remaindays', int),
        ('usage_warning', 'datausage_lowbalance', bool),
    ]

    def __init__(self, session) -> None:
        self._session = session

    @property
    def used_bytes(self) -> int:
        """ Integer: Used data, reported in bytes. """
        return self.get_data_usage().get('used_bytes', 0)

    @property
    def remaining_bytes(self) -> int:
        """ Integer: Remaining data available, reported in bytes. """
        return self.get_data_usage().get('remaining_bytes', 0)

    @property
    def used_percent(self) -> float:
        """ Numeric: Used data, reported as a percentage. """
        return self.get_data_usage().get('used_percent', 0)

    @property
    def remaining_percent(self) -> float:
        """ Numeric: Remaining data available, reported as a percentage. """
        return self.get_data_usage().get('remaining_percent', 0)

    @property
    def total_bytes(self) -> int:
        """ Integer: Total plan data available, reported in bytes. """
        return self.get_data_usage().get('total_bytes', 0)

    @property
    def remaining_days(self) -> int:
        """ Integer: Number of days remaining before plan rolls over. """
        return self.get_data_usage().get('remaining_days', 0)

    @property
    def used_data(self) -> str:
        """ String: Used data, human readable, e.g. 146.5 GB. """
        return self.get_data_usage().get('used_data', '')

    @property
    def remaining_data(self) -> str:
        """ String: Remaining data available, human readable, e.g. 53.5 GB. """
        return self.get_data_usage().get('remaining_data', '')

    @property
    def total_data(self) -> str:
        """ String: Total plan data available, human readable, e.g. 200 GB. """
        return self.get_data_usage().get('total_data', '')

    @property
    def usage_warning(self) -> bool:
        """ Boolean: True if data usage warning has been reached. """
        return self.get_data_usage().get('usage_warning', False)

    @cached(cache=TTLCache(maxsize=16, ttl=5))
    def get_data_usage(self) -> dict:
        """
            Queries data usage metrics from the ZTE modem API.

            Returns:
                Dictionary Containing data usage metrics.
        """

        query = urlencode(
            dict(
                isTest=False,
                cmd=','.join(self.DATA_USAGE_CMDS),
                multi_data=1,
            )
        )
        response = self._session._make_request(
            url=self._session._build_cmd_url(path=self._session.GET_PROCESS_ENDPOINT, query=query),
            method='GET'
        )
        result = {}
        for key, api_key, instance in self.DATA_USAGE_VAL_MAP:
            if response.get(api_key) and can_cast(response[api_key], instance):
                result[key] = instance(response[api_key])
        for source, key in [('used_bytes', 'used_data'), ('remaining_bytes', 'remaining_data'), ('total_bytes', 'total_data')]:
            if result.get(source):
                result[key] = convert_size(result[source])
        return result
