from model.calculScore import *

class Index_reverse :
    """ Répertorie les mots de l'index selon les pages où ils se trouvent et leur occurence dans ces pages.
        Cette classe à pour paramètres :
        - mots dictionnaire de mots
        - reverse (qui contient l'occurences des mots par pages)
        """

    #constructeur de la classe index reserve
    def __init__(self,index):
        # reverse est de la formze : [mots,[url1,url2,...],mot2,[url1,..url]...]
        self.reverse=[]
        #on enleve les doublons du contenu de chaque page avec split et on met la liste renvoyé à mots
        for i in range(len(index)):
            index[i][1]=index[i][1].split()
            mots=[]
            mots.extend(list(dict.fromkeys(index[i][1])))
            for k in range(len(mots)):
                if mots[k] in self.reverse:
                    self.reverse[self.reverse.index(mots[k])+1].append(index[i][0])
                else:
                    self.reverse.append(mots[k])
                    self.reverse.append([index[i][0]])

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
        print ("Les mots proches sont : ", mProches)
        #list d'url auquelle le mot apparait
        reverseContenu=[]
        #on cherche les mots de la requete dans l'index inverse
        for i in range(len(requete)):
            if requete[i] in self.reverse:
                #on retrouve la case du mot dans reverse et on ajoute 1 pour ca case d'urls
                indice=(self.reverse.index(requete[i]))+1
                #on évite de mettre 2 fois la même page pour le calcul
                for k in range(len(self.reverse[indice])):
                    if self.reverse[indice][k] not in reverseContenu :
                        reverseContenu.append(self.reverse[indice][k])
        print(reverseContenu)
        #on remplace les url par le contenu des pages
        for url in reverseContenu:
            print("on test l\'url :" + str(url))
            for page in d.index :
                if url == page[0] :
                    reverseContenu[reverseContenu.index(url)] = page[1]

        #tableau des scores avec leurs urls triées
        score=calculScore25(requete,reverseContenu)
        bestPages=[]
        if not(reverseContenu):
            return bestPages
        else:
            for j in range(len(score)):
                bestPages.append(score[j][1])
        return bestPages
