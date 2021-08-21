from typing import Literal
from cachetools import cached, LRUCache, TTLCache
from urllib.parse import urlparse, urlunparse, urlunsplit, urlencode
from requests import Timeout
from threading import Lock
import requests, time


class RESTCore():
    """ Provides a basic framework to integrate with the ZTE Modem REST API. """

    GET_PROCESS_CACHE = TTLCache(maxsize=512, ttl=1)
    GET_PROCESS_LOCK = Lock()
    GET_PROCESS_ENDPOINT = 'goform/goform_get_cmd_process'
    SET_PROCESS_ENDPOINT = 'goform/goform_set_cmd_process'

    def __init__(self, url: str, timeout: int=10, retries: int=5) -> None:
        self._url = urlparse(url)
        if self._url.path != '/':
            url = urlunsplit(self._url[0:2] + ('/',) + self._url[3:5])
            self._url = urlparse(url)
        self._baseurl = urlunparse(self._url)
        self._timeout = timeout
        self._retries = retries
        self._headers = {
            'Referer': f'{self.baseurl}index.html',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': f'{self._url.scheme}://{self._url.hostname}',
        }

    @property
    def is_authenticated(self) -> bool:
        return False

    @property
    def baseurl(self) -> str:
        return self._baseurl

    @baseurl.setter
    def baseurl(self, value):
        self._baseurl = value
        self._url = urlparse(self._baseurl)
        self.headers['Origin'] = f'{self._url.scheme}://{self._url.hostname}'

    @property
    def timeout(self) -> str:
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    @property
    def retries(self) -> str:
        return self._retries

    @retries.setter
    def retries(self, value):
        self._retries = value

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    @cached(cache=LRUCache(maxsize=32))
    def _build_cmd_url(self, path: str, query: str='') -> str:
        """
            Build URL for use in REST requests to the modem API.

            Arguments:
                path:
                    String pointing to REST endpoint.
                query:
                    URL encoded string containing query parameters.
            Returns:
                Formatted URL string.
        """
        return urlunsplit(
            self._url[0:2] + (path, (query or self._url.query), '')
        )

    def _method_request_get(self):
        return requests.get

    def _method_request_post(self):
        return requests.post

    def _make_request(self, url: str, method: Literal['GET', 'POST']='GET', data: dict={}, remain_retries: int=0) -> dict:
        """
            Execute REST request to ZTE modem API.

            Arguments:
                url:
                    URL string pointing to REST endpoint.
                method:
                    Request method to use, either "GET" or "POST".
                data:
                    If method is "POST" this is the data packet that will be sent in the API request.
                remain_retries:
                    Integer specifying number of tries before failing on timeout.
            Returns:
                Dictionary Containing device values on "GET" and success or failure on "POST".
            Raises:
                TypeError:
                    If "url" is not a string.
                    OR "method" is not either "GET" or "POST".
                    OR "remain_retries" is not an integer.
        """

        if not isinstance(url, str):
            raise TypeError(f'"url" object must be passed as a string, not {type(url)}!')
        if method not in ['GET', 'POST']:
            raise TypeError(f'{method} is not a valid option, must be either "GET" or "POST"!')
        if not isinstance(remain_retries, int):
            raise TypeError(f'"remain_retries" object must be passed as an integer, not {type(url)}!')

        response = {}
        req_method = getattr(self, f'_method_request_{method.lower()}')()
        try:
            api_request = req_method(
                url=url,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
            )
            response = api_request.json()
        except Timeout as e:
            if remain_retries and remain_retries <= 1:
                raise e
            elif not remain_retries:
                remain_retries = self.retries
            else:
                remain_retries -= 1
        except Exception as e:
            raise e
        if remain_retries and remain_retries >= 1:
            response = self._make_request(url=url, method=method, data=data, remain_retries=remain_retries)
        return response

    @cached(cache=GET_PROCESS_CACHE, lock=GET_PROCESS_LOCK)
    def get_cmd_process(self, cmd: tuple[str]) -> dict:
        """
            Query ZTE modem state using provided parameters.

            Arguments:
                cmd:
                    Tuple of strings, used to query the device state.
            Returns:
                Dictionary Containing device values for queried parameters.
            Raises:
                TypeError: If passed "cmd" is not tuple.
        """

        if not isinstance(cmd, tuple):
            raise TypeError(f'"cmd" object must be tuple, not {type(cmd)}!')
        query = urlencode(
            dict(
                isTest=False,
                cmd=','.join(cmd),
                multi_data=1,
                _=round(time.time() * 1000),
            )
        )
        return self._make_request(
            url=self._build_cmd_url(path=self.GET_PROCESS_ENDPOINT, query=query),
            method='GET'
        )

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

        if not isinstance(data, dict):
            raise TypeError(f'"data" object must be a dictionary, not {type(data)}!')

        # Prevent ZTE modem queries while attempting to update state
        result = {}
        with self.GET_PROCESS_LOCK:
            result = self._make_request(
                url=self._build_cmd_url(path=self.SET_PROCESS_ENDPOINT),
                method='POST',
                data=data,
            )

            # Clear cached state data
            self.GET_PROCESS_CACHE.clear()
        return result.get('result') in ['0', 'success']
