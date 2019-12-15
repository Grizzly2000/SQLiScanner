# Debug
DEBUG_LEVEL = 20  # logging.DEBUG = 10 / logging.INFO = 20

# Sqlmap
SQLMAP_SERVER = "http://127.0.0.1:8775/"
SQLTASK_MAX_TIME_ELAPSED = 30
SQLTASK_GET_STATUS_INTERVAL = 5
SQLMAP_REPORT_OUTPUT_FILE = "vulns_report.txt"

# HTTP
CRAWLER_THRESHOLD = 30
REQUEST_TIMEOUT = 10

# Brute force files
BF_FILEPATH_USERS = "wordlists/users.txt"
BF_FILEPATH_PASSWORDS = "wordlists/passwords.txt"

# DVWA login settings
URL_LOGIN = "login.php"
URL_SUCCESS = "index.php"
COOKIES_EXTRA = {
    "security": "low"
}
COOKIE_SESSION_NAME = "PHPSESSID"
COOKIE_SESSION_REGEX = COOKIE_SESSION_NAME + "=(.*?);"
PARAM_FORM_USER_KEY = "username"
PARAM_FORM_PASSWORD_KEY = "password"
PARAM_FORM_CSRF_KEY = "user_token"
PARAM_FORM_LOGIN_KEY = "Login"
DEFAULT_INPUT_VALUE = "1"  # default value to set in form parameters
URLS_WHITELIST = ["logout.php", "setup.php", "login.php", "security.php"]
