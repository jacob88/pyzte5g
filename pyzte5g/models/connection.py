from cachetools import cached, LRUCache
from .base import Base


class Connection(Base):
    """ Implements methods to fetch ZTE modem connection information. """

    CONNECTION_CMDS = (
        'ppp_status',
        'lte_rsrp',
        'Z5g_rsrp',
        'msisdn_prepaid',
    )
    CONNECTION_VAL_MAP = (
        ('state', 'ppp_status', str),
        ('sig_strength_lte', 'lte_rsrp', int),
        ('sig_strength_5g', 'Z5g_rsrp', int),
        # ('mobile_number', 'msisdn_prepaid', str),
        ('wan_ipv4_addr', 'wan_ipaddr', str),
        ('wan_ipv6_addr', 'ipv6_wan_ipaddr', str),
    )

    @property
    def state(self) -> str:
        """
            String: Current state of the WAN connection.
                    e.g. ['ppp_disconnected', 'ppp_connecting', 'ipv4_ipv6_connected']
        """
        return self.get_connection().get('state', '')

    @property
    def is_connected(self) -> bool:
        return self.state == 'ipv4_ipv6_connected' or self.state not in ('ppp_disconnected', 'ppp_connecting')

    @property
    def sig_strength_lte(self) -> int:
        """
            Integer: Current LTE(4G) signal stregth, measured in dBm.
                     Private value, requires an authenticated session.
        """
        return self._try_get_private(data=self.get_connection(), key='sig_strength_lte')

    @property
    def sig_strength_5g(self) -> int:
        """
            Integer: Current 5G signal stregth, measured in dBm.
                     Private value, requires an authenticated session.
        """
        return self._try_get_private(data=self.get_connection(), key='sig_strength_5g')

    # @property
    # def mobile_number(self) -> str:
    #     """
    #         String: Mobile phone number associated to the istalled SIM card.
    #                 Private value, requires an authenticated session.
    #     """
    #     return self._try_get_private(data=self.get_connection(), key='mobile_number')

    @property
    def wan_ipv4_addr(self) -> str:
        """
            String: Current WAN IPv4 Address.
                    Note that this may not reflect your external IPv4,
                    this is due to most ISP's using NAT technology.
        """
        return self._try_get_private(data=self.get_connection(), key='wan_ipv4_addr')

    @property
    def wan_ipv6_addr(self) -> str:
        """
            String: Current WAN IPv6 Address.
                    Note that this may not reflect your external IPv6,
                    this is due to most ISP's using NAT technology.
        """
        return self._try_get_private(data=self.get_connection(), key='wan_ipv4_addr')

    def get_connection(self) -> dict:
        """
            Queries connection details from the ZTE modem API.

            Returns:
                Dictionary Containing connection details.
        """
        response = self._session.get_cmd_process(cmd=self.CONNECTION_CMDS)
        return self._cast_data_to_map(data=response, map=self.CONNECTION_VAL_MAP)

    def disconnect(self) -> bool:
        """ Disable the WAN connection. """
        return self._session.set_cmd_process(data={
            'isTest': False,
            'notCallback': True,
            'goformId': 'DISCONNECT_NETWORK',
        })

    def connect(self) -> bool:
        """ Enable the WAN connection. """
        return self._session.set_cmd_process(data={
            'isTest': False,
            'notCallback': True,
            'goformId': 'CONNECT_NETWORK',
        })
