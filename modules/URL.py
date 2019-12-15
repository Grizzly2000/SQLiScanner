import settings


# URL object to store form parameters and result of sqlmapapi
class URL(object):
    def __init__(self, debug: bool, url: str, cookies: dict, method: str, parameters: list):
        self.__debug = debug            # debug mode
        self.__url = url                # url which contains the form
        self.__cookies = cookies        # cookies for authentication
        self.__method = method          # HTTP method (GET/POST)
        self.__parameters = parameters  # Form parameters

    # Get url
    def get_url(self):
        return self.__url

    # Get cookies
    def get_cookies(self):
        return self.__cookies

    # Get method
    def get_method(self):
        return self.__method

    # Get parameters
    def get_parameters(self):
        return self.__parameters

    # Get concat parameters
    def get_concat_parameters(self):
        concat_params = ""
        for parameter in self.get_parameters():
            concat_params += "&" + parameter + "=" + settings.DEFAULT_INPUT_VALUE
        return concat_params

