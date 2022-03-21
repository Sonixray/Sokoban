import pygame
import sys
pygame.init()

size = 742
screen = pygame.display.set_mode((size, size))
from game import *
from menu import *
from sauvegarde import*

menu = Menu(screen, size)
pygame.display.set_caption("Sokoban.exe")
image=pygame.image.load("textures/gameTextures/mario/box.png")
pygame.display.set_icon(image)
menu.play_musique("Original Music/Musique menu.wav")

while not menu.done:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:     #SI LE BOUTON QUITTER EST PRESSÉ
            menu.done = True

        if menu.menuPrincipal:            #MENU PRINCIPAL

            if not menu.affiché :
                menu.drawMenu()
                menu.affiché = True  #Variable pour n'afficher le menu qu'une seule fois (et pas 60 fois par seconde !)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #SI UN CLICK EST REALISÉ
                pos = pygame.mouse.get_pos()
                menu.update_menuPrincipal(pos)

        elif menu.aide:

            if not menu.affiché:
                menu.drawAide()
                menu.affiché=True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #SI UN CLICK EST REALISÉ
                pos = pygame.mouse.get_pos()
                menu.update_aide(pos)

        elif menu.menuLvl:           #MENU DE SELECTION DE NIVEAU

            if not menu.affiché :
                menu.drawLevelSelection()
                menu.affiché = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #SI UN CLICK EST REALISÉ
                pos = pygame.mouse.get_pos()
                menu.update_menuLvl(pos)

        elif menu.menuLvlPerso:          #MENU SELECTION NIVEAU PERSONNALISÉ

            if not menu.affiché :
                menu.drawLevelSelectionPerso()
                menu.affiché = True

            if event.type == pygame.MOUSEBUTTONDOWN:     #SI UN CLICK EST REALISÉ
                pos = pygame.mouse.get_pos()
                menu.update_menuLvlPerso(pos,event)

        elif menu.play:                    #EN JEU

            if not menu.pause and not menu.fin:

                if event.type == pygame.KEYDOWN:
                    menu.update_Play(event)

            elif menu.pause:               #MENU PAUSE EN JEU

                if not menu.affiché :
                    menu.drawMenuPause()
                    menu.affiché=True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    #SI UN CLICK EST REALISÉ DANS LE MENU PAUSE
                    pos = pygame.mouse.get_pos()
                    menu.update_MenuPause(pos)

            elif menu.fin:                                                   #MENU ECRAN DE FIN QUAND ON FINI UN NIVEAU
                if not menu.affiché :
                    menu.drawLevelEnding()
                    menu.affiché=True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    #QUAND UN CLICK EST REALISÉ DANS L'ECRAN DE FIN
                    pos = pygame.mouse.get_pos()
                    menu.update_EcranDeFin(pos)

    pygame.display.flip()

menu.musique_pause()
menu.play_sfx("Original SFX/SFX see you next time.wav")
pygame.time.delay(2000)
print("Au revoir :)")
pygame.quit()