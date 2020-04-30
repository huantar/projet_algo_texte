from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import re
from model.loadIndex import *

class Serv(BaseHTTPRequestHandler):

    # on initialise le serveur en creant un index
    repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web500"
    data = Data(repertoire)

    print(data.index[1][0])

    #function qui gere les requetes GET
    def do_GET(self):
        #Redirection des pages selon l'url
        if self.path == '/':
            self.path = "/view/A.html"
        if "?" in self.path:
            pattern = re.compile("(/\?search=?\+*$)")
            if pattern.match(self.path):
                self.path= "/view/A.html"
            else:
                self.path = "/view/B.html"

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
