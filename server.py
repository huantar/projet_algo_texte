from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import re
import shutil
from model.loadIndex import *
from model.Index_reverse import *

class Serv(BaseHTTPRequestHandler):

    # on initialise le serveur en creant un index
    repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web150"
    # repertoire="C:\\Users\\mathi\\OneDrive\\Bureau\\pages_web2"
    data = Data(repertoire)

    start = time.time()
    index_inverse = Index_reverse(data.index)
    # print(index_inverse.reverse[0])
    print("temps prit pour le reverse  :" + str((time.time()-start)/60) + " min \n")

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
                #On récupère la recherche de l'utilisateur
                motRechercher = self.path[9::]
                motRechercher = motRechercher.replace("+", " ")
                print("Le mot recherché est : \"", motRechercher, "\"")

                meilleur = self.index_inverse.recherche(motRechercher, self.data)
                print ("Il y a", len(meilleur), "pages pour cette recherche")

                #On copie le fichier modele Bbis pour lui ajouter les résulats
                shutil.copy("View/Bbis.html", "View/B.html")

                #On ouvre le fichier où l'on va afficher les pages
                file = open("View/B.html","a")
                #On initialise la variable que l'on va insérer dans le fichier B
                message='<h2>Recherche : ' + motRechercher + '</h2>'
                #Si le tableau ne contient aucune page, alors il n'y a pas de résultat
                if len(meilleur)==0:
                    message = message + '<h4>Aucune page ne correspond a votre recherche</h4>'
                else:
                    #Si il y a des résultats, alors on va concaténer les 10 premiers  à la variable message
                    if len(meilleur) <= 10 :
                        for j in meilleur:
                            message = message + '<div class="grid col-5 mt-2 p-2"> <h2><a href="'+ j + '">' + j + '</h2> </div>'
                    else:
                        for j in range(10):
                            message = message + '<div class="grid col-5 mt-2 p-2"> <h2><a href="'+ meilleur[j] + '">' + meilleur[j] + '</h2> </div>'

                message = message + '</div></div></body></html>'
                #On écrit la variable message à la fin du fichier B
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
