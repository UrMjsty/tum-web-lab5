import urllib.parse
import re
import time
import requests
from bs4 import BeautifulSoup
import sys
import json
import os


class URLBrowser:
    def __init__(self):
        self.cache = {}

    def fetch_url(self, url):
        """Fetch the content of the URL."""
        if url in self.cache:
            print(f"Using cached response for: {url}")
            return self.cache[url]
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.cache[url] = response.text
            if response.status_code == 429:
                print("Rate limit reached, waiting for a while...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                return self.fetch_url(url)  # Retry the request
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            sys.exit(1)

    def extract_search_results(self, html):
        """Extract the search result links from the DuckDuckGo HTML response."""
        soup = BeautifulSoup(html, "html.parser")
        search_results = []
        # Update this selector based on the current DuckDuckGo HTML structure
        results = soup.find_all("a", class_="result__a")
        for result in results:
            link = result.get('href')
            if link:
                search_results.append(link)
        return search_results

    def search(self, query):
        """Perform a search and display results."""
        if query in self.cache and time.time() - self.cache[query]['timestamp'] < 3600:  # Cache for 1 hour
            print("Using cached results...")
            return self.cache[query]['results']
        search_url = f"https://duckduckgo.com/html/?q={query}"
        try:
            response = self.fetch_url(search_url)
            search_results = self.extract_search_results(response)
            if not search_results:
                print("No search results found.")
            return search_results
        except Exception as e:
            print(f"Error fetching search results: {e}")
            return []

class Cache:
    def __init__(self, cache_filename="cache.json"):
        self.cache_filename = cache_filename
        self.cache_data = self.load_cache()

    def load_cache(self):
        """Load the cache from a file."""
        if os.path.exists(self.cache_filename):
            with open(self.cache_filename, 'r') as f:
                return json.load(f)
        return {}

    def save_cache(self):
        """Save the current cache to a file."""
        with open(self.cache_filename, 'w') as f:
            json.dump(self.cache_data, f)

    def get(self, key):
        """Get data from the cache."""
        return self.cache_data.get(key)

    def set(self, key, value):
        """Set data in the cache."""
        self.cache_data[key] = value
        self.save_cache()


def print_search_results(results):
    """Print the search results, cleaning up the URLs."""
    for idx, result in enumerate(results, start=1):
        # Parse the DuckDuckGo URL and extract the 'uddg' parameter value
        parsed_url = urllib.parse.urlparse(result)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if 'uddg' in query_params:
            actual_url = query_params['uddg'][0]  # Extract the URL from the 'uddg' parameter
            print(f"{idx}. {actual_url}")
        else:
            print(f"{idx}. {result}")  # Print the URL directly if no 'uddg' parameter is found


def handle_query(browser, cache, query):
    """Handle the search query, check cache, and show results."""
    cached_results = cache.get(query)
    if cached_results:
        print(f"Using cached results for: {query}")
        print_search_results(cached_results)
        return

    print(f"Searching for: {query}")
    search_results = browser.search(query)
    if search_results:
        cache.set(query, search_results)
        print_search_results(search_results)

def make_search(query):
    browser = URLBrowser()
    cache = Cache()

    handle_query(browser, cache, query)


def main():
    """Main function to run the program."""
    query = input("Enter search query: ")

    make_search(query)

if __name__ == "__main__":
    main()
