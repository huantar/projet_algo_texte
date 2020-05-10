import os
import re, string
from bs4 import BeautifulSoup
from progress.bar import Bar
from model.distancePage import *
import time

class Data :

    index = {}
    list_same = []

    # On initialise la classe avec un index qu'on "nettoie"
    def __init__(self, repertoire):
        start = time.time()
        self.loadIndex(repertoire)
        print("on a un index de taille :" + str(len(self.index)))
        # self.distance_pages()
        # self.clean_index()
        print("temps prit pour l'initialisation :" + str((time.time()-start)/60) + " min \n")

    #charge données dans index
    def loadIndex(self, repertoire):
        repertoireFichiers = os.listdir(repertoire)
        bar = Bar('Importation des données : ', max=(len(repertoireFichiers)))
        for nomFichier in repertoireFichiers:
            bar.next()
            cheminFichier = repertoire + "/" + nomFichier
            fichier = open(cheminFichier,"rb")
            contenu = BeautifulSoup(fichier.read().decode('utf-8', 'ignore'), "html.parser").get_text().lower()

            #on remplace par des espace lescaracteres de separation (dates, ...)
            contenu = re.sub('\/|\-', " ", contenu)
            #on supprime les ponctuation et texte inutile
            # contenu = re.sub('\W', "", contenu)
            contenu = re.sub('\'|\`|\=|\"|\[|\]|\+|\.|\(|\)|\_|\,|\;|\:|\&|\!|\?|[a-z]+\@[a-z]+|https?[a-z]*|[0-9]*[a-z]*\=[0-9]*', "", contenu)
            # contenu = contenu.decode('utf-8','ignore').encode("utf-8")
            contenu = ' '.join(contenu.split())
            self.index[nomFichier] = [contenu, 0]
            fichier.close()
        bar.finish()

    #Parcour l'index et calcule la distance de hamming de 2 voisins
    #Si la distance de hamming est trop petite on le met dans une liste a part
    def distance_pages (self):
        #on initialise une liste vide pou stocker les pages trop similaires
        list_same = []
        #Compteur page trop similaires
        cmpt = 0
        #on definit la hamming max pour les 40 premiers mots (5*40)
        maxh = 200
        #notre bar de progression
        bar = Bar('Analyse des pages :', max=(len(self.index)))
        tabPage = list(self.index.keys())
        for i in range(0,len(tabPage)):
            bar.next()
            for j in range(i+1,len(tabPage)):
                if (dist_hamming(tabPage[i], tabPage[j]) < 6) and (self.index[tabPage[i]][1] < 3) and (self.index[tabPage[j]][1] < 3):
                    if (dist_hamming(self.index[tabPage[i]][0], self.index[tabPage[j]][0]) < maxh):
                        cmpt += 1
                        # Si c'est la premiere fois qu'on a cette page, on la met dans les page similaires
                        if self.index[tabPage[j]][1] == 0 :
                            self.list_same.append(tabPage[j])
                        #on marque les page qui ressemblent a la notre
                        self.index[tabPage[j]][1] += 1
        bar.finish()

    # Supprime les pages trop similaires et n'en garde qu'une
    #créer une liste des pages trop similaires
    def clean_index(self):
        print("Avant suppression on avait : " + str(len(self.index)) + " pages dans l'index")
        for url in self.list_same :
            self.index.pop(url)
        print("Aprés  suppression on a : " + str(len(self.index)) + " pages dans l'index")
