import argparse
import sys


# This function will parse argument to run the main class.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="target to scan. (ex: http://localhost:8000/)", required=True)
    parser.add_argument("-s", "--sqlmap-server",
                        help="Sqlmap server API. (default: 127.0.0.1:8775)")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)


# main function of the program
if __name__ == "__main__":
    main()
