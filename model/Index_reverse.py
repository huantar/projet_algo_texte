from calculScore import *

class Index_reverse :
    """ Répertorie les mots de l'index selon les pages où ils se trouvent et leur occurence dans ces pages.
        Cette classe à pour paramètres :
        - mots dictionnaire de mots
        - reverse (qui contient l'occurences des mots par pages)
        """

    #constructeur de la classe index reserve
    def __init__(self,index):
        self.mots=[]
        self.reverse=[]
        #on enleve les doublons du contenu de chaque page avec split et on met la liste renvoyé à mots
        for i in range(len(index)):
            index[i][1]=index[i][1].split()
            self.mots.extend(list(dict.fromkeys(index[i][1])))
            #on s'assure d'enlever les mots qui reviennent dans plusieurs pages pour construire le disctionnaire
            self.mots=list(dict.fromkeys(self.mots))
            #on définit reverse de la forme [[mots1,[url1,pages]....[urlN,page]],...,[motsN[url1,pages]....[urlN,page]]]
            taille=len(self.mots)
            taillePar2=len(self.mots)/2
            #mots pair
            if len(self.mots)%2==0:
                taillePar2=round(taillePar2)
                taille=taille-1
                for j in range(taillePar2):
                    self.reverse.append([self.mots[j],[]])
                    self.reverse.append([self.mots[taille-j],[]])
                    if self.mots[j] in index[i][1]:
                        #on ajoute [url,page] à reverse
                        self.reverse[j][1].append([index[i][0],index[i][1]])
                        #supprimer le mots de la page
                        index[i][1] = list(filter(lambda x: x != self.mots[j], index[i][1]))
                    if self.mots[taille-j] in index[i][1]:
                        #on ajoute [url,page] à reverse
                        self.reverse[taille-j][1].append([index[i][0],index[i][1]])
                        #supprimer le mots de la page
                        index[i][1] = list(filter(lambda x: x != self.mots[taille-j], index[i][1]))
            #mots impair
            else:
                partieEntiere=int(taillePar2)
                taillePar2=round(taillePar2)
                if partieEntiere%2==0:
                    taillePar2=taillePar2+1
                for j in range(taillePar2):
                    self.reverse.append([self.mots[j],[]])
                    if j!=0:
                        self.reverse.append([self.mots[taille-j],[]])
                    if self.mots[j] in index[i][1]:
                        #on ajoute [url,page] à reverse
                        self.reverse[j][1].append([index[i][0],index[i][1]])
                        #supprimer le mots de la page
                        index[i][1] = list(filter(lambda x: x != self.mots[j], index[i][1]))
                    if j!=0:
                        if self.mots[taille-j] in index[i][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[taille-j][1].append([index[i][0],index[i][1]])
                            #supprimer le mots de la page
                            index[i][1] = list(filter(lambda x: x != self.mots[taille-j], index[i][1]))

    
    #prend en paramètre une requète et renvoie les 10 meilleurs pages correspondantes
    def recherche(requete):
        requete=requete.split()
        reverseContenu=[]
        #on cherche les mots de la requete dans l'index inverse
        for i in range(len(requete)):
            if requete[i] in self.mots:
                indice=self.mots.index(requete[i])
                #on évite de mettre 2 fois la même page pour le calcul
                for k in range(len(self.reverse[indice][1])):
                    if self.reverse[indice][1][k] in reverseContenu :
                        print("page déjà en traitement")
                    else:
                        reverseContenu.extend(self.reverse[indice][1])
        #tableau des scores avec leurs urls triées
        score=calculScore25(requete,reverseContenu)
        bestPages=[]
        #si on a plus de 10 pages
        if len(score)>10:
            #on prend les 10 meilleurs pages 
            score=score[0:10]
            for j in range(len(score)):
                bestPages.append(score[j][1])
        else:
            for j in range(len(score)):
                bestPages.append(score[j][1])
        return bestPages
