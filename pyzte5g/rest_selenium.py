from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from .rest_framework import RESTCore
import time, json


class RESTSelenium(RESTCore):
    """
    Uses Selenium to integrate with the ZTE Modem REST API.

    This implementation is a hack to get arround issues when attempting to use the requests module to set command states.
    """

    def __init__(self, url: str, timeout: int=10, retries: int=5, webdriver: RemoteWebDriver=Firefox, options=None, executable_path: str='geckodriver') -> None:
        super().__init__(url=url, timeout=timeout, retries=retries)
        self._password = None
        self._webdriver = webdriver
        self._executable_path = executable_path
        if self._webdriver == Firefox and not options:
            self._options = Options()
            self._options.headless = True
        else:
            self._options = options

    @property
    def webdriver(self) -> RemoteWebDriver:
        return self._webdriver

    @webdriver.setter
    def webdriver(self, value: RemoteWebDriver):
        self._webdriver = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @property
    def executable_path(self) -> str:
        return self._executable_path

    @executable_path.setter
    def executable_path(self, value: str):
        self._executable_path = value

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

        url = self._build_cmd_url(path=self.SET_PROCESS_ENDPOINT)
        driver = self.webdriver(options=self.options, executable_path=self.executable_path)
        driver.get(self.baseurl)
        driver.execute_script(f"""
        var zte_modem_response;
        $.ajax({{
            type: "POST",
            url: "{url}",
            cache: false,
            async: false,
            data: {{
                isTest: false,
                notCallback: true,
                goformId: "LOGIN",
                password: "{self._password}"
            }},
            error: function(data) {{
                zte_modem_response = jQuery.parseJSON(data);
            }},
            success: function(e) {{
                zte_modem_response = jQuery.parseJSON(e);
            }}
        }});
        """)
        time.sleep(3)
        data['AD'] = driver.execute_script(f"""
        var zte_modem_response;
        $.ajax({{
            type: "GET",
            url: "{self._build_cmd_url(path=self.GET_PROCESS_ENDPOINT, query='isTest=false&cmd=RD')}",
            cache: false,
            async: false,
            error: function(e) {{
                zte_modem_response = jQuery.parseJSON(e);
            }},
            success: function(e) {{
                zte_modem_response = jQuery.parseJSON(e);
            }}
        }});
        var a = hex_md5(rd0 + rd1), u = zte_modem_response.RD;
        zte_modem_response = hex_md5(a + u)
        return zte_modem_response;
        """)
        result = driver.execute_script(f"""
        var zte_modem_response;
        $.ajax({{
            type: "POST",
            url: "{url}",
            cache: false,
            async: false,
            data: {json.dumps(data)},
            error: function(data) {{
                zte_modem_response = jQuery.parseJSON(data);
            }},
            success: function(e) {{
                zte_modem_response = jQuery.parseJSON(e);
            }}
        }});
        return zte_modem_response;
        """)
        driver.close()
        return result in ['0', 'success']
