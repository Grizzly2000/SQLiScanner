import settings
import logging

from modules.Crawler import Crawler
from modules.BruteForce import BruteForce


# Class which scan a spefific website recursively to find SQL injection in form parameter
class SqliScanner(object):
    def __init__(self, debug: bool, target: str, server: str = settings.SQLMAP_SERVER):
        self.__debug = debug                        # debug mode
        self.__target = target                      # target to scan
        self.__server = server                      # sqlmapapi server (<IP>:<PORT>)

        # Init logger
        self.__logger = logging.getLogger(__name__) # logger
        self.__logger.disabled = not self.__debug

    # get target to scan
    def get_target(self):
        return self.__target

    # run sql injection scan
    # Brute force DVWA authentication
    # if we are authenticated,
    #   The crawler will gather every URLs with form parameters
    #   For each form, test parameters with sqlmap
    def run(self):
        self.__logger.info("Start scan for {target}".format(target=self.__target))

        # Brute force DVWA authentication
        dvwa_login = BruteForce(self.__debug, self.__target + settings.URL_LOGIN)
        dvwa_login.run()

        # if authentication succeed
        if dvwa_login.get_is_authenticated():
            # Crawl forms on the target
            crawler = Crawler(debug=self.__debug, target=self.__target, cookies=dvwa_login.get_cookies())
            crawler.run()

        self.__logger.info("End scan for {target}".format(target=self.__target))
