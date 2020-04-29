from loadIndex import *



# repertoire="/home/hasib/algoTexte/pages_web"
repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web500"
print("Chargement Index a partir du dossier : " + repertoire + "\n")
data = Data(repertoire)
data.find_word('2020')
