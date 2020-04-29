import os
import re
from bs4 import BeautifulSoup
from progress.bar import Bar
from distancePage import *
import time

class Data :

    index = []
    list_same = []

    # On initialise la classe avec un index qu'on "nettoie"
    def __init__(self, repertoire):
        start = time.time()
        self.loadIndex(repertoire)
        print("on a un index de taille :" + str(len(self.index)))
        self.distance_pages()
        self.clean_index()
        print("temps prit pour l'initialisation :" + str((time.time()-start)/60) + " min \n")

    #charge données dans index
    def loadIndex(self, repertoire):
        repertoireFichiers = os.listdir(repertoire)
        for nomFichier in repertoireFichiers:
            cheminFichier=repertoire+"/"+nomFichier
            fichier=open(cheminFichier,"rb")
            contenu=BeautifulSoup(fichier.read(), "html.parser").get_text()
            self.index.append([nomFichier,contenu, 0])
            fichier.close()


    #Parcour l'index et calcule la distance de hamming de 2 voisins
    #Si la distance de hamming est trop petite on le met dans une liste a part
    def distance_pages (self):
        #on initialise une liste vide pou stocker les pages trop similaires
        list_same = []
        #Compteur page trop similaires
        cmpt = 0
        # on definit la valeur max pour hamming qu'on accepte
        # En francais un mot fait 5 lettres en moyenne,
        # donc pour comparer les ~20 premiers mots on fait un max de 100
        maxh = 100
        #notre bar de progression
        bar = Bar('Analyse des pages', max=(len(self.index)))
        for i in range(0,len(self.index)):
            bar.next()
            for j in range(i+1,len(self.index)):
                if (dist_hamming(self.index[i][0], self.index[j][0]) < 15) and (self.index[i][2] < 3) and (self.index[j][2] < 3):
                    if (dist_hamming(self.index[i][1], self.index[j][1]) < maxh+5):
                        cmpt += 1
                        # Si c'est la premiere fois qu'on a cette page, on la met dans les page similaires
                        if self.index[j][2] == 0 :
                            self.list_same.append(self.index[j])
                        #on marque les page qui ressemblent a la notre
                        self.index[j][2] += 1
        bar.finish()

    #Compte les pages non-simialires (pour test suppression)
    def show_no_same(self):
        cmpt = 0
        for i in range(len(self.index)):
            if self.index[i][2] == 0:
                cmpt += 1
        print(cmpt)

    # Supprime les pages trop similaires et n'en garde qu'une
    #créer une liste des pages trop similaires
    def clean_index(self):
        print("Avant suppression on a : " + str(len(self.index)) + " pages dans index")
        for page in self.list_same :
                self.index.remove(page)
        print("Aprés  suppression on a : " + str(len(self.index)) + " pages dans index")
