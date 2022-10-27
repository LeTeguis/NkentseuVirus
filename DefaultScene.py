#!/usr/bin/python3
import pygame

from GUI import Button
from Scene import Scene


class DefaultScene(Scene):

    def __init__(self, fenetre, largeur, hauteur):
        Scene.__init__(self, fenetre, largeur, hauteur)

        self.__bg = pygame.image.load("data/ux/bg.png").convert_alpha()
        self.__plateau = pygame.image.load("data/ux/Plateau.png").convert_alpha()

        self.widgets = {"btn-aide": Button("data/ux/btn_aide", None, None, None, 81, 28),
                        "btn-parametre": Button("data/ux/btn_param", None, None, None, 81, 92),
                        "btn-level": Button("data/ux/btn_level", None, None, None, 1445, 48)}

    def draw(self):
        self.fenetre.blit(self.__bg, (0, 0))
        self.fenetre.blit(self.__plateau, (534, 198))

        for key in self.widgets:
            if self.widgets[key] is not None:
                self.widgets[key].draw(self.fenetre)

    def update(self, temps):
        for key in self.widgets:
            if self.widgets[key] is not None:
                self.widgets[key].update(temps)

    def event(self, event_):
        for key in self.widgets:
            if self.widgets[key] is not None:
                self.widgets[key].event(event_)
        return True
