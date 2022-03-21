import random
from copy import deepcopy

class Niveau:
    def __init__(self,level,screen,name, pack):
        self.screen = screen
        self.tableau=level
        self.name=name
        self.pack = pack

        """Auto-remplissage du tableau de 1 pour éviter les espaces blancs et pour que le niveau soit carré (pour remplir tout l'écran)"""
        lenmax=0
        for i in range(len(self.tableau)):
            if len(self.tableau[i])>lenmax:
                lenmax=len(self.tableau[i])
        for i in range(len(self.tableau)):
            if len(self.tableau[i])<lenmax:
                for j in range(lenmax-len(self.tableau[i])):
                    self.tableau[i].append(1)
        for i in range(lenmax-len(self.tableau)):
            self.tableau.append([1 for i in range(lenmax)])
        longueurx=len(self.tableau[0])
        if longueurx<len(self.tableau):
            for i in range(len(self.tableau)):
                for j in range(len(self.tableau)-longueurx):
                    self.tableau[i].append(1)

        self.start=deepcopy(self.tableau)

        self.personnage=0
        self.wall =1
        self.ground = 2
        self.box = 3
        self.checkpoint = 4
        self.boxONcheckpoint= 5
        self.player = 6
        self.playerONcheckpoint = 7

        """Création du tableau XY pour placer les cubes"""

        self.lignesTab=0
        for i in range(len(self.tableau)):
            if self.lignesTab<len(self.tableau[i]):
                self.lignesTab = len(self.tableau[i])

        self.colonesTab = len(self.tableau)

        self.longeurTab = max(self.lignesTab, self.colonesTab)
        self.longeurSquare = int(750/self.longeurTab)
        self.tabXY = []
        for i in range(self.longeurTab):
            self.tabXY.append([])
            for j in range(self.longeurTab):
                self.tabXY[i].append([int(i*self.longeurSquare), int(j*self.longeurSquare)])

        """Vérification que le niveau ne contient qu'un seul personnage et qu'il est possible"""

        tableautemp=[]
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                tableautemp.append(self.tableau[i][j])

        assert tableautemp.count(3)==tableautemp.count(4)+tableautemp.count(7), "Erreur... Il ne peut pas y avoir plus de caisse que de cible ou inversement !"
        assert tableautemp.count(6)+tableautemp.count(7)==1, "Erreur... Il ne peut y avoir qu'un seul personnage par niveau.. ni plus ni moins !"
        assert tableautemp.count(3)>0, "Erreur... Le niveau doit contenir au moins une caisse sur un sol"

    def loadTexturePack(self):      #Fonction pour charger le bon pack de texture
        if self.pack == "mario":
            path = "textures/gameTextures/mario/"
        if self.pack == "minecraft":
            path = "textures/gameTextures/minecraft/"
        if self.pack == "original":
            path = "textures/gameTextures/original/"
        self.wallImg = pygame.image.load(path+"wall.png")
        self.groundImg = pygame.image.load(path+"sol.png")
        self.boxImg = pygame.image.load(path+"box.png")
        self.playerImg = pygame.image.load(path+"player.png")
        self.boxONcheckpointImg = pygame.image.load(path+"boxOnTarget.png")
        self.playerONcheckpointImg = pygame.image.load(path+"playerOnTarget.png")
        self.checkpointImg = pygame.image.load(path+"target.png")

    def infos(self, direction):     #Fonction qui récupère les informations devant le personnage (bloc devant et bloc encore devant)
        pos=self.get_position()
        if direction=="haut":       #Si le personnage va vers le haut
            devant=self.get_haut()
            devantx2=self.get_hautx2()
            posdevant=[pos[0]-1,pos[1]]
            if devantx2!=None:
                posdevantx2=[pos[0]-2,pos[1]]
            else:
                posdevantx2=None

        if direction=="bas":        #Vers le bas
            devant=self.get_bas()
            devantx2=self.get_basx2()
            posdevant=[pos[0]+1,pos[1]]
            if devantx2!=None:
                posdevantx2=[pos[0]+2,pos[1]]
            else:
                posdevantx2=None

        if direction=="gauche":     #Vers la gauche
            devant=self.get_gauche()
            devantx2=self.get_gauchex2()
            posdevant=[pos[0],pos[1]-1]
            if devantx2!=None:
                posdevantx2=[pos[0],pos[1]-2]
            else:
                posdevantx2=None

        if direction=="droite":     #Vers la droite
            devant=self.get_droite()
            devantx2=self.get_droitex2()
            posdevant=[pos[0],pos[1]+1]
            if devantx2!=None:
                posdevantx2=[pos[0],pos[1]+2]
            else:
                posdevantx2=None

        return (pos,devant,devantx2,posdevant,posdevantx2)

    def update(self, direction):    #Met à jour le jeu en fonction de la direction et des différents obstacles

        pos=self.infos(direction)[0]
        etat=self.get_actuel()
        ancienneposition=[pos[0],pos[1]]
        devant=self.infos(direction)[1]
        devantx2=self.infos(direction)[2]
        posdevant=self.infos(direction)[3]
        posdevantx2=self.infos(direction)[4]

        if devant==self.ground:
            if etat==self.player:
                self.tableau[posdevant[0]][posdevant[1]],self.tableau[ancienneposition[0]][ancienneposition[1]]=self.player,self.ground     # 6,2 -> 2,6
            else:
                self.tableau[posdevant[0]][posdevant[1]],self.tableau[ancienneposition[0]][ancienneposition[1]]=self.player,self.checkpoint # 7,2 -> 4,6

            """Joueur se déplaçant vers une caisse"""
        elif devant==self.box:
            if posdevantx2!=None:
                if not self.tableau[posdevantx2[0]][posdevantx2[1]] in (self.wall,self.box,self.boxONcheckpoint):   #On vérifie bien qu'il n'y ai aucun obstacle devant la caisse (mur ou caisse)
                    if etat==self.player:
                        if devantx2==self.ground:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.ground,self.player,self.box # 6,3,2 -> 2,6,3
                        else:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.ground,self.player,self.boxONcheckpoint # 6,3,4 -> 2,6,5
                    else:
                        if devantx2==self.ground:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.checkpoint,self.player,self.box # 7,3,2 -> 4,6,3
                        else:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.checkpoint,self.player,self.boxONcheckpoint # 7,3,4 -> 4,6,5

            """Joueur se déplaçant vers un checkpoint"""
        elif devant==self.checkpoint:
            if etat==self.player:
                self.tableau[posdevant[0]][posdevant[1]],self.tableau[ancienneposition[0]][ancienneposition[1]]=self.playerONcheckpoint,self.ground # 6,4 -> 2,7
            else:
                self.tableau[posdevant[0]][posdevant[1]],self.tableau[ancienneposition[0]][ancienneposition[1]]=self.playerONcheckpoint,self.checkpoint # 7,4 -> 4,7

            """Joueur se déplaçant vers une caisse sur un checkpoint"""
        elif devant==self.boxONcheckpoint:
            if posdevantx2!=None:
                if not self.tableau[posdevantx2[0]][posdevantx2[1]] in (self.wall,self.box,self.boxONcheckpoint):   #On vérifie bien qu'il n'y ai aucun obstacle devant la caisse (mur ou caisse)
                    if etat==self.player:
                        if devantx2==self.ground:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.ground,self.playerONcheckpoint,self.box # 6,5,2 -> 2,7,3
                        else:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.ground,self.playerONcheckpoint,self.boxONcheckpoint # 6,5,4 -> 2,7,5
                    else:
                        if devantx2==self.ground:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.checkpoint,self.playerONcheckpoint,self.box # 7,5,2 -> 4,7,3

                        else:
                            self.tableau[ancienneposition[0]][ancienneposition[1]],self.tableau[posdevant[0]][posdevant[1]],self.tableau[posdevantx2[0]][posdevantx2[1]]=self.checkpoint,self.playerONcheckpoint,self.boxONcheckpoint # 7,5,4 -> 4,7,5

    def get_position(self):                         #Donne la position du personnage dans le tableau (x,y)
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j]==self.player or self.tableau[i][j]==self.playerONcheckpoint:
                    return [i,j]

    def get_actuel(self):                           #Donne la valeur du personnage (6 ou 7 s'il est sur un bouton)
        return self.tableau[self.get_position()[0]][self.get_position()[1]]

    def get_haut(self):                             #Donne la valeur au dessus du personnage
        if self.get_position()[0]>0:
            return self.tableau[self.get_position()[0]-1][self.get_position()[1]]

    def get_hautx2(self):                           #Donne la valeur deux fois au dessus du personnage
        if self.get_position()[0]>1:
            return self.tableau[self.get_position()[0]-2][self.get_position()[1]]

    def get_bas(self):                              #Donne la valeur en bas du personnage
        if self.get_position()[0]<len(self.tableau)-1:
            return self.tableau[self.get_position()[0]+1][self.get_position()[1]]

    def get_basx2(self):                            #Donne la valeur deux fois en bas du personnage
        if self.get_position()[0]<len(self.tableau)-2:
            return self.tableau[self.get_position()[0]+2][self.get_position()[1]]

    def get_gauche(self):                           #Donne la valeur à gauche du personnage
        if self.get_position()[1]>0:
            return self.tableau[self.get_position()[0]][self.get_position()[1]-1]

    def get_gauchex2(self):                         #Donne la valeur deux fois à gauche du personnage
        if self.get_position()[1]>1:
            return self.tableau[self.get_position()[0]][self.get_position()[1]-2]

    def get_droite(self):                           #Donne la valeur à droite du personnage
        if self.get_position()[1]<len(self.tableau[self.get_position()[0]])-1:
            return self.tableau[self.get_position()[0]][self.get_position()[1]+1]

    def get_droitex2(self):                         #Donne la valeur deux fois à droite du personnage
        if self.get_position()[1]<len(self.tableau[self.get_position()[0]])-2:
            return self.tableau[self.get_position()[0]][self.get_position()[1]+2]

    def verifier_win(self):                         #Vérifie si le niveau est gagné (si il ne reste plus de caisses ou personnage sur cible)
        for i in range(len(self.tableau)):
            if self.checkpoint in self.tableau[i]:
                return False
            if self.playerONcheckpoint in self.tableau[i]:
                return False
        return True

    def draw(self):                                 #Dessine le niveau en fonction du tableau actualisé en jeu

        for j in range(self.colonesTab):
            for i in range(len(self.tableau[j])):
                if self.tableau[j][i] == self.wall:     #Dessine un mur
                    self.wallImg = pygame.transform.scale(self.wallImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.wallImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                elif self.tableau[j][i] == self.ground:     #Dessine un sol
                    self.groundImg = pygame.transform.scale(self.groundImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.groundImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                elif self.tableau[j][i] == self.player:     #Dessine un joueur sur sol
                    self.groundImg = pygame.transform.scale(self.groundImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.groundImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))
                    self.playerImg = pygame.transform.scale(self.playerImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.playerImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                elif self.tableau[j][i] == self.box:        #Dessine une caisse
                    self.boxImg = pygame.transform.scale(self.boxImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.boxImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                elif self.tableau[j][i] == self.checkpoint:     #Dessine une cible
                    self.checkpointImg = pygame.transform.scale(self.checkpointImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.checkpointImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                elif self.tableau[j][i] == self.boxONcheckpoint:    #Dessine une caisse sur une cible
                    self.boxONcheckpointImg = pygame.transform.scale(self.boxONcheckpointImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.boxONcheckpointImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                elif self.tableau[j][i] == self.playerONcheckpoint:     #Dessine un joueur sur une cible
                    self.groundImg = pygame.transform.scale(self.groundImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.groundImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))
                    self.playerONcheckpointImg = pygame.transform.scale(self.playerONcheckpointImg, (self.longeurSquare, self.longeurSquare))
                    self.screen.blit(self.playerONcheckpointImg,(self.tabXY[i][j][0],self.tabXY[i][j][1]))

                else:                   #Sinon si la valeur n'est pas connue on dessine un bloc au hasard (mais ce cas ne devrait théoriquement jamais arriver)
                    pygame.draw.rect(self.screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),(self.tabXY[i][j][0],self.tabXY[i][j][1],self.longeurSquare,self.longeurSquare))

    def read_progression_officiel(self):    #Fonction qui lit la progression actuelle du joueur (pour afficher les niveaux en vert dans le niveau des niveaux originaux quand ils sont terminés)
        fileName="Progression/Niveaux officiels/Progression.txt"
        f = open(fileName,'r')
        message=f.read()
        f.close()
        return eval(message)

    def change_progression_officiel(self):      #Fonction qui change la progression du joueur (quand il finit un niveau original)
        fileName="Progression/Niveaux officiels/Progression.txt"
        f = open(fileName,'r')
        liste=f.read()
        liste=eval(liste)
        f.close()
        liste[self.name-1]=1
        f = open(fileName, "w")
        f.write(str(liste))
        f.close()

    def restart(self):                          #Fonction qui permet de recommencer le niveau quand on est bloqué (bouton restart en jeu)
        self.tableau=deepcopy(self.start)
        self.draw()