from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        print('Number detected:', self.path.strip('/'))

        self.send_header('Content-type', 'text/html')
        self.end_headers()


def main():
    print('Starting attacker server...')

    httpd = HTTPServer(('127.0.0.1', 8001), RequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
