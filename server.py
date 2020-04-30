from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/' :
            self.path = "/view/A.html"

        if "?" in self.path:
            self.path = "/view/B.html"
            # try:
            #     file_to_open = open(self.path[1:], 'rb+').read()
            #     self.send_response(200)
            # except:
            #     file_to_open = "File not found"
            #     self.send_response(404)
            # self.end_headers()
            # self.wfile.write(file_to_open)
            # # self.wfile.write(file_to_open)
        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return


        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)



httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
