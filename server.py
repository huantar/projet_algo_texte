from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
import os
import re
import shutil
from model.loadIndex import *
from model.Index_reverse import *
from sys import platform

class Serv(BaseHTTPRequestHandler):
    """
    La classe serveur met en place notre serveur. Ses parametres de classe sont :
        - data qui est une instance de la classe Data
        - index_inverse qui est une instance de la classe Index_reverse
    """
    # on initialise le serveur en creant un index
    repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web150"
    # repertoire="C:\\Users\\mathi\\OneDrive\\Bureau\\pages_web"
    data = Data(repertoire)

    start = time.time()
    index_inverse = Index_reverse(data.index)
    print("temps prit pour le reverse  :" + str((time.time()-start)/60) + " min \n")

    # Lorsque le serveur est pret on joue une notification sonore, adaptée pour windows et linux
    if platform == "win32":
        import winsound
        winsound.PlaySound("son", winsound.SND_FILENAME)
    if platform == "linux" or platform == "linux2":
        os.system("aplay son.wav&")

    #function qui gere les requetes GET
    def do_GET(self):
        #Redirection des pages selon l'url
        # S'il demande l'index on renvoit la page A
        if self.path == '/':
            self.path = "/view/A.html"
        # Sinon il s'agit d'une requete
        if "?" in self.path:
            # Si la requete est vide on renvoit la page A
            pattern = re.compile("(/\?search=?\+*$)")
            if pattern.match(self.path):
                self.path= "/view/A.html"
            # Sinon on renvoit la page B
            else:
                #On récupère la recherche de l'utilisateur
                motRechercher = self.path[9::]
                motRechercher = motRechercher.replace('+', " ")
                print("Le mot recherché est : \"", motRechercher, "\"")

                start = time.time()
                # On lance la recherche des pages correspondante a la recherche
                meilleur = self.index_inverse.recherche(motRechercher, self.data)
                print ("Il y a", len(meilleur), "pages pour cette recherche")
                print("temps prit pour la recherche  :" + str((time.time()-start)/60) + " min \n")

                #On copie le fichier modele Bbis pour lui ajouter les résulats
                shutil.copy("View/Bbis.html", "View/B.html")

                #On ouvre le fichier où l'on va afficher les pages
                file = open("View/B.html","a")
                #On initialise la variable que l'on va insérer dans le fichier B
                message = '<div class="row"><h2 class="">Recherche : ' + motRechercher + '</h2></div>'
                message = message + '<div class="row"><h2 class="">Pages correspondantes : ' + str(len(meilleur)) + '</h2></div>'
                #Si le tableau ne contient aucune page, alors il n'y a pas de résultat
                if len(meilleur)==0:
                    message = message + '<h4>Aucune page ne correspond a votre recherche</h4>'
                else:
                    message = message + '<ul class="list-group list-group-flush">'
                    #Si il y a des résultats, alors on va concaténer les 10 premiers  à la variable message
                    if len(meilleur) <= 10 :
                        for j in meilleur:
                            message = message + '<li class="col-5 mt-2 p-2 col-12 list-group-item"> <h4><a href="'+ j + '">' + j + '</a></h4> </li>'
                    else:
                        for j in range(10):
                            message = message + '<li class="col-5 mt-2 p-2 col-12 list-group-item"> <h4><a href="'+ meilleur[j] + '">' + meilleur[j] + '</a></h4> </li>'
                        message = message + '</ul>'
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

# on initilise le serveur sur un port et on lui de reseter active en permanence
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
