import json
import re
import socket
import sys
import ssl

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443
RESPONCE_LENGTH = 500

def send_http_request(host, path="/", use_https=False):
    """Send an HTTP/HTTPS request and return the response"""
    port = DEFAULT_HTTPS_PORT if use_https else DEFAULT_HTTP_PORT
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    with socket.create_connection((host, port)) as sock:
        if use_https:
            sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)

        sock.sendall(request.encode())
        response = b""
        while chunk := sock.recv(4096):
            response += chunk

    return response.decode(errors="ignore")


def clean_html(html):
    """Removes <script>, <style>, and HTML tags, preserving meaningful text."""
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)  # Remove <script>...</script>
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)    # Remove <style>...</style>
    html = re.sub(r'<[^>]+>', '', html)  # Remove all remaining HTML tags
    html = re.sub(r'\s+', ' ', html).strip()  # Normalize spaces
    return html


def parse_http_response(response):
    """Parse HTTP headers and extract meaningful content."""
    headers, _, body = response.partition("\r\n\r\n")

    # Handle HTTP redirects (301/302)
    if "302 Found" in headers or "301 Moved Permanently" in headers:
        match = re.search(r"Location: (.+?)\r", headers)
        if match:
            return f"Redirected to: {match.group(1)}"

    # Check if the response is JSON
    if "application/json" in headers.lower():
        try:
            json_data = json.loads(body)
            return json.dumps(json_data, indent=4)  # Pretty print JSON
        except json.JSONDecodeError:
            return "Failed to decode JSON."

    # Otherwise, clean the HTML response
    return clean_html(body)  # Return cleaned-up content


def handle_url(url):
    """Process a URL request, handling HTTP and HTTPS"""
    match = re.match(r"(https?)://([^/]+)(/.*)?", url)
    if not match:
        print("Invalid URL format.")
        return

    protocol, host, path = match.groups()
    path = path or "/"
    use_https = (protocol == "https")  # Determine HTTPS usage

    response = send_http_request(host, path, use_https)
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
