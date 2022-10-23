#!/usr/bin/python3

import pygame.image

from DefaultScene import DefaultScene
from FirstIA import FirstIA
from GUI import Button, CheckBox, ListImgChoix, Widget, ListIntChoix, ListStrChoix
from Scene import Scene
from SceneData import SceneData


class MenuPrincipal(DefaultScene):

    def __init__(self, fenetre, largeur, hauteur):
        DefaultScene.__init__(self, fenetre, largeur, hauteur)
        self.initialiser()

    def initialiser(self):
        self.widgets["btn-jouer"] = Button("data/ux/btn_jouer", None, None, self.lancer_jeu, 657, 61)
        self.widgets["btn-check_box"] = CheckBox("data/ux/check_box", 596, 143)
        self.widgets["left-choix"] = ListImgChoix(["data/ux/humain_data.png", "data/ux/ordinateur_data.png"],
                                                  self.__choix_left,
                                                  "data/ux/hleft_arrow", "data/ux/hright_arrow", 250, 104, 230)
        self.widgets["right-choix"] = ListImgChoix(["data/ux/humain_data.png", "data/ux/ordinateur_data.png"],
                                                   self.__choix_rigth,
                                                   "data/ux/hleft_arrow", "data/ux/hright_arrow", 250, 1100, 230)
        self.__left_ordinateur = ComputerPanel(38, 330)
        self.__right_ordinateur = ComputerPanel(1030, 330)

        self.widgets["left-ordinateur"] = None
        self.widgets["right-ordinateur"] = None

        self.__picon = {
            "rouge": [pygame.image.load("data/ux/virus_rouge.png").convert_alpha(), [(551, 215), (935, 599)]],
            "vert": [pygame.image.load("data/ux/virus_vert.png").convert_alpha(), [(551, 599), (935, 215)]]}

    def draw(self):
        DefaultScene.draw(self)

        for key in self.__picon:
            for cord in self.__picon[key][1]:
                self.fenetre.blit(self.__picon[key][0], cord)

    def update(self, temps):
        DefaultScene.update(self, temps)

    def event(self, event_):
        DefaultScene.event(self, event_)

        return True

    def lancer_jeu(self):
        SceneData.add_info("possibiliter", self.widgets["btn-check_box"].isActivate())
        SceneData.add_in_left_corner("joueur", None)
        if self.widgets["left-ordinateur"] is not None:
            SceneData.add_in_left_corner("joueur", {"algo": self.__left_ordinateur.algo,
                                                  "profondeur": self.__left_ordinateur.profondeur,
                                                  "class": self.__left_ordinateur.class_algo})
        SceneData.add_in_rigth_corner("joueur", None)
        if self.widgets["right-ordinateur"] is not None:
            SceneData.add_in_rigth_corner("joueur", {"algo": self.__right_ordinateur.algo,
                                                    "profondeur": self.__right_ordinateur.profondeur,
                                                    "class": self.__right_ordinateur.class_algo})
        Scene.actual = Scene.get_scene("GameScene")
        Scene.actual.initialiser()

    def activation(self):
        pass

    def __choix_left(self, item):
        self.__attribute_player_type(item, "left-ordinateur", self.__left_ordinateur)

    def __choix_rigth(self, item):
        self.__attribute_player_type(item, "right-ordinateur", self.__right_ordinateur)

    def __attribute_player_type(self, item, type, attrib):
        if item == 1:
            self.widgets[type] = None
        elif item == 2:
            self.widgets[type] = attrib


class ComputerPanel(Widget):

    def __init__(self, x=0, y=0):
        Widget.__init__(self)

        self.class_algo = FirstIA()
        self.algo = "" if len(self.class_algo.list_algo()) <= 0 else self.class_algo.list_algo()[0]
        self.profondeur = 0

        self.__font = pygame.font.Font("data/fonts/SCRIPTBL.TTF", 18)

        self.__titles = {"algo": [pygame.image.load("data/ux/Algorithme.png").convert_alpha(), x + 24, y + 6],
                         "profondeur": [pygame.image.load("data/ux/Profondeur.png").convert_alpha(), x + 24, y + 47],
                         "fichier": [pygame.image.load("data/ux/Fichier Algo (.py).png").convert_alpha(), x + 24,
                                     y + 93],
                         "file_py": [self.set_file_name("default_algo.py"), x + 234, y + 100]}
        self.widgets = {
            "algo": ListStrChoix(self.class_algo.list_algo(), self.__algo, "data/ux/alleft_arrow",
                                 "data/ux/alright_arrow", 139, x + 232, y + 14),
            "profondeur": ListIntChoix(0, 100, self.__profondeur,
                                       "data/ux/alleft_arrow", "data/ux/alright_arrow", 139, x + 232, y + 56),
            "find_file": Button("data/ux/btn_dir", None, None, None, x + 386, y + 105)}

        self.__bg = pygame.image.load("data/ux/choix_ordinateur.png").convert_alpha()
        self.rect = self.__bg.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_file_name(self, file_name):
        interpret = file_name
        if len(file_name) > 20:
            interpret = file_name[0:16]
            interpret += "..."
        return self.__font.render(interpret, True, (255, 255, 255))

    def draw(self, fenetre):
        fenetre.blit(self.__bg, (self.rect.x, self.rect.y))

        for key in self.widgets:
            if self.widgets[key] is not None:
                self.widgets[key].draw(fenetre)
        for key in self.__titles:
            fenetre.blit(self.__titles[key][0], (self.__titles[key][1], self.__titles[key][2]))

    def event(self, event):
        for key in self.widgets:
            if self.widgets[key] is not None:
                self.widgets[key].event(event)

    def update(self, dt):
        pass

    def __algo(self, item):
        self.algo = item

    def __profondeur(self, item):
        self.profondeur = item
