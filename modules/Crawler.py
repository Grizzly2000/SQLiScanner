import settings
import logging


# Class which crawl URLs website recursively
class Crawler(object):
    def __init__(self, debug: bool, target: str, cookies: dict = None, threshold: int = settings.CRAWLER_THRESHOLD):
        self.__debug = debug                        # debug mode
        self.__target = target                      # target to crawl recursively
        self.__cookies = cookies                    # cookies to provide
        self.__threshold = threshold                # crawl to a specific deep

        self.__urls = []                            # store URL objects here

        # Init logger
        self.__logger = logging.getLogger(__name__) # logger
        self.__logger.disabled = not debug

    # Find urls with parameters in form
    def run(self):
        self.__logger.info("Start crawler for {target}".format(target=self.__target))

        self.__logger.info("Exit crawler for {target}".format(target=self.__target))
