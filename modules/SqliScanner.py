import settings


# Main class
class SqliScanner:
    def __init__(self, target, server=settings.SQLMAP_SERVER):
        self.__target = target
        self.__server = server
