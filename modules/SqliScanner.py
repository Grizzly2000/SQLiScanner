import settings
import logging


# Main class
class SqliScanner(object):
    def __init__(self, target, debug, server=settings.SQLMAP_SERVER):
        self.__target = target
        self.__server = server

        # Init logger
        self.__logger = logging.getLogger(__name__)
        self.__logger.disabled = not debug

    def get_target(self):
        return self.__target

    def run(self):
        self.__logger.debug("Start scan for {target}".format(target=self.__target))
        self.__logger.debug("End scan for {target}".format(target=self.__target))
