import settings
from modules.URL import URL


# Task created by Sqlmap using sqlmapapi.py
# The project sqlmap is available here : https://github.com/sqlmapproject/sqlmap.
class SqliTask(object):
    def __init__(self, debug: bool, url: URL, id_task: int, server: str = settings.SQLMAP_SERVER):
        self.__debug = debug  # debug mode
        self.__url = url  # Check SQL injection on this URL
        self.__id_task = id_task  # sqlmap task id
        self.__server = server  # sqlmapapi server (<IP>:<PORT>)

        self.__finished = False  # If Sqlmap task has been finished


