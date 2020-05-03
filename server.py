from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import re
import shutil
from model.loadIndex import *
from model.Index_reverse import *

class Serv(BaseHTTPRequestHandler):

    # on initialise le serveur en creant un index
    repertoire="C:\\Users\\mathi\\OneDrive\\Bureau\\pages_web2"
    data = Data(repertoire)
    index_inverse = Index_reverse(data.index)
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
                motRechercher = self.path[9::]
                print("Le mot recherché est : \"", motRechercher, "\"")
                meilleur = self.index_inverse.recherche(motRechercher)
                print ("Il y a", len(meilleur), "pages pour cette recherche")

                shutil.copy("View/Bbis.html", "View/B.html")

                file = open("View/B.html","a")
                message=""
                for j in meilleur:
                    message = message + '<div class="grid col-5 mt-2 p-2"> <h2><a href="'+ j + '">' + j + '</h2> </div>'

                message = message + '<button type="button" name="more" class="btn btn-primary mt-3 offset-2">Charger plus</button></div></div></body></html>'
                file.write(message)
                file.close()

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
