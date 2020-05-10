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
        self.distance_pages()
        self.clean_index()
        print("temps prit pour l'initialisation :" + str((time.time()-start)/60) + " min \n")

    # Charge les données dans l'index
    def loadIndex(self, repertoire):
        repertoireFichiers = os.listdir(repertoire)
        bar = Bar('Importation des données : ', max=(len(repertoireFichiers)))
        for nomFichier in repertoireFichiers:
            bar.next()
            cheminFichier = repertoire + "/" + nomFichier
            fichier = open(cheminFichier,"rb")
            # on supprime le html
            contenu = BeautifulSoup(fichier.read().decode('utf-8', 'ignore'), "html.parser").get_text().lower()
            # on remplace par des espace les caracteres de separation (dates, ...)
            contenu = re.sub('\/|\-', " ", contenu)
            # on supprime les ponctuation et texte inutile
            contenu = re.sub('\'|\`|\=|\"|\[|\]|\+|\.|\(|\)|\_|\,|\;|\:|\&|\!|\?|[a-z]+\@[a-z]+|https?[a-z]*|[0-9]*[a-z]*\=[0-9]*', "", contenu)
            contenu = ' '.join(contenu.split())
            self.index[nomFichier] = [contenu, 0]
            fichier.close()
        bar.finish()

    # Parcours l'index et calcule la distance de hamming de 2 pages
    # Si la distance de hamming est trop petite on le met dans une liste a part
    def distance_pages (self):
        # on initialise une liste vide pou stocker les pages trop similaires
        list_same = []
        # On definit la hamming max pour les 40 premiers mots
        # Un mot francais a entre 5-6 lettres donc on fait (5*40)=200
        maxh = 200
        bar = Bar('Analyse des pages :', max=(len(self.index)))
        # On recupere uniquement les urls des pages
        tabPage = list(self.index.keys())
        # On parcours les urls 1 fois
        for i in range(0,len(tabPage)):
            bar.next()
            # On compare chaque urls avec les urls qui suivent
            for j in range(i+1,len(tabPage)):
                # On verifie la distance de hamming entre les urls (plus court qu'une page )
                # On permet egalment qu'une page soit similaire a 3 pages pour detecter plus de pages similaires
                if (dist_hamming(tabPage[i], tabPage[j]) < 6) and (self.index[tabPage[i]][1] < 3) and (self.index[tabPage[j]][1] < 3):
                    # Si les urls sontr trop proche alors on verifie le contenu des pages
                    if (dist_hamming(self.index[tabPage[i]][0], self.index[tabPage[j]][0]) < maxh):
                        # Si c'est la premiere fois qu'on a cette page, on la met dans les page similaires
                        if self.index[tabPage[j]][1] == 0 :
                            self.list_same.append(tabPage[j])
                        #on marque les page qui ressemblent a la notre
                        self.index[tabPage[j]][1] += 1
        bar.finish()

    # Supprime les pages trop similaires pour n'en avoir qu'une
    def clean_index(self):
        print("Avant suppression on avait : " + str(len(self.index)) + " pages dans l'index")
        for url in self.list_same :
            self.index.pop(url)
        print("Aprés  suppression on a : " + str(len(self.index)) + " pages dans l'index")

    # Function qui retrouve dans l'index les mots similaires a un mot clé
    def find_single_word(self, word):
        # On initialise notre tableau de retour
        single_word_same=[]
        #si on cherche un chiffre alors on ne fait pas hamming
        if word.isdigit():
            for page in self.index :
                txt = page[1]
                for mot in txt :
                    if word == mot:
                        word_same.append(mot)
        #Sinon, on fait hamming
        else:
            # On parcours l'index
            for page in self.index :
                txt = page[1]
                wt = len(word)
                # Pour chaque page on parcours le contenu
                for mot in txt :
                    # Et on verifie avec hamming la distance entre les deux mots,
                    # De plus on accepte les mots qui sont proche a plus ou moins une lettre
                    if dist_hamming(mot,word) < wt/2 and wt-1 <= len(mot)  <= wt+1 :
                        word_same.append(mot)
        return single_word_same
