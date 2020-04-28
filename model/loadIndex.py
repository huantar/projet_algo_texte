import os
import re
from bs4 import BeautifulSoup
from progress.bar import Bar
from distancePage import *
#Pour utiliser la barre de progression il faut d'abord faire "pip install progress"

#supprime balise html, \t et \n
def cleanhtml(raw_html):
    raw_html = raw_html.replace("\\t",'')
    raw_html = raw_html.replace("\\n ",'')
    raw_html = raw_html.replace("; ",' ')
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    # cleantext = cleantext.replace("\\t",'')
    # cleantext = cleantext.replace("\\n ",'')
    # cleantext = cleantext.replace("; ",' ')
    return cleantext

class Data :

    index = []
    list_same = []

    #charge données dans index
    def __init__(self, repertoire):
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
        #notre bar de progression
        bar = Bar('Analyse des pages', max=(len(self.index)))

        for i in range(0,len(self.index)):
        # for i in range(0,50):
            bar.next()
            for j in range(i+1,len(self.index)):
                if (dist_hamming(self.index[i][0], self.index[j][0]) < 20) and (self.index[i][2] < 3) and (self.index[j][2] < 3):
                    #print("Pour " + str(i) + " et " + str(i+1) + " on a distance de H : " + str(dist_hamming(index[i][1], index[i+1][1])))
                    if (dist_hamming(self.index[i][1], self.index[j][1]) < 10):
                        cmpt += 1
                        self.list_same.append(self.index[i])
                        self.list_same.append(self.index[j])
                        #on marque les page qui ressemblent a la notre
                        self.index[j][2] += 1
                        self.index[i][2] += 1

        bar.finish()
        print("On supprime : " + str(cmpt) + " page similaires")

    def show_no_same(self):
        cmpt = 0
        for i in range(len(self.index)):
            if self.index[i][2] == 0:
                cmpt += 1
        print(cmpt)
