


def dist_hamming(m1,m2):
    d = 0
    for a,b in zip(m1,m2):
        if a != b :
            d += 1
    return d


def parcours_page (p1, p2):
    print(dist_hamming(p1, p2))
    #return dist_hamming(p1, p2))



#for word1 in str.split(p1) :
#    for word2 in str.split(p2) :
#        dist_hamming()
