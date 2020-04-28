from progress.bar import Bar
#Pour utiliser la barre de progression il faut d'abord faire "pip install progress"

#Calcule la distance de hamming entre 2 string
def dist_hamming(m1,m2):
    d = 0
    for a,b in zip(m1,m2):
        if a != b :
            d += 1
    return d

#Parcour l'index et calcule la distance de hamming de 2 voisins
#Si la distance de hamming est trop petite on le met dans une liste a part
def distance_pages (index):
    #on initialise une liste vide pou stocker les pages trop similaires
    list_same = []
    #Compteur page trop similaires
    cmpt = 0
    #notre bar de progression
    bar = Bar('Analyse des pages', max=(len(index)))
    for i in range(int(len(index))):
    # for i in range(0,50):
        bar.next()
        for j in range(i+1, int(len(index))):
            if dist_hamming(index[i][0], index[i+1][0]) < 50 :
                #print("Pour " + str(i) + " et " + str(i+1) + " on a distance de H : " + str(dist_hamming(index[i][1], index[i+1][1])))
                if dist_hamming(index[i][1], index[i+1][1]) < 20 :
                    cmpt += 1
                    list_same.append(index[i])
                    list_same.append(index[i+1])
                    # on supprime les autres pages qui ressemblent et ainsi on garde que la premiere apparue
                    index.remove(index[i+1])
    bar.finish()
    print("On a un ratio :" + str(cmpt) +"/"+ str(i))
    return index, list_same
