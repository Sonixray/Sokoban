import pygame
import glob
import os
from game import *
from menu import *
from sauvegarde import*

class Menu:
    def __init__(self, screen, size):
        self.menuPrincipal = True    #On commence le jeu en affichant le menu principal
        self.menuLvl, self.menuLvlPerso, self.play, self.affiché, self.done, self.aide= False, False, False, False, False, False   # "done" en True arrête tout et "affiché"" empêche d'afficher plusieurs fois les menus
        self.screen = screen
        self.size = size

        self.pack = "minecraft"

        self.decalage = 0
        self.y = 0
        self.volumeMusique = 0.1
        self.volumeSfx = 0.15

        self.bgMenu = pygame.image.load("textures/bgMenuAlt.png")
        self.bg = pygame.image.load("textures/bg.png")
        self.bg2 = pygame.image.load("textures/bg2.png")

        # --- Images de la page de selection de niv persos
        self.lvlRect =  pygame.image.load("textures/LvlSelectPerso.png")
        self.LvlSelectionPersoBtn = []
        self.btnPlay = pygame.image.load("textures/playBtn.png")
        self.LvlSelectionPersoBtn.append(self.btnPlay)
        self.btnEdit = pygame.image.load("textures/editBtn.png")
        self.LvlSelectionPersoBtn.append(self.btnEdit)
        self.btnBin = pygame.image.load("textures/bin.png")
        self.LvlSelectionPersoBtn.append(self.btnBin)
        self.btnReset = pygame.image.load("textures/reset.png")
        # --- Images page selection levels
        self.levelBtn = pygame.image.load("textures/btnLvl.png")
        self.levelBtnFinish = pygame.image.load("textures/btnLvlWin.png")
        # --- Images bouton retour, menu de victoire et de pâuse
        self.retourBtn = pygame.image.load("textures/back.png")
        self.menuWin = pygame.image.load("textures/menuWin.png")
        self.menuWinLite = pygame.image.load("textures/menuWinLite.png")
        self.menuPause = pygame.image.load("textures/menuPause.png")

        self.packMario = pygame.image.load("textures/packMario.png")
        self.packMinecraft = pygame.image.load("textures/packMinecraft.png")
        self.original = pygame.image.load("textures/packOriginal.png")

        self.soundOn = pygame.image.load("textures/soundOn.png")
        self.soundOff = pygame.image.load("textures/soundOff.png")
        self.aideimg = pygame.image.load("textures/help.png")
        self.son = True

        self.policeLvl = pygame.font.Font(None,30)  
        self.policeNomLvlPerso = pygame.font.Font(None,45)

        self.tabNiveauPerso=self.getLvlNames()


    def update(self, arg):                      #Fonction pour actualiser le menu des niveaux personnalisés si la molette est utilisée
        if arg == "down":                       #Molette bas
            self.decalage += -30
        if arg == "up":                         #Molette haut
            if self.decalage < 0:
                self.decalage += +30
        self.y += self.decalage

    def clear(self):                            #Fonction qui "nettoie" l'écran en affichant du noir (utile dans certains cas)
        self.screen.fill((0,0,0))

    # def drawLogo(self):
    #     pygame.draw.rect(self.screen, (255,0,0),((self.size - 600)//2,50,600,200)) #logo

    def drawFond(self):                                     #Fonction qui dessine le fond dans le menu principal
        pygame.draw.rect(self.screen, (255,255,255),(0,0,self.size, self.size)) #fond
        self.screen.blit(self.bgMenu, (0,0))

    def drawRetour(self, quitter):          #Fonction qui affiche le bouton retour et quitter (dans le menu principal quitter est affiché car le menu principal est le premier menu et on ne peut pas revenir en arrière)
        if quitter:                                                                               #True = afficher image "quitter", False = afficher image "retour"
            retour = pygame.draw.rect(self.screen, (255,0,0),(self.size-230,self.size-80,200,60)) #QUITTER
        else:
            retour = self.screen.blit(self.retourBtn, (self.size-235,self.size-85))               #RETOUR
        return retour

    def drawMenu(self):                                 #Fonction qui dessine le menu principal
        pygame.display.set_caption("Sokoban.exe / Menu")
        buttons = []
        self.y = 300
        #--- Boutons pour acceder aux différentes pages
        for i in range(3):
            button = pygame.draw.rect(self.screen, (255,0,0),((self.size - 400)//2,self.y,400,75)) #BtnSelectLvl
            self.y += 100
            buttons.append(button)

        #--- bouton aide
        aide = pygame.draw.rect(self.screen, (0,0,0),(self.size -  75,20, 55,55))
        son = pygame.draw.rect(self.screen, (0,0,0),(13,13, 71,69))
        buttons.append(self.drawRetour(True))

        self.screen.blit(self.bgMenu, (0,0))

        #--- Contours vert qui disent quel pack est selectionné
        if self.pack == "original":
            pygame.draw.rect(self.screen, (0,255,0),(177,self.size -  78, 61,61))

        if self.pack == "mario":
            pygame.draw.rect(self.screen, (0,255,0),(97,self.size -  78, 61,61))

        if self.pack == "minecraft":
            pygame.draw.rect(self.screen, (0,255,0),(17,self.size -  78, 61,61))

        #--- boutons des packs
        pack1 = pygame.draw.rect(self.screen, (0,0,0),(20,self.size -  75, 55,55))
        self.screen.blit(self.packMinecraft, (20,self.size -  75, 55,55))
        buttons.append(pack1)
        pack2 = pygame.draw.rect(self.screen, (0,0,0),(100,self.size -  75, 55,55))
        self.screen.blit(self.packMario, (100,self.size -  75, 55,55))
        buttons.append(pack2)
        pack3 = pygame.draw.rect(self.screen, (0,0,0),(180,self.size -  75, 55,55))
        self.screen.blit(self.original, (180,self.size -  75, 55,55))
        buttons.append(pack3)


        buttons.append(aide)
        buttons.append(son)

        if not pygame.mixer.Channel(1).get_volume()==0:
            self.screen.blit(self.soundOn, (13,13, 55,55))
        else:
            self.screen.blit(self.soundOff, (13,13, 55,55))

        self.buttons=buttons

    def drawLevelSelection(self):                    #Fonction qui dessine le menu de sélection des niveaux
        pygame.display.set_caption("Sokoban.exe / Original levels")
        buttons = []
        self.screen.blit(self.bg, (0,0))
        self.y = 225
        fileName="Progression/Niveaux officiels/Progression.txt"
        f = open(fileName,'r')
        message=f.read()
        f.close()
        progression = eval(message)
        niveau=0
        for i in range(5):
            self.x = 38
            self.x_texte = 43
            self.y += 70
            for j in range(8):
                self.x += 70
                self.x_texte += 70
                if progression[niveau]==1:
                    btn = self.screen.blit(self.levelBtnFinish, (self.x,self.y))
                else:
                    btn = self.screen.blit(self.levelBtn, (self.x,self.y))

                buttons.append(btn)
                texte = self.policeLvl.render(str(i*8+j+1),True,pygame.Color("#FFFFFF")) #(i*8+j+1) permet de compter les niveaux
                if niveau in (9,16,24,32):  #On redécale le x à certains moments pour éviter un décalage dans l'affichage des niveaux
                    self.x_texte-=5
                self.screen.blit(texte, (self.x_texte+20,self.y+10))
                niveau+=1

        btn = self.screen.blit(self.btnReset, (self.size-450,self.size-85))
        buttons.append(btn)
        buttons.append(self.drawRetour(False))

        self.buttons=buttons

    def drawLevelSelectionPerso(self):                  #Fonction qui dessine le menu de sélection des niveaux personnalisés
        pygame.display.set_caption("Sokoban.exe / Custom levels")
        self.screen.blit(self.bg, (0, 0))
        buttons = []
        self.y = 245 + self.decalage
        self.x = 60
        for i in range(len(self.tabNiveauPerso)):
            self.y += 80
            self.screen.blit(self.lvlRect, (self.x, self.y - 7)) #le carré qui fait le contour de notre lvl
            temp = self.x
            select = [] #On mettras nos 3 bouttons Jouer / Editer / Supp dedans
            for j in range(3):
                button = self.screen.blit(self.LvlSelectionPersoBtn[j], (self.x + 440,self.y + 5))
                select.append(button)
                self.x += 60

            self.x = temp
            buttons.append(select)
            texte = self.policeNomLvlPerso.render(str(self.tabNiveauPerso[i][:-4]),True,pygame.Color("#FFFFFF")) #On prends la liste des niv et on en affiche un et on enlève le ".txt"
            self.screen.blit(texte, (self.x+25,self.y+20))
        self.screen.blit(self.bg2, (0,0)) #Permet de cacher l'icone des niveaux quand on monte / descend
        buttons.append(self.drawRetour(False))

        self.buttons=buttons

    def drawMenuPause(self):                            #Fonction qui dessine le menu pause en jeu
        self.musique_pause()
        buttons=[]
        self.x = 150
        self.y = 250
        for i in range(3):
            button = pygame.draw.rect(self.screen, (255,255,255),((self.size - 300)//2,self.y,300,75)) #Bouton reprendre
            self.y += 100
            buttons.append(button)

        self.screen.blit(self.menuPause, ((self.size - 505)//2,180))
        self.buttons=buttons

    def getLvlNames(self):                                  #Fonction qui permet de récupérer le nom des niveaux personnalisés, pour ensuite les afficher dans le menu des niveaux perosnnalisés
        fichiers = glob.glob('./Niveaux/Niveaux personnalisés/*.txt') # Nous permet de récuperer tous les fichiers.txt dans le fichier "Niveaux personnalisés"
        fichiersTab = []
        for fichier in fichiers:
            fichiersTab.append(os.path.basename(fichier))             # Nous permet de récup uniquement le nom du fichier
        return fichiersTab

    def drawLevelEnding(self):                             #Fonction qui dessine le menu de fin de niveau
        if self.officiel and self.level.name != 40:          #self.officiel en True = Niveau officiel (bouton niveau suivant actif), en False = niveau personnalisé (pas de bouton niveau suivant)
            buttons = []
            self.x = 150
            self.y = 250
            for i in range(3):
                button = pygame.draw.rect(self.screen, (255,255,255),((self.size - 300)//2,self.y,300,75))
                self.y += 100
                buttons.append(button)
                
            self.screen.blit(self.menuWin, ((self.size - 505)//2,180))
            self.buttons = buttons

        else:
            buttons=[]
            self.x = 150
            self.y = 300
            # bg=pygame.draw.rect(self.screen, (255,255,255),((self.size - 480)//2,190,480,400))

            for i in range(2):
                button = pygame.draw.rect(self.screen, (255,255,255),((self.size - 300)//2,self.y,300,75))
                self.y += 100
                buttons.append(button)
            self.screen.blit(self.menuWinLite, ((self.size - 495)//2,230))
            self.buttons=buttons

    def drawAide(self):                          #Fonction qui dessine le menu aide
        pygame.display.set_caption("Sokoban.exe / Aide")
        self.screen.blit(self.aideimg, (0,0))
        button=self.drawRetour(False)
        self.buttons=[button]

    def update_menuPrincipal(self,pos):          #Fonction qui gère les évènements du menu principal
        if self.buttons[0].collidepoint(pos):    #Menu sélection de niveau officiel
            self.play_sfx("Original SFX/SFX switch menu.wav")
            self.menuPrincipal,self.affiché,self.menuLvl = False,False,True

        if self.buttons[1].collidepoint(pos):    #Menu sélection de niveau personnalisé
            self.play_sfx("Original SFX/SFX switch menu.wav")
            self.decalage = 0                    #On remet le décalage du menu des niveaux persos à 0
            self.menuPrincipal,self.affiché,self.menuLvlPerso = False,False,True

        if self.buttons[2].collidepoint(pos):    #Menu créateur de niveau
            self.play_sfx("Original SFX/SFX switch menu.wav")
            print("L'éditeur de niveau sera bientôt disponible...")

        if self.buttons[3].collidepoint(pos):    #SI LE BOUTON QUITTER EST PRESSÉ
            self.done=True

        if self.buttons[4].collidepoint(pos):     #bouton du pack minecraft
            self.play_sfx("Original SFX/SFX changer skin.wav")
            self.pack, self.affiché = "minecraft", False

        if self.buttons[5].collidepoint(pos):     #bouton du pack mario
            self.play_sfx("Original SFX/SFX changer skin.wav")
            self.pack, self.affiché = "mario", False

        if self.buttons[6].collidepoint(pos):     #bouton du dernier pack
            self.play_sfx("Original SFX/SFX changer skin.wav")
            self.pack, self.affiché = "original", False

        if self.buttons[7].collidepoint(pos):     #bouton tutoriel
            self.play_sfx("Original SFX/SFX switch menu.wav")
            self.aide, self.menuPrincipal, self.affiché=True,False,False

        if self.buttons[8].collidepoint(pos):     #bouton tutoriel
            self.affiché = False
            self.mute()

    def update_aide(self,pos):                          #Fonction qui gère les évènements du menu d'aide
        if self.buttons[0].collidepoint(pos):
            self.play_sfx("Original SFX/SFX switch menu.wav")
            self.aide,self.menuPrincipal,self.affiché=False,True,False


    def update_menuLvl(self,pos):                       #Fonction qui gère les évènements du menu des niveaux originaux

        if self.buttons[41].collidepoint(pos):                #SI LE BOUTON RETOUR EST PRESSÉ
            self.play_sfx("Original SFX/SFX switch menu.wav")
            self.menuLvl, self.affiché, self.menuPrincipal = False, False, True

        elif self.buttons[40].collidepoint(pos):         #SI LE BOUTON RENITIALISER EST PRESSÉ
            self.play_sfx("Original SFX/SFX restart progression.wav")
            restart_progression()
            self.affiché=False

        else:                                       #SI UN BOUTON NIVEAU EST PRESSÉ
            for i in range(len(self.buttons)):
                if self.buttons[i].collidepoint(pos):
                    self.musique_pause()
                    self.play_sfx("Original SFX/SFX lancer niveau.wav")
                    pygame.display.flip()
                    pygame.time.delay(300)
                    self.play_musique("Original Music/Musique en jeu.wav")
                    self.level=Niveau(read_niveauofficiel(str(i+1)),self.screen,i+1, self.pack)
                    self.level.loadTexturePack()
                    self.clear()
                    self.level.draw()
                    pygame.display.set_caption("Sokoban.exe / Original levels / Level "+str(self.level.name))
                    self.pause,self.fin,self.menuLvl,self.play,self.officiel=False, False, False, True, True

    def update_menuLvlPerso(self,pos,event):                           #Fonction qui gère tous les évènements du menu des niveaux personnalisés (molette haut ou bas, clics)

        if event.button == 1:

            if self.buttons[len(self.buttons)-1].collidepoint(pos):    #SI LE BOUTON RETOUR EST PRESSÉ
                self.play_sfx("Original SFX/SFX switch menu.wav")
                self.menuLvlPerso,self.affiché,self.menuPrincipal = False,False,True

            else:
                for i in range(len(self.buttons)-1):
                    for j in range(3):
                        if self.buttons[i][j].collidepoint(pos):
                            if j==0:                                   #SI LE BOUTON PLAY EST PRESSÉ
                                self.musique_pause()
                                self.play_sfx("Original SFX/SFX lancer niveau.wav")
                                pygame.display.flip()
                                pygame.time.delay(300)
                                self.level=Niveau(read_niveauperso(self.getLvlNames()[i]),self.screen,self.getLvlNames()[i], self.pack)
                                self.level.loadTexturePack()
                                self.clear()
                                self.level.draw()
                                self.pause,self.fin,self.menuLvlPerso,self.play,self.officiel=False, False, False, True, False
                                self.play_musique("Original Music/Musique en jeu.wav")
                                pygame.display.set_caption("Sokoban.exe / Custom levels / "+str(self.level.name)[0:-4])

                            elif j==1:                                 #SI LE BOUTON ÉDITEUR DE NIVEAU EST PRESSÉ
                                self.play_sfx("Original SFX/SFX switch menu.wav")
                                print("L'éditeur de niveau sera bientôt disponible...")

                            elif j==2:                                 #SI LE BOUTON SUPPRIMER UN NIVEAU EST PRESSÉ
                                self.play_sfx("Original SFX/SFX supprimer niveau.wav")
                                os.remove("Niveaux/Niveaux personnalisés/"+self.getLvlNames()[i])
                                self.tabNiveauPerso=self.getLvlNames()
                                self.affiché=False
        else:

            if event.button == 4:
                self.update("up")
                self.affiché=False

            if event.button == 5:
                self.update("down")
                self.affiché=False

    def update_Play(self,event):                                #Fonction pour update le jeu en fonction des différents évênements

        if event.key==pygame.K_RIGHT or event.key==pygame.K_d:  #DROITE
            self.level.update("droite")

        elif event.key==pygame.K_LEFT or event.key==pygame.K_q: #GAUCHE
            self.level.update("gauche")

        elif event.key==pygame.K_UP or event.key==pygame.K_z:   #HAUT
            self.level.update("haut")

        elif event.key==pygame.K_DOWN or event.key==pygame.K_s: #BAS
            self.level.update("bas")

        elif event.key==pygame.K_ESCAPE:                        #PAUSE
            self.affiché,self.pause=False,True

        self.level.draw()

        if self.level.verifier_win()==True:                     #Si niveau terminé
            self.musique_pause()
            self.play_sfx("Original SFX/SFX niveau terminé.wav")
            if self.officiel:
                self.level.change_progression_officiel()        #On met le niveau comme terminé si c'est un niveau officiel
            self.affiché,self.fin=False,True
            pygame.display.flip()
            pygame.time.delay(2000)

    def update_MenuPause(self,pos):                              #Fonction pour update le menu pause en jeu
        if self.buttons[0].collidepoint(pos):                    #Reprendre le niveau
            self.pause=False
            self.level.draw()
            self.musique_unpause()
        if self.buttons[1].collidepoint(pos):                    #Recommencer le niveau
            self.play_sfx("Original SFX/SFX restart niveau actuel.wav")
            self.pause=False
            self.level.restart()
            self.level.draw()
            self.play_musique("Original Music/Musique en jeu.wav")
        if self.buttons[2].collidepoint(pos):                    #Quitter le niveau
            self.play_sfx("Original SFX/SFX quitter niveau.wav")
            pygame.time.delay(500)
            if self.officiel:
                self.play,self.pause,self.fin,self.affiché,self.menuLvl=False,False,False,False,True
            else:
                self.play,self.pause,self.fin,self.affiché,self.menuLvlPerso=False,False,False,False,True
            self.play_musique("Original Music/Musique menu.wav")

    def update_EcranDeFin(self,pos):                             #Fonction pour update l'écran de fin quand on termine un niveau
        if self.officiel and self.level.name!=40:                #self.level.name!=40 car on n'affiche pas le bouton niveau suivant une fois le niveau 40 terminé (car c'est le dernier niveau)
            if self.buttons[0].collidepoint(pos):
                self.level=Niveau(read_niveauofficiel(str(self.level.name+1)),self.screen,self.level.name+1, self.pack)
                self.level.loadTexturePack()
                self.level.draw()
                self.fin=False
                self.play_musique("Original Music/Musique en jeu.wav")
                pygame.display.set_caption("Sokoban.exe / Original levels / Level "+str(self.level.name))
            if self.buttons[1].collidepoint(pos):
                self.fin=False
                self.level.restart()
                self.level.draw()
                self.play_musique("Original Music/Musique en jeu.wav")
            if self.buttons[2].collidepoint(pos):    #Quitter le niveau
                self.play,self.pause,self.fin,self.affiché,self.menuLvl=False,False,False,False,True
                self.play_musique("Original Music/Musique menu.wav")
        else:
            if self.buttons[0].collidepoint(pos):
                self.fin=False
                self.level.restart()
                self.level.draw()
                self.play_musique("Original Music/Musique en jeu.wav")
            if self.buttons[1].collidepoint(pos):    #Quitter le niveau
                if not self.officiel:
                    self.play,self.pause,self.fin,self.affiché,self.menuLvlPerso=False,False,False,False,True
                    self.play_musique("Original Music/Musique menu.wav")
                else:
                    self.play,self.pause,self.fin,self.affiché,self.menuLvl=False,False,False,False,True
                    self.play_musique("Original Music/Musique menu.wav")

    def play_musique(self,path):                                    #Fonction pour jouer de la musique (en jeu ou dans le menu)
        pygame.mixer.Channel(1).set_volume(self.volumeMusique)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(path), -1)	#-1 permet de jouer la musique en boucle (elle ne s'arretera jamais)

    def musique_pause(self):                                        #Fonction pour mettre la musique en pause (quand on met pause en jeu par exemple)
        pygame.mixer.Channel(1).pause()

    def musique_unpause(self):                                      #Fonction pour reprendre la musique quand elle a été mise en pause
        pygame.mixer.Channel(1).unpause()

    def play_sfx(self,path):                                        #Fonction pour jouer un SFX
        pygame.mixer.Channel(2).set_volume(self.volumeSfx)
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(path))

    def mute(self):                                                 #Fonction pour enlever le son ou le remettre (grâce au bouton en haut à gauche dans le menu principal)
        if self.volumeMusique == 0:                                 #Si le son est déjà enlevé on le remet
            self.volumeMusique = 0.1
            self.volumeSfx = 0.15

        else:                                                       #Sinon on met le volume de tous les sons à 0
            self.volumeMusique = 0
            self.volumeSfx = 0

        pygame.mixer.Channel(1).set_volume(self.volumeMusique)
        pygame.mixer.Channel(2).set_volume(self.volumeSfx)