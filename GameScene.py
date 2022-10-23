#!/usr/bin/python3

import pygame
import pygame.image
from pygame.locals import *

from Entiter import TypeEntiter, Humain, Ordinateur, Entiter
from Plateau import Plateau
from Scene import Scene
from DefaultScene import DefaultScene
from GUI import Button, Widget
from SceneData import SceneData


class GameScene(DefaultScene):
    def __init__(self, fenetre, largeur, hauteur):
        DefaultScene.__init__(self, fenetre, largeur, hauteur)
        self.initialiser()

    def initialiser(self):
        self.widgets["btn-menu"] = Button("data/ux/btn_menu", None, None, self.menu, 534, 85)
        self.widgets["btn-recommencer"] = Button("data/ux/btn_recommencer", None, None, self.recommencer, 794, 85)

        self.__block = (64, 64)
        self.__gp = (544, 208)
        self.__picon = {TypeEntiter.JOUEUR_UN: pygame.image.load("data/ux/virus_rouge.png").convert_alpha(),
                        TypeEntiter.JOUEUR_DEUX: pygame.image.load("data/ux/virus_vert.png").convert_alpha()}
        self.__ppicon = {TypeEntiter.JOUEUR_UN: pygame.image.load("data/ux/virus_rouge_possibiliter.png").convert_alpha(),
                        TypeEntiter.JOUEUR_DEUX: pygame.image.load("data/ux/virus_vert_possibiliter.png").convert_alpha()}
        self.__dec = ((self.__block[0] - self.__picon[TypeEntiter.JOUEUR_UN].get_rect().w) // 2,
                      (self.__block[1] - self.__picon[TypeEntiter.JOUEUR_UN].get_rect().h) // 2,)
        self.__plateau = Plateau()
        self.__joueur_actuel = self.__plateau.joueur_un

        self.__font = pygame.font.Font("data/fonts/SCRIPTBL.TTF", 40)
        # temps
        self.__clock = pygame.time.Clock()
        self.__t_passer = self.__clock.tick() // 1000
        self.__t_passer_s = 0
        self.__t_pose = 0
        self.__temps = {}
        self.__temps["title"] = [pygame.image.load("data/ux/Temps.png").convert_alpha(), 673, 682]
        self.__temps["ecouler"] = self.__recalculate_times(self.__t_passer_s)
        # joueur
        self.player_graphics = {"left-player": JoueurPanel(2, 6, SceneData.get_left_corner("joueur") is None, 130, 228),
                                "rigth-player": JoueurPanel(2, 6, SceneData.get_rigth_corner("joueur") is None, 1124, 228)}
        self.set_player_info()

        self.__g_player = [pygame.image.load("data/ux/joueur_actuel.png").convert_alpha(), 130, 464]

        self.__xy = (-1, -1)

    def set_player_info(self):
        if SceneData.get_left_corner("joueur") is None:
            self.__plateau.joueur_un = Humain(TypeEntiter.JOUEUR_UN)
        elif "profondeur" in SceneData.get_left_corner("joueur") and "algo" in SceneData.get_left_corner("joueur"):
            self.__plateau.joueur_un = Ordinateur(SceneData.get_left_corner("joueur")["profondeur"],
                                                  SceneData.get_left_corner("joueur")["algo"],
                                                  SceneData.get_left_corner("joueur")["class"], TypeEntiter.JOUEUR_UN)

        if SceneData.get_rigth_corner("joueur") is None:
            self.__plateau.joueur_deux = Humain(TypeEntiter.JOUEUR_DEUX)
        elif "profondeur" in SceneData.get_rigth_corner("joueur") and "algo" in SceneData.get_rigth_corner("joueur"):
            self.__plateau.joueur_deux = Ordinateur(SceneData.get_rigth_corner("joueur")["profondeur"],
                                                  SceneData.get_rigth_corner("joueur")["algo"],
                                                  SceneData.get_rigth_corner("joueur")["class"], TypeEntiter.JOUEUR_DEUX)

        self.__plateau.joueur_un.adversaire = self.__plateau.joueur_deux
        self.__plateau.joueur_deux.adversaire = self.__plateau.joueur_un

        self.__joueur_actuel = self.__plateau.joueur_un

        self.__plateau.init_game()

    def reinitialiser(self):
        self.__t_passer = 0
        self.__t_passer_s = 0
        self.__temps["ecouler"] = self.__recalculate_times(self.__t_passer_s)
        self.__plateau.init_game()
        self.__joueur_actuel = self.__plateau.joueur_un

        self.__update_playe_info(6, 2, True)
        self.__update_playe_info(6, 2, False)

        self.__g_player[1], self.__g_player[2] = 130, 464

    def __recalculate_times(self, temps):
        minutes = f"{temps // 60}"
        minutes = f"{minutes}" if len(minutes) > 1 else f"0{minutes}"
        secondes = f"{temps % 60}"
        secondes = f"{secondes}" if len(secondes) > 1 else f"0{secondes}"
        temps_ = self.__font.render(f'{minutes}:{secondes}', True, (255, 255, 255))
        x_ = ((191 - temps_.get_rect().w) // 2) + 673
        y_ = 775
        return [temps_, x_, y_]

    def draw(self):
        DefaultScene.draw(self)

        for i in range(self.__plateau.ligne):
            for j in range(self.__plateau.colone):
                e = self.__plateau.grille[j][i]
                if e != TypeEntiter.VIDE:
                    x = j * self.__block[0] + self.__gp[0] + self.__dec[0]
                    y = i * self.__block[1] + self.__gp[1] + self.__dec[1]
                    self.fenetre.blit(self.__picon[e], (x, y))
                if SceneData.info()["possibiliter"] and (j, i) in self.__joueur_actuel.possibiliter:
                    x = j * self.__block[0] + self.__gp[0] + self.__dec[0]
                    y = i * self.__block[1] + self.__gp[1] + self.__dec[1]
                    self.fenetre.blit(self.__ppicon[self.__joueur_actuel.type], (x, y))

        for key in self.__temps:
            self.fenetre.blit(self.__temps[key][0], (self.__temps[key][1], self.__temps[key][2]))

        for key in self.player_graphics:
            self.player_graphics[key].draw(self.fenetre)

        self.fenetre.blit(self.__g_player[0], (self.__g_player[1], self.__g_player[2]))

    def update(self, temps):
        DefaultScene.update(self, temps)
        t = self.__clock.tick()

        if self.__xy == (-1, -1) and isinstance(self.__joueur_actuel, Ordinateur):
            i, j = self.__joueur_actuel.jouer(None, self.__plateau.copy(), self.__joueur_actuel.type)
            self.__xy = (i, j)

        self.__t_pose += t
        if self.__t_pose >= 1000 // 8:
            self.__t_pose = 0
            self.__xy = self.dominer(self.__xy[0], self.__xy[1])

            if self.__xy == (-1, -1) and self.__plateau.match_terminer():
                print("terminer")

        self.__t_passer += t
        if self.__t_passer_s != self.__t_passer // 1000:
            self.__t_passer_s = self.__t_passer // 1000
            self.__temps["ecouler"] = self.__recalculate_times(self.__t_passer_s)

    def event(self, event):
        DefaultScene.event(self, event)

        if self.__xy == (-1, -1) and isinstance(self.__joueur_actuel, Humain):
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                i = (event.pos[0] - self.__gp[0]) // self.__block[0]
                j = (event.pos[1] - self.__gp[1]) // self.__block[1]

                self.__xy = (i, j)

        return True

    def dominer(self, i, j):
        passer, changer = self.__plateau.jouer(self.__joueur_actuel, i, j)
        if passer and changer:
            self.__update_playe_info(len(self.__joueur_actuel.possibiliter), self.__joueur_actuel.taille,
                                     self.__joueur_actuel.type == TypeEntiter.JOUEUR_UN)
            self.__joueur_actuel = self.__joueur_actuel.adversaire
            self.__update_playe_info(len(self.__joueur_actuel.possibiliter), self.__joueur_actuel.taille,
                                     self.__joueur_actuel.type == TypeEntiter.JOUEUR_UN)

            if self.__joueur_actuel.type == TypeEntiter.JOUEUR_UN:
                self.__g_player[1], self.__g_player[2] = 130, 464
            else:
                self.__g_player[1], self.__g_player[2] = 1124, 464
            return (-1, -1)
        return (i, j)

    def __update_playe_info(self, poss, virus, type):
        if type:
            self.player_graphics["left-player"].set_virus(virus)
            self.player_graphics["left-player"].set_possibiliter(poss)
        else:
            self.player_graphics["rigth-player"].set_virus(virus)
            self.player_graphics["rigth-player"].set_possibiliter(poss)

    def menu(self):
        Scene.actual = Scene.get_scene("Menu-Principal")
        Scene.actual.initialiser()

    def recommencer(self):
        self.reinitialiser()

class JoueurPanel(Widget):

    def __init__(self, virus, poss, humain, x=0, y=0):
        Widget.__init__(self)

        self.__font = pygame.font.Font("data/fonts/SCRIPTBL.TTF", 18)

        self.__bg = [pygame.image.load("data/ux/evolution.png").convert_alpha(), x]
        self.__titre = [pygame.image.load("data/ux/humain_data.png").convert_alpha()]
        if not humain:
            self.__titre = [pygame.image.load("data/ux/ordinateur_data.png").convert_alpha()]
        self.__bg.append(self.__titre[0].get_rect().h + y + 58)
        self.__titre.append(((self.__bg[0].get_rect().w - self.__titre[0].get_rect().w) // 2) + x)
        self.__titre.append(y)

        self.rect = self.__bg[0].get_rect()
        self.rect.x = x
        self.rect.y = y

        self.__titles = {"virus": [[pygame.image.load("data/ux/virus_nbr.png").convert_alpha(), x + 24, y + 113], None],
                         "poss": [[pygame.image.load("data/ux/Possibiliter_nbr.png").convert_alpha(), x + 24, y + 154],
                                  None]}
        self.set_virus(virus)
        self.set_possibiliter(poss)

        self.algo = "min-max"
        self.profondeur = 0

    def set_virus(self, virus):
        self.__titles["virus"][1] = [self.__font.render(f"{virus}", True, (255, 255, 255)), self.rect.x + 200,
                                     self.rect.y + 118]

    def set_possibiliter(self, poss):
        self.__titles["poss"][1] = [self.__font.render(f"{poss}", True, (255, 255, 255)), self.rect.x + 200,
                                            self.rect.y + 159]

    def draw(self, fenetre):
        fenetre.blit(self.__bg[0], (self.__bg[1], self.__bg[2]))
        fenetre.blit(self.__titre[0], (self.__titre[1], self.__titre[2]))

        for key in self.__titles:
            t = self.__titles[key]
            fenetre.blit(t[0][0], (t[0][1], t[0][2]))
            fenetre.blit(t[1][0], (t[1][1], t[1][2]))

    def event(self, event):
        for key in self.widgets:
            if self.widgets[key] is not None:
                self.widgets[key].event(event)

    def update(self, dt):
        pass

    def __algo(self, item):
        if item == 0:
            self.algo = "min-max"
        elif item == 1:
            self.algo = "nega-max"
        else:
            self.algo = "alpha-betha"

    def __profondeur(self, item):
        self.profondeur = item