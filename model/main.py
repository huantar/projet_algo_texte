from  loadIndex import loadIndex
from distancePage import *

# repertoire="/home/hasib/algoTexte/pages_web"
repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web"
print("Chargement Index \n")
index = loadIndex(repertoire)
print("Chargement Index fini \n")
#print(index[0])
distance_pages(index)
