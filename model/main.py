from  loadIndex import loadIndex
from distancePage import *

# repertoire="/home/hasib/algoTexte/pages_web"
repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web"
index = loadIndex(repertoire)
print("Chargement Index fini \n")
#print(index[0])
parcours_page(index[1][1], index[2][1])
