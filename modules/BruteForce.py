import requests
import re

import settings


# Brute force authentication
class BruteForce(object):
    def __init__(self, debug: bool, url_login: str, target_credential: str = None,
                 file_users: str = settings.BF_FILEPATH_USERS, file_passwords: str = settings.BF_FILEPATH_PASSWORDS):
        self.__debug = debug
        self.__url_login = url_login
        self.__target_credential = target_credential
        self.__cookies = None
        self.__request_login = None

        # if known creds has not been set, set users/passwords files
        if not self.__target_credential:
            self.__file_users = file_users
            self.__file_passwords = file_passwords

    def test_login_url(self):
        try:
            self.__request_login = requests.get(self.__url_login, timeout=settings.REQUEST_TIMEOUT)
        except ConnectionRefusedError:
            print("Error - Login page unreachable !")
            exit(0)

    def dvwa_set_cookies(self):
        cookie_session_name = "PHPSESSID"
        cookie_session_regexp = cookie_session_name + "=(.*?);"
        cookie_session_value = re.match(cookie_session_regexp, self.__request_login.headers["set-cookie"]).group(1)

        # Set cookies
        self.__cookies = {cookie_session_name: cookie_session_value,
                          "security": "low"}

    def dvwa_brute_force(self):
        pass

    def run(self):
        self.test_login_url()
        self.dvwa_set_cookies()
        self.dvwa_brute_force()
