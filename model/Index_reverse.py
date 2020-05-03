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
        taille=len(index)
        taillePar2=len(index)/2
        #pair
        if len(index)%2==0:
            taillePar2=round(taillePar2)
            taille=taille-1
            for i in range(taillePar2):
                #de 0 a la N/2
                index[i][1]=index[i][1].split()
                self.mots.extend(list(dict.fromkeys(index[i][1])))
                #de N a N/2
                index[taille-i][1]=index[taille-i][1].split()
                self.mots.extend(list(dict.fromkeys(index[taille-i][1])))
        #impaire
        else:
            partieEntiere=int(taillePar2)
            taillePar2=round(taillePar2)
            #on traite le cas pour arrondir la moitier
            if partieEntiere%2==0:
                taillePar2=taillePar2+1
            for i in range(taillePar2):
                #de 0 a la N/2
                index[i][1]=index[i][1].split()
                self.mots.extend(list(dict.fromkeys(index[i][1])))
                #de N a N/2
                if i!=0:
                    index[taille-i][1]=index[taille-i][1].split()
                    self.mots.extend(list(dict.fromkeys(index[taille-i][1])))
        #on s'assure d'enlever les mots qui reviennent dans plusieurs pages pour construire le disctionnaire
        self.mots=list(dict.fromkeys(self.mots))
        #on définit reverse de la forme [[mots1,[url1,pages]....[urlN,page]],...,[motsN[url1,pages]....[urlN,page]]]
        tailleMots=len(mots)
        tailleMotsPar2=len(mots)/2
        #taille mots pair
        if len(mots)%2==0:
            tailleMotsPar2=round(tailleMotsPar2)
            tailleMots=tailleMots-1
            for i in range(tailleMotsPar2):
                self.reverse.append([self.mots[i],[]])
                self.reverse.append([self.mots[tailleMots-i],[]])
                #taille index pair
                if len(index)%2==0:
                    taillePar2=round(taillePar2)
                    taille=taille-1
                    for j in range(taillePar2):
                        if self.mots[i] in index[j][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[i][1].append([index[j][0],index[j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
                        if self.mots[tailleMots-i] in index[taille-j][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[tailleMots-i][1].append([index[taille-j][0],index[taille-j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
                #taille index impaire
                else:
                    partieEntiereIndex=int(taillePar2)
                    taillePar2=round(taillePar2)
                    if partieEntiereIndex%2==0:
                        taillePar2=taillePar2+1
                    for j in range(taillePar2):
                        if self.mots[i] in index[j][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[i][1].append([index[j][0],index[j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
                        if self.mots[tailleMots-i] in index[taille-j][1] and j!=0:
                            #on ajoute [url,page] à reverse
                            self.reverse[tailleMots-i][1].append([index[taille-j][0],index[taille-j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))                    
        #taille mots impair
        else:
            partieEntiereMots=int(tailleMotsPar2)
            tailleMotsPar2=round(tailleMotsPar2)
            if partieEntiereMots%2==0:
                tailleMotsPar2=tailleMotsPar2+1
            for i in range(tailleMotsPar2):
                self.reverse.append([self.mots[i],[]])
                if i!=0:
                    self.reverse.append([self.mots[taille-i],[]])
                #taille index impair
                if len(index)%2==0:
                    taillePar2=round(taillePar2)
                    taille=taille-1
                    for j in range(taillePar2):
                        if self.mots[i] in index[j][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[i][1].append([index[j][0],index[j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
                        if self.mots[tailleMots-i] in index[taille-j][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[tailleMots-i][1].append([index[taille-j][0],index[taille-j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
                #taille index impaire
                else:
                    partieEntiereIndex=int(taillePar2)
                    taillePar2=round(taillePar2)
                    if partieEntiereIndex%2==0:
                        taillePar2=taillePar2+1
                    for j in range(taillePar2):
                        if self.mots[i] in index[j][1]:
                            #on ajoute [url,page] à reverse
                            self.reverse[i][1].append([index[j][0],index[j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
                        if self.mots[tailleMots-i] in index[taille-j][1] and j!=0 and i!=0:
                            #on ajoute [url,page] à reverse
                            self.reverse[tailleMots-i][1].append([index[taille-j][0],index[taille-j][1]])
                            #supprimer le mots de la page
                            #index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
    
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
