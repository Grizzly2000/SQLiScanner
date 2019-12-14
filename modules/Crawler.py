import settings
import logging


# Class which crawl URLs website recursively
# Init paramaters :
# target : target to scan recursively
# debug : enable debug mode
# threshold : crawl to a specific deep
class Crawler(object):
    def __init__(self, target, debug, threshold=settings.CRAWLER_THRESHOLD):
        self.__target = target
        self.__threshold = threshold
        self.__urls = []

        # Init logger
        self.__logger = logging.getLogger(__name__)
        self.__logger.disabled = not debug

    def crawl_target_forms(self):
        self.__logger.debug("Start crawler for {target}".format(target=self.__target))
        self.__logger.debug("Exit crawler for {target}".format(target=self.__target))
