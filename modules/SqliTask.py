import json
import requests
import time
import enum
import logging

import settings
from modules.URL import URL


# Class to enum sqlmap task states
class TaskStatus(enum.Enum):
    RUNNING = 0
    TERMINATED = 1
    ERROR = -1
    NOT_CREATED = -2


# Task created by Sqlmap using sqlmapapi.py
# The project sqlmap is available here : https://github.com/sqlmapproject/sqlmap.
class SqliTask(object):
    def __init__(self, debug: bool, url: URL, server: str = settings.SQLMAP_SERVER):
        self.__debug = debug  # debug mode
        self.__url = url  # Check SQL injection on this URL
        self.__server = server  # sqlmapapi server (<IP>:<PORT>)

        self.__status = TaskStatus.NOT_CREATED  # Status of the scan
        self.__result = ""  # result of sqlmapapi
        self.__time_begin = time.time()  # save datetime during class creation
        self.__time_elapsed = 0  # time elapsed during the SQLi scan

        # Init logger
        self.__logger = logging.getLogger(__name__)  # logger
        self.__logger.disabled = not self.__debug

        # Create new task on sqlmap server
        self.__task_id = json.loads(requests.get(self.__server + 'task/new').text)['taskid']
        self.run()

    # Start to scan url
    def start(self):
        headers = {'Content-Type': 'application/json'}

        # If form uses POST or GET request
        if self.__url.get_method() == "POST":
            target_options = {
                'url': self.__url.get_url(),
                'cookie': self.get_cookies_sqlmap(),
                'data': self.__url.get_concat_parameters()
            }
        elif self.__url.get_method() == "GET":
            # Craft URL with GET parameters
            url_get = self.__url.get_url() + "?" + self.__url.get_concat_parameters()

            target_options = {
                'url': url_get,
                'cookie': self.get_cookies_sqlmap()
            }
        else:
            return

        self.__logger.info(target_options)
        # Start task through Sqlmap API
        url = self.__server + 'scan/' + self.__task_id + '/start'
        json.loads(requests.post(url, data=json.dumps(target_options), headers=headers).text)

    # Stop task
    def stop(self):
        requests.get(self.__server + 'scan/' + self.__task_id + '/stop')
        requests.get(self.__server + 'scan/' + self.__task_id + '/kill')
        requests.get(self.__server + 'task/' + self.__task_id + '/delete')

    # Get cookies as string for sqlmap
    def get_cookies_sqlmap(self):
        cookies_sqlmap = ""
        cookies_dict = self.__url.get_cookies()
        for key in cookies_dict:
            cookies_sqlmap += key + "=" + cookies_dict[key] + ";"
        return cookies_sqlmap

    # Get status of a Sqlmap task
    def get_task_status(self):
        status = json.loads(requests.get(self.__server + 'scan/' + self.__task_id + '/status').text)['status']
        if status == 'running':
            self.__status = TaskStatus.RUNNING
        elif status == 'terminated':
            self.__status = TaskStatus.TERMINATED
        else:
            self.__status = TaskStatus.ERROR
        return

    # Get sqlmap result for this task
    def get_result_from_sqlmap(self):
        self.__result = json.loads(requests.get(self.__server + 'scan/' + self.__task_id + '/data').text)['data']

    # Get result of the class
    def get_result(self):
        return self.__result

    # Start the task previously created (during init)
    # Check status/time_spent
    # Get result if vulnerable
    def run(self):
        # Start scan
        self.start()
        # SQLTASK_MAX_TIME can be changed in 'settings.py'
        while settings.SQLTASK_MAX_TIME_ELAPSED > self.__time_elapsed:
            self.__time_elapsed = time.time() - self.__time_begin  # update time elapsed

            # Check status
            self.get_task_status()
            if self.__status == TaskStatus.RUNNING:
                time.sleep(settings.SQLTASK_GET_STATUS_INTERVAL)
            else:
                break

        # Check status if task has been correctly finished
        if self.__status == TaskStatus.TERMINATED:
            self.get_result_from_sqlmap()

        # Stop task on sqlmap server
        self.stop()
