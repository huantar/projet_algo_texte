from model.calculScore import *

class Index_reverse :
    """ Répertorie les mots de l'index selon les pages où ils se trouvent et leur occurence dans ces pages.
        Cette classe à pour paramètres :
        - mots dictionnaire de mots
        - reverse (qui contient l'occurences des mots par pages)
        """

     #constructeur de la classe index reserve
    def __init__(self,index):
        self.reverse = {}
        #on enleve les doublons du contenu de chaque page avec split et on met la liste renvoyé à mots
        for url, contenu in index.items():
            contenu[0] = contenu[0].split()
            mots = []
            mots.extend(list(dict.fromkeys(contenu[0])))
            for k in range(len(mots)):
                if bool(self.reverse.get(mots[k])):
                    # print(url)
                    self.reverse[mots[k]].append(url)
                else:
                    self.reverse[mots[k]]=[url]

    #prend en paramètre une requète et renvoie les 10 meilleurs pages correspondantes
    def recherche(self, requete, d):
        requete = requete.split()
        #On recherche les mots proches
        mProches = []
        mProches = find_word(requete)
        #liste de page (0:url et 1:contenue) ou notre mot apparait
        reverseContenu=[]
        #on cherche les mots de la requete dans l'index inverse
        for i in range(len(mProches)):
            if bool(self.reverse.get(mProches[i])):
                #on évite de mettre 2 fois la même page pour le calcul
                reverseContenu.extend(self.reverse[mProches[i]])
        reverseContenu = list(dict.fromkeys(reverseContenu))
        #on remplace les url par le contenu des pages
        for url in reverseContenu :
            if bool(d.index.get(url)):
                reverseContenu[reverseContenu.index(url)] =[url,  d.index[url][0]]

        #tableau des scores avec leurs urls triées
        if len(reverseContenu) > 0:
            score=calculScore25(requete,reverseContenu)
        # print(score)
        bestPages=[]
        if not(reverseContenu):
            return bestPages
        else:
            for j in range(len(score)):
                bestPages.append(score[j][1])

        return bestPages
