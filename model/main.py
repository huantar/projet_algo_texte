from loadIndex import *

# repertoire="/home/hasib/algoTexte/pages_web"
repertoire="D:\\Users\\Tomasz\\Documents\\mes_doc\\master\\data\\pages_web"
print("Chargement Index \n")
data = Data(repertoire)
print("Chargement Index fini \n")



# print(index[0][1])
print("on a un index de taille :" + str(len(data.index)))
data.distance_pages()
print("on a un index de taille :" + str(len(data.index)))
data.show_no_same()
