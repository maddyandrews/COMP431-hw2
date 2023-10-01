__author__ = "730393750"

import sys
import os


def checkRequestMethod(tokens: list[str]) -> bool:
    """Checks if an HTTP Request method token is valid and formatted correctly.
    Prints error statement and exits if token is invalid.

    Args: 
        tokens (list[str]): List of tokens found in HTTP request line.

    Returns: 
        bool: True if valid method token found, false otherwise.
    """
    if (len(tokens) < 1):
        return False

    method = tokens[0]

    if (method != "GET"):
        print("ERROR -- Invalid Method token.")
        return False

    return True


def checkAbsolutePath(tokens: list[str]) -> bool:
    """ 
    Checks if an HTTP Request absolute path token is valid and formatted correctly.
    Prints error statement and exits if token is invalid.

   Args: 
        tokens (list[str]): List of tokens found in HTTP request line.

    Returns: 
        bool: True if valid path token found, false otherwise.
    """
    if (len(tokens) < 2):
        print("ERROR -- Invalid Absolute-Path token.")
        return False

    path = tokens[1]

    if path.startswith("/") == False:
        print("ERROR -- Invalid Absolute-Path token.")
        return False

    for c in path:
        if (c.isalnum() or (c == ".") or (c == "_") or (c == "/")) == False:
            print("ERROR -- Invalid Absolute-Path token.")
            return False

    return True


def checkHTTPVersion(tokens: list[str]) -> bool:
    """
    Checks if an HTTP Request version token is valid and formatted correctly.
    Prints error statement and exits if token is invalid.

    Args: 
        tokens (list[str]): List of tokens found in HTTP request line.

    Returns: 
        bool: True if valid HTTP version token found, false otherwise.
    """
    if (len(tokens) < 3):
        print("ERROR -- Invalid Absolute-Path token.")
        return False

    http = tokens[2]

    if ((http.startswith("HTTP/") == False)
        or ((http[5].isnumeric() and http[6] == "." and http[7].isnumeric()) == False)
            or (len(http) > 8)):
        print("ERROR -- Invalid HTTP-Version token.")
        return False

    return True


def checkSpuriousTokens(tokens: list[str]) -> bool:
    """
    Checks if an HTTP Request contains spurious tokens following HTTP version token.
    Prints error statement and exits if additional token(s) found.

    Args: 
        tokens (list[str]): List of tokens found in HTTP request line.

    Returns: 
        bool: True if valid number of tokens found, false otherwise.
    """
    if len(tokens) != 3:
        print("ERROR -- Spurious token before CRLF.")
        return False
    return True


def main():
    """Main function."""

    for line in sys.stdin:
        print(line, end="")

        requestTokens: list[str] = line.split()

        if (checkRequestMethod(requestTokens) and checkAbsolutePath(requestTokens)
                and checkHTTPVersion(requestTokens) and checkSpuriousTokens(requestTokens)):

            print("Method = " + requestTokens[0] + "\nRequest-URL = " +
                  requestTokens[1] + "\nHTTP-Version = " + requestTokens[2])

            try:
                if (requestTokens[1].lower().endswith(".txt")
                    or requestTokens[1].lower().endswith(".htm")
                        or requestTokens[1].lower().endswith(".html")) == False:
                    print('501 Not Implemented: ' + requestTokens[1])
                elif os.path.isfile("." + requestTokens[1]) == False:
                    print('404 Not Found: ' + requestTokens[1])
                else:
                    f = open("." + requestTokens[1],
                             newline='\r\n').read().splitlines()
                    [print(line) for line in f]
            except Exception as e:
                print("ERROR: ", str(e))


if __name__ == "__main__":
    main()
