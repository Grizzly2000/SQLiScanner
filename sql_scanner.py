import argparse
import sys

import settings
from modules.SqliScanner import SqliScanner


# This program check if a website is vulnerable to SQL injection (wiki: https://en.wikipedia.org/wiki/SQL_injection)
# It will crawl the targeted website and check if form parameters are vulnerable using SQLmap server API.
# Then, the result will be written in JSON file
# The project sqlmap is available here : https://github.com/sqlmapproject/sqlmap.

# This function will parse argument to run the main class.
# Not required parameters will be loaded in 'settings.py' as default parameters.
# Here is the list of each parameters :
# --url is a required parameter. The program will crawl this URL to check if form parameters are vulnerable to SQLi.
# --sqlmap-server is optional. Provide its own sqlmapapi server. (run sqlmap server : sqlmapapi.py -s)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="target to scan. (ex: http://localhost:8000/)", required=True)
    parser.add_argument("-s", "--sqlmap-server",
                        help="Sqlmap server API. (default: {default})".format(default=settings.SQLMAP_SERVER))
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    sqlscan = SqliScanner(args.url)


# main function of the program
if __name__ == "__main__":
    main()
