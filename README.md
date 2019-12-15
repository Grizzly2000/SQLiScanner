# SQLiScanner
Small program to find SQL injection vulnerabilities on a specific website. 

This program will crawl recursively every forms on the specified target and test each GET/POST parameters.

## Structure of the project

```
├── modules                                     # Contains classes of the project
│   ├── BruteForce.py                           # Class to brute force login/password (tested on DVWA)
│   ├── Crawler.py                              # Class to Crawl URLs website recursively to gather form informations
│   ├── SqliScanner.py                          # Class to run Sqlmap tasks and write a report in JSON format
│   ├── SqliTask.py                             # Class to handle Sqlmap tasks
│   └── URL.py                                  # Class to store informations of potentially vulnerable URL
├── README.md                                   # This file
├── reports                                     # Store reports here (according to the 'settings.py' file)
│   └── 1576389014.339253_vulns_report.txt      # Sample of report with DVWA
├── requirements.txt                            # List of dependencies
├── settings.py                                 # Settings of the application
├── sql_scanner.py                              # Main program to launch SQL injection scan on specific target
├── TODO                                        # Just in case ...
└── wordlists                                   # Wordlists directory
    ├── passwords.txt                           # Contains well-known passwords
    └── users.txt                               # Contains well-known users
``` 

## Installation

Install python3

Install Sqlmap (already installed on Kali Linux) : https://github.com/sqlmapproject/sqlmap & http://sqlmap.org/

Install the following python3 dependencies with pip ('root' permissions could be necessary):
```
pip install -r requirements.txt
```

## Set up
Run the sqlmap API server with the following command line
```
sqlmapapi -s
```

## Test
To test this program, you can use DVWA project : https://github.com/ethicalhack3r/DVWA

A docker container is available ('root' permission requiered)
```
docker run --rm -it -p 80:80 vulnerables/web-dvwa
```
Then, you need to connect with the following credentials 'admin/password'.

Go to "http://localhost:8000/setup.php" to click on the button "Create / Reset Database"

## Examples
Run Sqlmap scanner on "http://localhost:8000"
```
python sql_scanner.py --url http://localhost:8000
```
or
```
chmod u+x sql_scanner.py
./sql_scanner.py --url http://localhost:8000
```
Quiet mode is available
```
./sql_scanner.py --url http://localhost:8000 -q
```
## Basic Help
```
./sql_scanner.py --help
usage: sql_scanner.py [-h] -u URL [-q]

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  target to scan. (ex: http://localhost:8000/)
  -q, --quiet        Do not use stdout.
```

## Settings in settings.py

```
# Debug - Set Debug information
DEBUG = True
# Debug - Set Debug level if option has been enabled : logging.DEBUG = 10 / logging.INFO = 20
DEBUG_LEVEL = 20 

# Sqlmap - server location
SQLMAP_SERVER = "http://127.0.0.1:8775/"
# Sqlmap - time to spend on each scan
SQLTASK_MAX_TIME_ELAPSED = 30
# Sqlmap - time to spend between each 'status' task request.
SQLTASK_GET_STATUS_INTERVAL = 5
# Sqlmap - output directory to write the report in JSON format
SQLMAP_REPORT_OUTPUT_DIR = "reports/"
# Sqlmap - output file to write the report in JSON format
SQLMAP_REPORT_OUTPUT_FILE = "vulns_report.txt"

# HTTP - Threshold to crawl the targeted website
CRAWLER_THRESHOLD = 30
# HTTP - set HTTP request timeout
REQUEST_TIMEOUT = 10

# URL - default value for each GET/POST parameters
DEFAULT_INPUT_VALUE = "1" 

# Brute force - file with users
BF_FILEPATH_USERS = "wordlists/users.txt"
# Brute force - file with passwords
BF_FILEPATH_PASSWORDS = "wordlists/passwords.txt"

# DVWA - login page
URL_LOGIN = "login.php"
# DVWA - login redirection succeed page
URL_SUCCESS = "index.php"
# DVWA - additional cookies
COOKIES_EXTRA = {
    "security": "low"
}
# DVWA - session cookie name
COOKIE_SESSION_NAME = "PHPSESSID"
# DVWA - regexp to get the session cookie value
COOKIE_SESSION_REGEX = COOKIE_SESSION_NAME + "=(.*?);"
# DVWA - login form, value of attribute username
PARAM_FORM_USER_KEY = "username"
# DVWA - login form, value of attribute password
PARAM_FORM_PASSWORD_KEY = "password"
# DVWA - login form, value of attribute token CSRF (useless - invalidation problem)
PARAM_FORM_CSRF_KEY = "user_token"
# DVWA - login form, value of attribute Login 
PARAM_FORM_LOGIN_KEY = "Login"
# DVWA - Avoid these urls during the scan.
URLS_WHITELIST = ["logout.php", "setup.php", "login.php", "security.php"]
```