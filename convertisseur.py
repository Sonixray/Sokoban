import os

def convertisseur(nom):
    level = open("Niveaux/Niveaux personnalisés/level"+nom+'.txt')
    message = level.read()
    level.close()
    print(len(message))

    lignes=1
    for i in range(len(message)):
        if '\n' in message[i]:
            lignes+=1

    tab=[[] for i in range (lignes)]
    j=0
    repetitions=0
    for i in range(len(tab)):
        while not "\n" in message[j] and repetitions+lignes!=len(message):

            repetitions+=1

            if message[j]=="#":
                tab[i].append(1)

            elif message[j]=="@":
                tab[i].append(6)

            elif message[j]=="+":
                tab[i].append(7)

            elif message[j]=="$":
                tab[i].append(3)

            elif message[j]=="*":
                tab[i].append(5)

            elif message[j]==".":
                tab[i].append(4)

            elif message[j]==" ":
                tab[i].append(2)

            j+=1
        j+=1

    level = open("Niveaux/Niveaux personnalisés/level"+nom+'.txt', "w")
    level.write(str(tab))
    level.close()
    print("Niveau converti avec succès !")

"""Les niveaux ont été trouvés sur https://github.com/kazantzakis/pySokoban et convertis en tableaux de tableaux grâce à cette fonction"""
#Pour être converti, le niveau doit se situer dans le dossier "Niveaux/Niveaux personnalisés" et doit avoir un nom de la forme "level5.txt" avec à la place de 5 n'importe quel nombre.
#Il suffit juste ensuite de lancer la fonction convertisseur avec en paramètre le nombre (ici convertisseur("5") par exemple). Attention le paramètre doit être sous forme de STR et non de INT !