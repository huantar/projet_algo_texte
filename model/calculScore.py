#prend en paramère un string
#renvoie deux tableaux,un qui contient les mots du string et un autre sans les doublons
def enleveDoublons(document):
    #transforme la chaine en tableau de mots
    texte=document.split()
    #on enlève les doublons
    dictionnaireMots=list(dict.fromkeys(texte))
    return (texte,dictionnaireMots)

#prend en paramètre un string contenant le contenu de la page de l'index
#retourne un tableau contenant les mots et leur TF
def calculTF(document):
    TF=[]
    texte,dictionnaireMots=enleveDoublons(document)
    nbrTotalMots=len(texte)
    for i in range(len(dictionnaireMots)):
        tfValeur=texte.count(dictionnaireMots[i])/nbrTotalMots
        TF.append([dictionnaireMots[i],tfValeur])
    return TF

#prend en paramètre le string qui contient le contenu du document et l'index 
#retourne un tableau contenant les mots et leur IDF
def calculIDF(document,listeDocuments):
    import math
    IDF=[]
    nbrDocuments=len(listeDocuments)
    texte,dictionnaireMots=enleveDoublons(document)
    for i in range(len(listeDocuments)):
        listeDocuments[i][1]=listeDocuments[i][1].split()
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

#prend en paramètre le contenu string d'une page et l'index
#retourne le score bm-25 de cette page
def calculScore25(document,listeDocuments):
    score25=0
    idf=calculIDF(document,listeDocuments)
    avgdl=calculAVGDL(listeDocuments)
    k=2.0
    b=0.75
    document=document.split()
    for i in range(len(idf)):
        dividende=idf[i][1]*(document.count(idf[i][0])*(k+1))
        diviseur=document.count(idf[i][0])+k*((1-b)+b*(len(document)/avgdl))
        score25=score25+(dividende/diviseur)
        print(score25)
    return score25    
