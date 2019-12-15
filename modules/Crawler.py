import requests
from bs4 import BeautifulSoup
import logging

import settings

from modules.URL import URL


# Class which crawl URLs website recursively
class Crawler(object):
    def __init__(self, debug: bool, target: str, cookies: dict = None, threshold: int = settings.CRAWLER_THRESHOLD):
        self.__debug = debug  # debug mode
        self.__target = target  # target to crawl recursively
        self.__cookies = cookies  # cookies for authentication
        self.__threshold = threshold  # crawl to a specific deep

        self.__urls_form = []  # store URLs with form
        self.__urls_visited = []  # store visited urls
        self.__urls_to_visit = [target]  # store urls to crawl like a queue (entry point : target url)

        # Init logger
        self.__logger = logging.getLogger(__name__)  # logger
        self.__logger.disabled = not debug

        # Run
        self.run()

    # Get first url in current queue
    def get_first_url_to_visit(self):
        return self.__urls_to_visit[0]

    # Remove first element of __urls_to_visit
    def pop_first_url_to_visit(self):
        self.__urls_to_visit = self.__urls_to_visit[1:]

    # Get newt url(s) to crawl
    def get_next_urls_to_visit(self):
        if len(self.__urls_to_visit) == 1:  # No new urls
            self.__urls_to_visit = []
        else:  # New url(s) to crawl
            self.pop_first_url_to_visit()

    # Crawl current URL to find new urls or form.
    def crawl_urls_form(self):

        # Get HTML content (parsed with BeautifulSoup) of the first url to visit
        try:
            url = self.get_first_url_to_visit()
            self.__logger.info("Current crawled url : {url}".format(url=url))
            response = requests.get(url, cookies=self.__cookies, timeout=settings.REQUEST_TIMEOUT)
            bs = BeautifulSoup(response.text, "html.parser")
        except ConnectionRefusedError:
            print("Error - Webpage unreachable !")
            return

        # Append current url to visited url.
        self.__urls_visited.append(url)

        # Search form
        html_tag_form = bs.find('form')
        if html_tag_form:
            # Get list of parameters
            parameters = []
            # Get 'name' parameter
            html_tags_input_name = html_tag_form.find_all('input',{'name':True})
            for html_tag_input_name in html_tags_input_name:
                parameters.append(html_tag_input_name["name"])

            # Check 'action' in form.
            html_tag_form_action = html_tag_form.find("action")
            if html_tag_form_action:
                if html_tag_form["action"].startswith(self.__target):
                    html_url_form_action = html_tag_form["action"]
                elif html_tag_form["action"] == "#":
                    html_url_form_action = url
                else:
                    html_url_form_action = self.__target + html_tag_form["action"]
            else:
                html_url_form_action = url
            # Create and append new URL objects to __urls_form
            url_form = URL(debug=self.__debug, url=html_url_form_action, cookies=self.__cookies,
                           method=html_tag_form["method"].upper(), parameters=parameters)
            self.__urls_form.append(url_form)

        # Search new urls
        html_tags_a = bs.find_all('a', href=True)
        if html_tags_a:
            for html_tag_a in html_tags_a:
                html_href = html_tag_a["href"]
                if html_href is None:
                    continue

                # Check new_url format
                if html_href.startswith(self.__target):
                    new_url = html_href
                elif html_href.startswith("http") or "../" in html_href or html_href in settings.URLS_WHITELIST:
                    continue
                else:
                    new_url = self.__target + html_href

                # Add new URL to crawl
                if new_url not in self.__urls_visited and new_url not in self.__urls_to_visit:
                    self.__urls_to_visit.append(new_url)
                    self.__logger.info("New url has been added : {url}".format(url=new_url))

        # remove the visited url
        self.get_next_urls_to_visit()

    # Get URLs with forms
    def get_urls_form(self):
        return self.__urls_form

    # Find urls form with parameters
    def run(self):
        self.__logger.info("Start crawler for {target}".format(target=self.__target))

        # Crawl target
        crawl_condition = (x for x in range(0, self.__threshold) if len(self.__urls_to_visit))
        for i in crawl_condition:
            self.__logger.info("HTTP request number {number}".format(number=i))
            # find urls or form
            self.crawl_urls_form()

        self.__logger.info("Exit crawler for {target}".format(target=self.__target))
