import settings
import logging
import json
from datetime import datetime

from modules.Crawler import Crawler
from modules.BruteForce import BruteForce
from modules.SqliTask import SqliTask


# Class which scan a spefific website recursively to find SQL injection in form parameter
class SqliScanner(object):
    def __init__(self, debug: bool, target: str, server: str = settings.SQLMAP_SERVER):
        self.__debug = debug                        # debug mode
        self.__target = target                      # target to scan
        self.__server = server                      # sqlmapapi server (<IP>:<PORT>)

        self.__urls_vuln = []                       # store list of vulnerable urls provided by sqlmap
        # Init logger
        self.__logger = logging.getLogger(__name__) # logger
        self.__logger.disabled = not self.__debug

        # Run
        self.run()

    # get target to scan
    def get_target(self):
        return self.__target

    # Write report to a file in JSON format
    def write_json_report(self):
        # current timestamp
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        filename = settings.SQLMAP_REPORT_OUTPUT_DIR + str(timestamp) + "_" + settings.SQLMAP_REPORT_OUTPUT_FILE
        with open(filename, "w+") as fp_report:
            for vuln in self.__urls_vuln:
                fp_report.write(json.dumps(vuln))

    # run sql injection scan
    # Brute force DVWA authentication
    # if we are authenticated,
    #   The crawler will gather every URLs with form parameters
    #   For each form, test parameters with sqlmap
    def run(self):
        self.__logger.info("Start scan for {target}".format(target=self.__target))

        # Brute force DVWA authentication
        dvwa_login = BruteForce(self.__debug, self.__target + settings.URL_LOGIN)

        # if authentication succeed, crawl forms on the target
        if dvwa_login.get_is_authenticated():
            # Crawl forms of the target
            crawler = Crawler(debug=self.__debug, target=self.__target, cookies=dvwa_login.get_cookies())
            # Start SQL scan for each URLs
            for url in crawler.get_urls_form():
                sqlitask = SqliTask(self.__debug, url)
                # If vulnerabilities have been found
                result = sqlitask.get_result()
                if len(result) > 0:
                    self.__urls_vuln.append(sqlitask.get_result())

            # Write report in file (path location can be changed in 'settings.py')
            self.write_json_report()

        self.__logger.info("End scan for {target}".format(target=self.__target))
