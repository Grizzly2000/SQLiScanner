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