from  loadIndex import loadIndex
from distancePage import *

# repertoire="/home/hasib/algoTexte/pages_web"
repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web"
print("Chargement Index \n")
index = loadIndex(repertoire)
print("Chargement Index fini \n")
#print(index[0])
print("on a un index de taille :" + str(len(index)))
index, list_same = distance_pages(index)
print("on a un index de taille :" + str(len(index)))
