#prend en paramère le contenu split d'une requête
#renvoie le contenu split sans les doublons
def enleveDoublons(requete):
    #on enlève les doublons
    dictionnaireMots = list(dict.fromkeys(requete))
    return dictionnaireMots

#prend en paramètre le contenu split d'une requête
#retourne un tableau contenant les mots et leur TF
def calculTF(requete):
    TF=[]
    dictionnaireMots=enleveDoublons(requete)
    nbrTotalMots=len(requete)
    for i in range(len(dictionnaireMots)):
        tfValeur=requete.count(dictionnaireMots[i])/nbrTotalMots
        TF.append([dictionnaireMots[i],tfValeur])
    return TF

#le contenu split d'une requête et l'index qui a son contenu splité
#retourne un tableau contenant les mots et leur IDF
def calculIDF(requete,listeDocuments):
    import math
    IDF=[]
    nbrDocuments=len(listeDocuments)
    dictionnaireMots=enleveDoublons(requete)
    for k in range(len(dictionnaireMots)):
        occurParDoc=0
        for j in range(0,len(listeDocuments)):
            print("k :" + str(k) + " taille dict : " + str(len(dictionnaireMots)))
            print("j :" + str(j) + " taille doc : " + str(len(listeDocuments)))
            print("doc aff : ")
            print(listeDocuments[j])
            if (listeDocuments[j].count(dictionnaireMots[k]))>0:
                occurParDoc+=1
        if occurParDoc > 0:
            idfValeur=math.log10(nbrDocuments/occurParDoc)
            IDF.append([dictionnaireMots[k],idfValeur])
    return IDF

#prend en paramètre le tableau des TF et celui des IDF
#retourne un tableau contenant les mots et leurs TF-IDF
def calculTFIDF(tf,idf):
    TFIDF=[]
    for i in range(len(tf)):
        tfidfValeur=tf[i][1]*idf[i][1]
        TFIDF.append([tf[i][0],tfidfValeur])
    return TFIDF

#prend en paramètre l'index
#retourne le avgdl(longueur moyenne des documents)
def calculAVGDL(listeDocuments):
    sommeMots=0
    nombreDocuments=len(listeDocuments)
    for i in range(len(listeDocuments)):
        sommeMots=sommeMots+len(listeDocuments[i][1])
    avgdl = 0
    if nombreDocuments != 0:
        avgdl=sommeMots/nombreDocuments
    return avgdl

#prend en paramètre l'index qui a son contenu splité et la requete splité
#retourne le score bm-25 de la requete pour chaque url
def calculScore25(requete,listeDocuments):
    from operator import itemgetter
    score=[]
    score25=0
    idf=calculIDF(requete,listeDocuments)
    avgdl=calculAVGDL(listeDocuments)
    k=2.0
    b=0.75
    for j in range(len(listeDocuments)):
        for i in range(len(idf)):
            dividende=idf[i][1]*(listeDocuments[j][1].count(idf[i][0])*(k+1))
            diviseur=listeDocuments[j][1].count(idf[i][0])+k*((1-b)+b*(len(listeDocuments[j][1])/avgdl))
            score25=score25+(dividende/diviseur)
        score.append([score25,listeDocuments[j][0]])
    score=sorted(score, key=itemgetter(0),reverse=True)
    return score
