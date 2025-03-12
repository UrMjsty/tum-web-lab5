import re
import socket
import sys

DEFAULT_HTTP_PORT = 80

def send_http_request(host, path="/"):
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, DEFAULT_HTTP_PORT))
        s.sendall(request.encode())
        response = b""
        while chunk := s.recv(4096):
            response += chunk

    return response.decode(errors="ignore")


def parse_http_response(response):
    headers, _, body = response.partition("\r\n\r\n")
    if "302 Found" in headers or "301 Moved Permanently" in headers:
        match = re.search(r"Location: (.+?)\r", headers)
        if match:
            return f"Redirected to: {match.group(1)}"
    return re.sub(r"<.*?>", "", body)  # Strip HTML tags


def handle_url(url):
    match = re.match(r"https?://([^/]+)(/.*)?", url)
    if not match:
        print("Invalid URL format.")
        return

    host, path = match.groups()
    path = path or "/"
    response = send_http_request(host, path)
    print(parse_http_response(response))


def show_help():
    print("Usage:")
    print("  go2web -u <URL>         # Fetch a URL")
    print("  go2web -s <search-term> # Search for a term")
    print("  go2web -h               # Show help")


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    option = sys.argv[1]
    if option == "-h":
        show_help()
    elif option == "-u" and len(sys.argv) > 2:
        handle_url(sys.argv[2])
    elif option == "-s" and len(sys.argv) > 2:
        print("Placeholder for search")
    else:
        print("Invalid command. Use -h for help.")
if __name__ == "__main__":
        main()