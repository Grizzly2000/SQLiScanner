import settings


# URL object to store form parameters and result of sqlmapapi
class URL(object):
    def __init__(self, debug: bool, url: str, method: str, parameters: list):
        self.__debug = debug            # debug mode
        self.__url = url                # url which contains the form
        self.__method = method          # HTTP method (GET/POST)
        self.__parameters = parameters  # Form parameters

        self.__result = ""              # result of sqlmapapi
        self.__is_vulnerable = False    # is vulnerable?

    # Get url
    def get_url(self):
        return self.__url

    # Get method
    def get_method(self):
        return self.__method

    # Get parameters
    def get_parameters(self):
        return self.__parameters

    # Set sqlmap result
    def set_result(self, result: str):
        self.__result = result

    # Set is_vulnerable
    def set_is_vulnerable(self, is_vulnerable: bool):
        self.__is_vulnerable = is_vulnerable
