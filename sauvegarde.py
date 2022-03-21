import os
import pygame
def sauvegarde(niveau,nom):                     #Fonction pour sauvegarder un niveau (pour l'éditeur de niveau)
    fileName = "Niveaux/"+nom+".txt"
    i=0
    tmp=nom
    while os.path.isfile(fileName)==True:       #Si un fichier du même nom existe déjà on change le nom pour éviter d'écraser le fichier déjà existant
        i+=1
        tmp = nom+" ("+str(i)+")"
        fileName = "Niveaux/"+tmp+".txt"
    if i!=0:
        nom = nom+" ("+str(i)+")"
    fichier = open("Niveaux/"+nom+".txt", "w")  #Ensuite on créé le fichier
    fichier.write(str(niveau))                  #Et on écrit le niveau dedant
    fichier.close()

def read_niveauperso(nom):                      #Fonction pour lire un niveau personnalisé
    fileName = "Niveaux/Niveaux personnalisés/"+nom
    if os.path.isfile(fileName)==False:     #Cas où le fichier n'existe pas
        return None
    else:
        f = open(fileName,'r') #Sinon on lit le contenu du fichier et on le converti en tableau (eval() converti str -> tab)
        message = f.read()
        f.close()
        return eval(message)

def read_niveauofficiel(nom):                   #Fonction pour lire un niveau officiel
    fileName = "Niveaux/Niveaux officiels/"+nom+".txt"
    if os.path.isfile(fileName)==False:     #Cas où le fichier n'existe pas
        return None
    else:
        f = open(fileName,'r') #Sinon on lit le contenu du fichier et on le converti en tableau (eval() converti str -> tab)
        message = f.read()
        f.close()
        return eval(message)

def restart_progression():  #Fonction pour remettre à 0 la progression du jeu
    fileName="Progression/Niveaux officiels/Progression.txt"
    f = open(fileName, "w")
    f.write("[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]")
    f.close()