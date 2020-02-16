from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):

    # This class handles all the get requests made to the page.
    def do_GET(self):
        if self.path == '/':  # Home-page
            self.path = '/pages/home.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        if self.path == '/about':  # About-page
            self.path = '/pages/about.html'
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


httpd = HTTPServer(('localhost', 8080), Serv) # The server is running on localhost:8080.
print('The server is up and running!')

httpd.serve_forever()
