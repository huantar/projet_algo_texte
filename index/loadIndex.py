#!/usr/bin/env python
# coding: utf-8

# In[49]:


import os

def loadIndex(repertoire):
    repertoireFichiers = os.listdir(repertoire)
    index=[]
    for nomFichier in repertoireFichiers:
        cheminFichier=repertoire+"/"+nomFichier
        fichier=open(cheminFichier,"rb")
        contenu=fichier.read()
        index.append([nomFichier,contenu])
        fichier.close()
    return index


# In[50]:


repertoire="/home/hasib/algoTexte/pages_web"
index=loadIndex(repertoire)
print(index[0])
