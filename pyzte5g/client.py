from typing import Iterable
from .rest_framework import RESTCore
from .session import RESTSession
from .datausage import DATAUsage


class ZTE_Client():
    """ Client wrapper for the ZTE device REST API. """

    def __init__(self, url: str, password: str=None, session: RESTSession=None) -> None:
        self._public_session = False
        if session:
            self._session = session
            self._public_session = isinstance(self._session, RESTCore)
        elif password:
            self._session = RESTSession(url=url, password=password)
        else:
            self._session = RESTCore(url=url)
            self._public_session = True

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def datausage(self):
        """
            Access data usage metrics from the ZTE modem API.
            Public endpoint, does not require an authenticated session.
        """
        return DATAUsage(session=self.session)

    def get_cmd_process(self, cmd: Iterable[str]) -> dict:
        """
            Query ZTE modem state using provided parameters.

            Arguments:
                cmd:
                    Iterable of strings, used to query the device state.
            Returns:
                Dictionary Containing device values for queried parameters.
            Raises:
                TypeError: If passed "cmd" is not iterable.
        """
        return self.session.get_cmd_process(cmd=cmd)

    def set_cmd_process(self, data: dict) -> bool:
        """
            Alter ZTE modem state using provided parameters.

            Arguments:
                data:
                    Dictionary containing key value pairs of states to update.
            Returns:
                Boolean, True if request succeeded, False if it failed.
            Raises:
                TypeError: If passed "data" is not a dictionary object.
        """
        return self.session.set_cmd_process(data=data)
