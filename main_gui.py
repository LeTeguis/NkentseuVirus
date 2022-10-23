#!/usr/bin/python3

import pygame
from pygame.locals import *

from GameScene import GameScene
from MenuPrincipal import MenuPrincipal
from Plateau import Plateau
from Scene import Scene

pygame.init()

if __name__ == "__main__":
    running = True

    fenetre_size = (1536, 864)  # taille de la fenetre
    fenetre = pygame.display.set_mode(fenetre_size)  # création de la fenetre
    pygame.display.set_caption("Virus By Nkentseu")  # définition du titre de la fenetre

    Scene.actual = Scene.add_scene("Menu-Principal",  MenuPrincipal(fenetre, fenetre_size[0], fenetre_size[1]))
    Scene.add_scene("GameScene", GameScene(fenetre, fenetre_size[0], fenetre_size[1]))

    while running:
        for event in pygame.event.get():  # Attente des événements
            if event.type == QUIT:
                running = False
            if Scene.actual != None:
                running = Scene.actual.event(event) and running

        if Scene.actual != None:
            Scene.actual.update(10)
            Scene.actual.draw()
        # Rafraichissement
        pygame.display.flip()

pygame.quit()