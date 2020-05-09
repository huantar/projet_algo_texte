from model.calculScore import *

class Index_reverse :
    """ Répertorie les mots de l'index selon les pages où ils se trouvent et leur occurence dans ces pages.
        Cette classe à pour paramètres :
        - mots dictionnaire de mots
        - reverse (qui contient l'occurences des mots par pages)
        """

     #constructeur de la classe index reserve
    def __init__(self,index):
        self.reverse={}
        #on enleve les doublons du contenu de chaque page avec split et on met la liste renvoyé à mots
        for i in range(len(index)):
            index[i][1]=index[i][1].split()
            mots=[]
            mots.extend(list(dict.fromkeys(index[i][1])))
            for k in range(len(mots)):
                if bool(self.reverse.get(mots[k])):
                    self.reverse[mots[k]].append(index[i][0])
                else:
                    self.reverse[mots[k]]=[index[i][0]]


    # Ancien constructeur de la classe index reserve
    # def __init__(self,index):
    #     self.mots=[]
    #     self.reverse=[]
    #     #on enleve les doublons du contenu de chaque page avec split et on met la liste renvoyé à mots
    #     for i in range(len(index)):
    #         index[i][1]=index[i][1].split()
    #         self.mots.extend(list(dict.fromkeys(index[i][1])))
    #     #on s'assure d'enlever les mots qui reviennent dans plusieurs pages pour construire le disctionnaire
    #     self.mots=list(dict.fromkeys(self.mots))
    #     #on définit reverse de la forme [[mots1,[url1,pages]....[urlN,page]],...,[motsN[url1,pages]....[urlN,page]]]
    #     for i in range(len(self.mots)):
    #         self.reverse.insert(self.mots[i],[self.mots[i],[]])
    #         for j in range(len(index)):
    #             if self.mots[i] in index[j][1] and index[j][2] == 0:
    #                 #on ajoute [url,page] à reverse
    #                 self.reverse[i][1].append([index[j][0],index[j][1]])
    #                 #supprimer le mots de la page
    #                 index[j][2] = 1

    #prend en paramètre une requète et renvoie les 10 meilleurs pages correspondantes
    def recherche(self, requete, d):
        requete=requete.split()
        #On recherche les mots proches
        mProches = []
        for i in range(len(requete)):
            mProches = mProches + d.find_word(requete[i])
        #liste de page (0:url et 1:contenue) ou notre mot apparait
        reverseContenu=[]
        #on cherche les mots de la requete dans l'index inverse
        for i in range(len(mProches)):
            if bool(self.reverse.get(mProches[i])):
                #on évite de mettre 2 fois la même page pour le calcul
                reverseContenu.extend(self.reverse[mProches[i]])
                reverseContenu = list(dict.fromkeys(reverseContenu))
        #on remplace les url par le contenu des pages
        for url in reverseContenu:
            for page in d.index :
                if url == page[0] :
                    reverseContenu[reverseContenu.index(url)] = [page[0] ,page[1]]
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
