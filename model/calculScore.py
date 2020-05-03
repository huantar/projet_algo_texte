#prend en paramère le contenu split d'une page
#renvoie le contenu split sans les doublons
def enleveDoublons(document):
    #on enlève les doublons
    dictionnaireMots=list(dict.fromkeys(document))
    return dictionnaireMots

#prend en paramètre le contenu split d'une page 
#retourne un tableau contenant les mots et leur TF
def calculTF(document):
    TF=[]
    dictionnaireMots=enleveDoublons(document)
    nbrTotalMots=len(document)
    for i in range(len(dictionnaireMots)):
        tfValeur=document.count(dictionnaireMots[i])/nbrTotalMots
        TF.append([dictionnaireMots[i],tfValeur])
    return TF

#le contenu split d'une page et l'index qui a son contenu splité
#retourne un tableau contenant les mots et leur IDF
def calculIDF(document,listeDocuments):
    import math
    IDF=[]
    nbrDocuments=len(listeDocuments)
    dictionnaireMots=enleveDoublons(document)
    for k in range(len(dictionnaireMots)):
        occurParDoc=0
        for j in range(len(listeDocuments)):
            if listeDocuments[j][1].count(dictionnaireMots[k])>0:
                occurParDoc+=1
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
    avgdl=sommeMots/nombreDocuments
    return avgdl

#prend en paramètre l'index qui a son contenu splité
#retourne le score bm-25 toutes les pages de l'index dans un tableau trié selon le score
def calculScore25(listeDocuments):
    from operator import itemgetter
    score=[]
    for j in range(len(listeDocuments)):
        document=listeDocuments[j][1]
        score25=0
        idf=calculIDF(document,listeDocuments)
        avgdl=calculAVGDL(listeDocuments)
        k=2.0
        b=0.75
        #on calcul le score pour chaque document
        for i in range(len(idf)):
            dividende=idf[i][1]*(document.count(idf[i][0])*(k+1))
            diviseur=document.count(idf[i][0])+k*((1-b)+b*(len(document)/avgdl))
            score25=score25+(dividende/diviseur)
        score.append([score25,listeDocuments[j][0]])
    #on trie le tableau des score
    score=sorted(score, key=itemgetter(0))
    return score    
