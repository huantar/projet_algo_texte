
#Calcule la distance de hamming entre 2 string, avec une distance max
def dist_hamming(m1,m2):
    d = 0
    for a,b in zip(m1,m2):
        if a != b :
            d += 1
    return d
