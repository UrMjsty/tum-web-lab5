go2web - Simple Web Client
Overview
go2web is a Python-based command-line tool designed to fetch and display content from web URLs using low-level socket programming. It supports both HTTP and HTTPS requests, follows redirects (up to a limit), and processes responses (HTML or JSON) to extract meaningful content. This project demonstrates fundamental concepts of network programming, HTTP protocol handling, and text processing.
Features

Fetch URL Content: Retrieves content from a specified URL using HTTP/HTTPS GET requests.
Redirect Handling: Automatically follows HTTP 301/302 redirects up to a limit of 10.
Content Processing:
Strips HTML tags, scripts, and styles to display clean text.
Pretty-prints JSON responses if the server returns JSON.


Low-Level Networking: Uses Python's socket and ssl libraries instead of high-level libraries like requests to illustrate how HTTP works under the hood.
Relative URL Support: Resolves relative redirect URLs (e.g., /page) to absolute URLs.

Requirements

Python 3.6 or higher (due to SSLContext usage).
No external dependencies; uses only Python standard libraries (socket, ssl, json, re, sys).

Installation

Clone or download the project to your local machine.
Ensure Python 3.6+ is installed.
Place the go2web.py script in your desired directory.
(Optional) Set up a virtual environment:python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate



Usage
Run the script from the command line with the following options:
python go2web.py [option]

Options

-u <URL>: Fetch content from the specified URL (e.g., https://httpbin.org/get).
Example: python go2web.py -u https://httpbin.org/redirect/5
Follows redirects and displays the final content (JSON or cleaned HTML).


-h: Show the help message with usage instructions.
Example: python go2web.py -h



Example Output
Fetching a URL with redirects:
$ python go2web.py -u https://httpbin.org/redirect/5
Requesting: https://httpbin.org/redirect/5
Headers received:
HTTP/1.1 302 Found
...
Location: /relative-redirect/4
...
Detected redirect to: /relative-redirect/4
Following redirect to: https://httpbin.org/relative-redirect/4
[...]
Final content:
{
    "args": {},
    "headers": {
        "Host": "httpbin.org",
        "Connection": "close"
    },
    "url": "https://httpbin.org/get"
}

Code Structure

Main Functions:

send_http_request(host, path, use_https): Sends an HTTP/HTTPS GET request using sockets.
clean_html(html): Strips HTML tags, scripts, and styles to extract readable text.
parse_http_response(response): Parses HTTP responses, handles redirects, and processes JSON or HTML.
resolve_redirect_url(current_url, redirect_path): Converts relative redirect URLs to absolute URLs.
handle_url(url, redirect_limit): Manages URL fetching and redirect following.
main(): Parses command-line arguments and routes to appropriate functions.


Key Features:

Uses SSLContext for secure HTTPS connections (modern alternative to deprecated ssl.wrap_socket).
Handles redirect loops with a limit to prevent infinite recursion.
Processes JSON responses with pretty-printing for readability.



Notes

This project is designed for educational purposes to demonstrate low-level HTTP communication and response parsing.
The RESPONCE_LENGTH constant is defined but unused; it may have been intended for limiting response size.
The url_browser module (for search functionality) is referenced but not implemented in this version.

License
This project is unlicensed and intended for educational use only.
