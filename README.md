# SQLiScanner
Small program to find SQL injection vulnerabilities on a specific website. 

This program will crawl recursively every forms on the specified target and test each GET/POST parameters.


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
Run Sqlmap scanner in quiet mode on "http://localhost:8000"
```
python sql_scanner.py --url http://localhost:8000
```

Run Sqlmap scanner in debug mode on "http://localhost:8000"
```
python sql_scanner.py -u http://localhost:8000 -d
```

## Basic Help
```
usage: sql_scanner.py [-h] -u URL [-s SQLMAP_SERVER] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     target to scan. (ex: http://localhost:8000/)
  -s SQLMAP_SERVER, --sqlmap-server SQLMAP_SERVER
                        Sqlmap server API. (default: http://127.0.0.1:8775/)
  -d, --debug           Get debug output.
```



## Settings in settings.py

```
# Debug - Set Debug level if option '-d' have been specified : logging.DEBUG = 10 / logging.INFO = 20
DEBUG_LEVEL = 20 

# Sqlmap - server location
SQLMAP_SERVER = "http://127.0.0.1:8775/"
# Sqlmap - time to spend on each scan
SQLTASK_MAX_TIME_ELAPSED = 30
# Sqlmap - time to spend between each 'status' task request.
SQLTASK_GET_STATUS_INTERVAL = 5
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