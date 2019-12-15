#!/usr/bin/python

import argparse
import sys
import logging

import settings
from modules.SqliScanner import SqliScanner

logging.basicConfig(stream=sys.stdout, level=settings.DEBUG_LEVEL)
logger = logging.getLogger(__name__)


# This program check if a website is vulnerable to SQL injection (wiki: https://en.wikipedia.org/wiki/SQL_injection)
# It will crawl the targeted website and check if form parameters are vulnerable using SQLmap server API.
# Then, the result will be written in JSON file
# The project sqlmap is available here : https://github.com/sqlmapproject/sqlmap.

# This function will parse argument to run the main class.
# Not required parameters will be loaded in 'settings.py' as default parameters.
# Here is the list of each parameters :
# --url is a required parameter. The program will crawl this URL to check if form parameters are vulnerable to SQLi.
# --sqlmap-server is optional. Provide its own sqlmapapi server. (run sqlmap server : sqlmapapi.py -s)
# --debug is optional. Get debug output.
def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="target to scan. (ex: http://localhost:8000/)", required=True)
    parser.add_argument("-q", "--quiet", action='store_true', help="Do not use stdout.")
    args = parser.parse_args()

    # print help if no argument is provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Add slash at the end of thr provided url
    if '/' not in args.url[-1]:
        args.url += '/'

    if args.quiet:
        debug = False
    else:
        debug = settings.DEBUG

    # Create SqliScanner object
    SqliScanner(debug=debug, target=args.url)


# main function of the program
if __name__ == "__main__":
    main()
