import settings
import logging

from modules.Crawler import Crawler

# Class which scan a spefific website recursively to find SQL injection in form parameter
# Init paramaters :
# target : target to scan
# debug : enable debug mode
# server : sqlmapapi server
class SqliScanner(object):
    def __init__(self, target, debug, server=settings.SQLMAP_SERVER):
        self.__target = target
        self.__server = server
        self.__debug = debug

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
        crawler = Crawler(self.__target, self.__debug)
        crawler.crawl_target_forms()
        self.__logger.debug("End scan for {target}".format(target=self.__target))
