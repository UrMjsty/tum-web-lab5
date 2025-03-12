import sys

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

if __name__ == "__main__":
        main()