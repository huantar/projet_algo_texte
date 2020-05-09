import os
import re, string
from bs4 import BeautifulSoup
from progress.bar import Bar
from model.distancePage import *
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
        bar = Bar('Importation des données : ', max=(len(repertoireFichiers)))
        for nomFichier in repertoireFichiers:
            bar.next()
            cheminFichier = repertoire + "/" + nomFichier
            fichier = open(cheminFichier,"rb")
            contenu = BeautifulSoup(fichier.read(), "html.parser").get_text().lower()
            #on remplace par des espace lescaracteres de separation (dates, ...)
            contenu = re.sub('\/|\-', " ", contenu)
            #on supprime les ponctuation et texte inutile
            # contenu = re.sub('\W', "", contenu)
            contenu = re.sub('\'|\`|\=|\"|\[|\]|\+|\.|\(|\)|\_|\,|\;|\:|\&|\!|\?|[a-z]+\@[a-z]+|https?[a-z]*|[0-9]*[a-z]*\=[0-9]*', "", contenu)
            # contenu = contenu.decode('utf-8','ignore').encode("utf-8")
            contenu = ' '.join(contenu.split())
            self.index.append([nomFichier,contenu, 0])
            fichier.close()
        bar.finish()

    #Parcour l'index et calcule la distance de hamming de 2 voisins
    #Si la distance de hamming est trop petite on le met dans une liste a part
    def distance_pages (self):
        #on initialise une liste vide pou stocker les pages trop similaires
        list_same = []
        #Compteur page trop similaires
        cmpt = 0
        # on definit la valeur max pour hamming qu'on accepte
        # En francais un mot fait 5 lettres en moyenne,
        # donc pour comparer les ~20 premiers mots on fait un max de 120
        maxh = 120
        #notre bar de progression
        bar = Bar('Analyse des pages :', max=(len(self.index)))
        for i in range(0,len(self.index)):
            bar.next()
            for j in range(i+1,len(self.index)):
                if (dist_hamming(self.index[i][0], self.index[j][0]) < 6) and (self.index[i][2] < 3) and (self.index[j][2] < 3):
                    if (dist_hamming(self.index[i][1], self.index[j][1]) < maxh):
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

    # Supprime les pages trop similaires et n'en garde qu'une
    #créer une liste des pages trop similaires
    def clean_index(self):
        print("Avant suppression on avait : " + str(len(self.index)) + " pages dans l'index")
        for page in self.list_same :
                self.index.remove(page)
        print("Aprés  suppression on a : " + str(len(self.index)) + " pages dans l'index")

    def find_word(self, word):
        #print(self.index)
        word_same=[]
        #si on cherche un chiffre alors on ne fait pas hamming
        if word.isdigit():
            for page in self.index :
                txt = page[1]
                for mot in txt :
                    if word == mot:
                        word_same.append(mot)
        #Sinon il s'agit d'un mot avec des faute potentiel donc on fait hamming
        else:
            for page in self.index :
                txt = page[1]
                wt = len(word)
                for mot in txt :
                    if dist_hamming(mot,word) < wt/2 and wt-1 <= len(mot)  <= wt+1 :
                        word_same.append(mot)
        #print("voici la liste des mots trouver : " + str(self.word_same))
        return word_same
