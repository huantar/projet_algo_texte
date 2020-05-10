from model.calculScore import *
import time
from model.distancePage import *

class Index_reverse :
    """ Répertorie les mots de l'index selon les pages où ils se trouvent et leur occurence dans ces pages.
        Cette classe à pour paramètres :
        - reverse (dictionnaire de mots avec les pages correspondantes)
        """

     # Création du reverse dans le constructeur (on récupere le nombre d'url chargée de l'index avec len())
    def __init__(self,index):
        self.reverse = {}
        # On parcours l'index page par page pour génerer le reverse
        for url, contenu in index.items():
            # On transforme le contenu des pages en tableau de mots
            contenu[0] = contenu[0].split()
            mots = []
            # On enléve les doublons de la page et on les range dans le tableau mots avec extend
            mots.extend(list(dict.fromkeys(contenu[0])))
            # On va remplir le reverse avec les mots et les urls des pages de l'index
            for k in range(len(mots)):
                # On verifie si le mot est deja dans le reverse
                if bool(self.reverse.get(mots[k])):
                    self.reverse[mots[k]].append(url)
                else:
                    self.reverse[mots[k]]=[url]

    # Function qui return la liste des mots simialires d'une requete dans word_same
    def find_word(self, requete):
        word_same=[]
        dictionnaireMots= list(self.reverse.keys())
        requete = list(dict.fromkeys(requete))
        # On enléve les doublons et mots similaires de la requete
        for mot in requete :
            for motSim in requete :
                #si on cherche un chiffre alors on ne fait pas hamming
                if motSim.isdigit():
                    word_same.append(motSim)
                    requete.remove(motSim)
                else :
                    if dist_hamming(mot,motSim) < 3 and len(motSim)-1 <= len(mot)  <= len(motSim)+1 :
                        word_same.append(motSim)
                        requete.remove(motSim)
        # On cherche les mots similaires de la requete dans le dictionnaire
        for mot in dictionnaireMots :
            for motReq in requete :
                #si on cherche un chiffre alors on ne fait pas hamming
                if motReq.isdigit():
                    word_same.append(motReq)
                else :
                    if dist_hamming(mot,motReq) < 3 and len(motReq)-1 <= len(mot)  <= len(motReq)+1 :
                        word_same.append(mot)
        return list(dict.fromkeys(word_same))


    # Prend en paramètre une requète et l'index pour renvoyer les 10 meilleurs pages correspondantes
    def recherche(self, requete, d):
        # On recupere une liste de mots de la requete
        requete = requete.split()
        mProches = []
        start = time.time()
        #On recherche les mots proches
        mProches = self.find_word(requete)
        print("temps prit pour le findword:" + str((time.time()-start)/60) + " min \n")

        # reverseContenu contient la liste des pages ou notre mot apparait avec leur contenu 
        reverseContenu=[]
        # On cherche les mots de la requete dans l'index inverse
        for i in range(len(mProches)):
            if bool(self.reverse.get(mProches[i])):
                #on évite de mettre 2 fois la même page pour le calcul
                reverseContenu.extend(self.reverse[mProches[i]])
        # On supprime les eventuels doublons
        reverseContenu = list(dict.fromkeys(reverseContenu))
        # On remplace les urls par le contenu des pages
        for url in reverseContenu :
            if bool(d.index.get(url)):
                reverseContenu[reverseContenu.index(url)] =[url,  d.index[url][0]]

        start = time.time()
        #On créer le tableau des scores avec leurs urls triées
        if len(reverseContenu) > 0:
            score=calculScore25(requete,reverseContenu)
        print("temps prit pour score:" + str((time.time()-start)/60) + " min \n")

        bestPages=[]
        if not(reverseContenu):
            return bestPages
        else:
            for j in range(len(score)):
                bestPages.append(score[j][1])

        return bestPages
