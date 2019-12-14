import settings


# Main class
class SqliScanner(object):
    def __init__(self, target, server=settings.SQLMAP_SERVER):
        self.__target = target
        self.__server = server

    def get_target(self):
        return self.__target
