from urllib.parse import unquote_plus

from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

    <title>Computer Graphics Club Forum</title>
</head>
<body style="display: grid; grid-template-rows: auto 1fr auto; min-height: 100vh">
    <nav class="blue">
        <div class="nav-wrapper">
            <div class="container">
                <span class="brand-logo">Computer Graphics Club Forum</span>
                <ul class="right">
                    <li>
                        <button class="btn orange darken-2"
                                onclick="alert('Thanks for buying pizza! Your card has been charged.')">
                            Buy Pizza For Next Meeting
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container">
        <div id="messages">
            {MESSAGES}
        </div>
    </main>

    <footer class="container" style="margin-bottom: 20px">
        <form action="/" method="post" autocomplete="off">
            <div class="input-field">
                <input type="text" name="message" id="message">
                <label for="message">Message</label>
            </div>
            <input type="submit" class="btn blue right" value="Send">
        </form>
        
        <button class="btn blue right"
                style="margin-right: 20px"
                onclick="document.getElementById('message')
                                 .setAttribute('value', Math.ceil(Math.random() * 10)
                                 .toString());
                         M.updateTextFields();">
            Generate Random Number
        </button>
    </footer>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
</body>
</html>
'''

messages = [
    '<b>Lesley</b>: Meetings are at 6pm.',
    '<b>Tiffany</b>: I love computer graphics!',
    '<b>Lici</b>: Me too!',
]


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        messages_string = ''.join('<p>{}</p>'.format(message) for message in messages)
        response = PAGE_HTML.replace('{MESSAGES}', messages_string)

        self.wfile.write(bytes(response, 'utf8'))

    def do_POST(self):
        bytes_to_read = int(self.headers.get('Content-Length'))
        raw = self.rfile.read(bytes_to_read).decode('UTF8')
        message = unquote_plus(raw.lstrip('message='))

        # For the demo, this will show that this platform "does not allow XSS". This isn't actually secure though, as
        # there are many ways around this.
        message = message.replace('<script>', '').replace('</script>', '')

        messages.append('<b>Josh</b>: ' + message)
        self.do_GET()


def main():
    print('Starting server...')

    httpd = HTTPServer(('127.0.0.1', 8000), RequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
