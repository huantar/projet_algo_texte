from calculScore import *

class Index_reverse :
    """ Répertorie les mots de l'index selon les pages où ils se trouvent et leur occurence dans ces pages.
        Cette classe à pour paramètres :
        - reverse (qui contient l'occurences des mots par pages)
        """

    #constructeur de la classe index reserve
    def __init__(self,index):
        #variable qui contiendra tous les mots des contenu des pages(sans doublons)
        mots=[]
        self.reverse=[]
        #on enleve les doublons du contenu de chaque page avec split et on met la liste renvoyé à mots
        for i in range(len(index)):
            index[i][1]=index[i][1].split()
            mots.extend(list(dict.fromkeys(index[i][1])))
        #on s'assure d'enlever les mots qui reviennent dans plusieurs pages
        mots=list(dict.fromkeys(mots))
        #on définit reverse tel que [[mots1,[score,url1],...,[score,url2]],....,[motsN,[score,url1],...,[score,url2]]]
        for i in range(len(mots)):
            self.reverse.append([mots[i],[]])
            for j in range(len(index)):
                if mots[i] in index[j][1]:
                    #on ajoute [url,page] à reverse
                    self.reverse[i][1].append([index[j][0],index[j][1]])
                    #supprimer le mots de la page
                    index[j][1] = list(filter(lambda x: x != mots[i], index[j][1]))
        #on remplace le [url,page] par [score,url] 
        for k in range(len(self.reverse)):
            self.reverse[k][1]=calculScore25(self.reverse[k][1])
                
