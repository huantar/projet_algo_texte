from loadIndex import *
from Index_reverse import *



# repertoire="/home/hasib/algoTexte/pages_web"
repertoire="C:\\Users\\mathi\\OneDrive\\Bureau\\pages_web2"
print("Chargement Index a partir du dossier : " + repertoire + "\n")
data = Data(repertoire)
# data.find_word('2020')
index_inverse = Index_reverse(data.index)
meilleur=[]
meilleur = index_inverse.recherche("simple")
print(meilleur[0])
print(len(meilleur))
