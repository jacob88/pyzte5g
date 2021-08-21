from typing import Literal
from urllib.parse import urlencode
from .rest_framework import RESTCore
from .exceptions import AuthFailure
import requests, base64, hashlib


class RESTSession(RESTCore):
    """ Extends core framework to include request session management and authentication. """

    def __init__(self, url: str, password: str=None, timeout: int=10, retries: int=5) -> None:
        super().__init__(url=url, timeout=timeout, retries=retries)
        self._session = requests.Session()
        self._password = password and base64.b64encode(
            password.encode('utf-8')
        ).decode('utf-8')
        self.session.headers = self._headers
        if self._password and not self.is_authenticated:
            self._renew_auth()

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def headers(self) -> dict:
        return self.session.headers

    @headers.setter
    def headers(self, value: dict):
        self.session.headers = value

    @property
    def is_authenticated(self) -> bool:
        result = {}
        query = urlencode(
            dict(
                isTest=False,
                cmd='hardware_version',
                multi_data=1,
            )
        )
        req_method = self._method_request_get()
        try:
            api_request = req_method(
                url=self._build_cmd_url(path=self.GET_PROCESS_ENDPOINT, query=query),
                headers=self.headers,
                timeout=self.timeout,
            )
            result = api_request.json()
        except Exception:
            return False
        return bool(result.get('hardware_version'))

    def _method_request_get(self):
        return self.session.get

    def _method_request_post(self):
        return self.session.post

    def _renew_auth(self):
        with self.GET_PROCESS_LOCK:
            req_method = self._method_request_post()
            req_method(
                url=self._build_cmd_url(path=self.SET_PROCESS_ENDPOINT),
                timeout=self.timeout,
                data={
                    'isTest': False,
                    'goformId': 'LOGIN',
                    'password': self._password,
                },
            )

            # Clear cached state data
            self.GET_PROCESS_CACHE.clear()

            if not self.is_authenticated:
                raise AuthFailure('Session authentication failed, check password and retry.')
        return True

    def set_cmd_process(self, data: dict) -> bool:
        if isinstance(data, dict) and not data.get('AD'):
            ver_info = self.get_cmd_process(cmd=('Language', 'wa_inner_version','cr_version',))
            rd_key = self.get_cmd_process(cmd=('RD',))
            ver_md5 = hashlib.md5(f"{ver_info.get('wa_inner_version', '')}{ver_info.get('cr_version', '')}".encode('utf-8')).hexdigest()
            data['AD'] = hashlib.md5(f"{rd_key.get('RD', '')}{ver_md5}".encode('utf-8')).hexdigest()
        return super().set_cmd_process(data=data)

    def manage_auth(func=None):
        """ Decorator to manage the request session. """
        def auth_dec(self, **kwargs):
            if self._password and not self.is_authenticated:
                self._renew_auth()
            return func(self, **kwargs)
        return auth_dec

    @manage_auth
    def _make_request(self, url: str, method: Literal['GET', 'POST']='GET', data: dict={}, remain_retries: int=0) -> dict:
        result = super()._make_request(url=url, method=method, data=data, remain_retries=remain_retries)
        if not (result and self.is_authenticated):
            # Authed session has timed out, re-auth and try again
            self._renew_auth()
            result = super()._make_request(url=url, method=method, data=data, remain_retries=remain_retries)
        return result
