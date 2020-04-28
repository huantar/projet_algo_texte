

#Calcule la distance de hamming entre 2 string
def dist_hamming(m1,m2):
    d = 0
    for a,b in zip(m1,m2):
        if a != b :
            d += 1
    return d

#Parcour l'index et calcule la distance de hamming de 2 voisins 
def distance_pages (index):
    #for i in range(int(len(index))-1):
    for i in range(50):
        if dist_hamming(index[i][0], index[i+1][0]) < 50 :
            print("Pour " + str(i) + " et " + str(i+1) + " on a distance de H : " + str(dist_hamming(index[i][1], index[i+1][1])))
