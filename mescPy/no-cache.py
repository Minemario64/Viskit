
# save as serve_nocache.py
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import argparse
import os

class NoCacheHandler(SimpleHTTPRequestHandler):
    # Ensure HTTP/1.1 so Cache-Control is respected consistently
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        # Add strong no-cache headers to every response
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")   # for older proxies
        self.send_header("Expires", "0")
        # (Optional) prevent conditional 304 by removing Last-Modified
        # Note: SimpleHTTPRequestHandler sets Last-Modified in send_head;
        # if you still see 304s, override send_head to suppress it.
        super().end_headers()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=8000)
    parser.add_argument("--directory", "-d", default=".")
    args = parser.parse_args()

    # Serve the chosen directory
    print("GoGoGo")

    with ThreadingHTTPServer(("127.0.0.1", args.port), NoCacheHandler) as httpd:
        print(f"Serving {os.getcwd()} at http://127.0.0.1:{args.port} (no-cache)")
        httpd.serve_forever()

if __name__ == "__main__":
    main()