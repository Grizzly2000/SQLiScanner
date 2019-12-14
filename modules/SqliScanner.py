import settings
import logging

from modules.Crawler import Crawler


# Class which scan a spefific website recursively to find SQL injection in form parameter
# Init paramaters :
# debug : enable debug mode
# target : target to scan
# server : sqlmapapi server
class SqliScanner(object):
    def __init__(self, debug: bool, target: str, server: str = settings.SQLMAP_SERVER):
        self.__debug = debug
        self.__target = target
        self.__server = server

        # Init logger
        self.__logger = logging.getLogger(__name__)
        self.__logger.disabled = not self.__debug

    # get target
    def get_target(self):
        return self.__target

    # run sql injection scan
    # the crawler gather every webpage till a specific threshold with form parameters
    # each website forms parameters will be tested by sqlmapapi
    def run(self):
        self.__logger.debug("Start scan for {target}".format(target=self.__target))
        crawler = Crawler(debug=self.__debug, target=self.__target)
        crawler.crawl_target_forms()
        self.__logger.debug("End scan for {target}".format(target=self.__target))
