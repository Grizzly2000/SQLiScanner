import settings
import logging


# Class which crawl URLs website recursively
# Init paramaters :
# debug : enable debug mode
# target : target to scan recursively
# cookies : specify cookies cookies
# threshold : crawl to a specific deep
# urls : list of URL object
# self.__logger : class logger
class Crawler(object):
    def __init__(self, debug: bool, target: str, cookies: dict = None, threshold: int = settings.CRAWLER_THRESHOLD):
        self.__debug = debug
        self.__target = target
        self.__cookies = cookies
        self.__threshold = threshold
        self.__urls = []

        # Init logger
        if self.__debug:
            self.__logger = logging.getLogger(__name__)
            self.__logger.disabled = not debug

    # Find urls with parameters in form
    def crawl_target_forms(self):
        self.__logger.debug("Start crawler for {target}".format(target=self.__target))

        self.__logger.debug("Exit crawler for {target}".format(target=self.__target))
