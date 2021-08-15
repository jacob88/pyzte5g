from urllib.parse import urlencode
from cachetools import cached, TTLCache
from .base import Base


class DATAUsage(Base):
    """ Implements methods to fetch data usage metrics from the ZTE modem API. """

    DATA_USAGE_CMDS = (
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
    )
    DATA_USAGE_VAL_MAP = (
        ('used_bytes', 'datausage_usedamount', int),
        ('remaining_bytes', 'datausage_remainamount', int),
        ('used_percent', 'datausage_usedrate', float),
        ('remaining_percent', 'datausage_remainrate', float),
        ('total_bytes', 'datausage_allotedamount', int),
        ('remaining_days', 'datausage_remaindays', int),
        ('usage_warning', 'datausage_lowbalance', bool),
    )

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

        response = self._session.get_cmd_process(cmd=self.DATA_USAGE_CMDS)
        result = self._cast_data_to_map(data=response, map=self.DATA_USAGE_VAL_MAP)
        for source, key in [('used_bytes', 'used_data'), ('remaining_bytes', 'remaining_data'), ('total_bytes', 'total_data')]:
            if result.get(source):
                result[key] = self._bytes_to_human(result[source])
        return result
