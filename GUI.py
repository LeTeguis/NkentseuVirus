#!/usr/bin/python3
import pygame
from pygame.locals import *


class Widget:

    def __init__(self):
        self.rect = (0, 0, 0, 0)

    def draw(self, fenetre):
        pass

    def event(self, event):
        pass

    def update(self, dt):
        pass

class Button(Widget):

    def __init__(self, name, normal, hover, click, x=0, y=0):
        Widget.__init__(self)

        self.normal = [self.get_img(name, "normal"), normal]
        self.hover = [self.get_img(name, "hover"), hover]
        self.click = [self.get_img(name, "click"), click]
        self.actual = self.normal
        self.rect = self.normal[0].get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_img(self, name, type):
        return pygame.image.load(f"{name}_{type}.png").convert_alpha()

    def draw(self, fenetre):
        if self.actual != None:
            fenetre.blit(self.actual[0], (self.rect.x, self.rect.y))

    def update(self, dt):
        pass

    def event(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1 and self.click != None and self.normal != None\
                and self.hover != None:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w \
                    and self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h:
                if self.actual[1] is not None:
                    self.actual[1]()
                self.actual = self.hover
            elif self.actual == self.click:
                self.actual = self.normal
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.click != None:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w \
                    and self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h:
                self.actual = self.click
        if event.type == MOUSEMOTION and self.click != None and self.normal != None \
                and self.hover != None and self.actual != self.click:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w \
                    and self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h:
                self.actual = self.hover
            else:
                self.actual = self.normal

class CheckBox(Widget):

    def __init__(self, nom, x=0, y=0):
        Widget.__init__(self)

        self.__activer = self.get_img(nom, "activate")
        self.__desactiver = self.get_img(nom, "desactivate")

        self.actual = self.__activer
        self.rect = self.__activer.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_img(self, name, type):
        return pygame.image.load(f"{name}_{type}.png").convert_alpha()

    def draw(self, fenetre):
        if self.actual != None:
            fenetre.blit(self.actual, (self.rect.x, self.rect.y))

    def event(self, event):
        if event.type == MOUSEBUTTONUP and event.button == 1 and self.__activer != None and self.__desactiver != None:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.rect.w \
                    and self.rect.y <= event.pos[1] <= self.rect.y + self.rect.h:
                if self.actual == self.__activer:
                    self.actual = self.__desactiver
                else:
                    self.actual = self.__activer

    def update(self, dt):
        pass

    def isActivate(self):
        return self.actual == self.__activer

class ListImgChoix(Widget):

    def __init__(self, list_nom, event, left, right, interieur, x=0, y=0):
        Widget.__init__(self)

        self.actual = 0
        self.x = x
        self.y = y

        self.__liste = []
        self.__event = event
        i = 0
        for nom in list_nom:
            self.add_item(nom)
            i += 1
        self.__intern = interieur
        self.__left_arrow = Button(left, None, None, self.__go_left, x, y)
        self.__right_arrow = Button(right, None, None, self.__go_right, x + interieur + self.__left_arrow.rect.w, y)

        self.__intern_x = x
        self.__intern_y = y

        self.__recalculate()

    def __recalculate(self):
        if self.__liste[self.actual] is not None:
            self.__intern_x = ((self.__intern - self.__liste[self.actual].get_rect().w) // 2) + self.x + self.__left_arrow.rect.w
            self.__intern_y = ((self.__left_arrow.rect.h - self.__liste[self.actual].get_rect().h) // 2) + self.y

    def __go_left(self):
        self.actual -= 1
        if self.actual < 0:
            self.actual = 0
        else:
            self.__recalculate()
            if self.__event is not None:
                self.__event(self.actual + 1)

    def __go_right(self):
        self.actual += 1
        if self.actual >= len(self.__liste):
            self.actual = len(self.__liste) - 1
        else:
            self.__recalculate()
            if self.__event is not None:
                self.__event(self.actual + 1)

    def add_item(self, name):
        self.__liste.append(pygame.image.load(name).convert_alpha())

    def get_actual(self):
        return self.actual + 1

    def draw(self, fenetre):
        if self.actual != None:
            self.__left_arrow.draw(fenetre)
            fenetre.blit(self.__liste[self.actual], (self.__intern_x, self.__intern_y))
            self.__right_arrow.draw(fenetre)

    def event(self, event):
        self.__left_arrow.event(event)
        self.__right_arrow.event(event)

    def update(self, dt):
        pass

class ListIntChoix(Widget):

    def __init__(self, min_, max_, event, left, right, interieur, x=0, y=0):
        Widget.__init__(self)

        self.x = x
        self.y = y
        self.__intern = interieur

        self.__borne = (min_ if min_ < max_ else max_, min_ if min_ > max_ else max_)
        self.actual = self.__borne[0]
        self.__pas = 1
        self.__event = event
        self.__left_arrow = Button(left, None, None, self.__go_left, x, y)
        self.__right_arrow = Button(right, None, None, self.__go_right, x + interieur + self.__left_arrow.rect.w, y)

        self.__font = pygame.font.Font("data/fonts/SCRIPTBL.TTF", 18)
        self.__recalculate(self.actual)

    def __recalculate(self, valeur):
        self.__text = self.__font.render(f'{valeur}', True, (255, 255, 255))
        self.__textx = ((self.__intern - self.__text.get_rect().w) // 2) + self.x + self.__left_arrow.rect.w
        self.__texty = ((self.__left_arrow.rect.h - self.__text.get_rect().h) // 2) + self.y

    def __go_left(self):
        self.actual -= self.__pas
        if self.actual < self.__borne[0]:
            self.actual = self.__borne[0]
        else:
            self.__recalculate(self.actual)
            if self.__event is not None:
                self.__event(self.actual)

    def __go_right(self):
        self.actual += self.__pas
        if self.actual > self.__borne[1]:
            self.actual = self.__borne[1]
        else:
            self.__recalculate(self.actual)
            if self.__event is not None:
                self.__event(self.actual)

    def get_actual(self):
        return self.actual

    def draw(self, fenetre):
        self.__left_arrow.draw(fenetre)
        fenetre.blit(self.__text, (self.__textx, self.__texty))
        self.__right_arrow.draw(fenetre)

    def event(self, event):
        self.__left_arrow.event(event)
        self.__right_arrow.event(event)

    def update(self, dt):
        pass

class ListStrChoix(Widget):

    def __init__(self, string_list, event, left, right, interieur, x=0, y=0):
        Widget.__init__(self)

        self.x = x
        self.y = y
        self.__intern = interieur

        self.__str = string_list.copy()
        self.actual = 0
        self.__event = event
        self.__left_arrow = Button(left, None, None, self.__go_left, x, y)
        self.__right_arrow = Button(right, None, None, self.__go_right, x + interieur + self.__left_arrow.rect.w, y)

        self.__font = pygame.font.Font("data/fonts/SCRIPTBL.TTF", 18)
        self.__recalculate(self.actual)

    def __recalculate(self, valeur):
        if len(self.__str) >= 0 and 0 <= valeur < len(self.__str):
            self.__text = self.__font.render(self.__str[valeur], True, (255, 255, 255))
            self.__textx = ((self.__intern - self.__text.get_rect().w) // 2) + self.x + self.__left_arrow.rect.w
            self.__texty = ((self.__left_arrow.rect.h - self.__text.get_rect().h) // 2) + self.y

    def __go_left(self):
        self.actual -= 1
        if self.actual < 0:
            self.actual = 0
        else:
            self.__recalculate(self.actual)
            if self.__event is not None:
                self.__event(self.__str[self.actual])

    def __go_right(self):
        self.actual += 1
        if self.actual >= len(self.__str):
            self.actual = len(self.__str) - 1
        else:
            self.__recalculate(self.actual)
            if self.__event is not None:
                self.__event(self.__str[self.actual])

    def get_actual(self):
        return self.__str[self.actual]

    def draw(self, fenetre):
        self.__left_arrow.draw(fenetre)
        if len(self.__str) > 0:
            fenetre.blit(self.__text, (self.__textx, self.__texty))
        self.__right_arrow.draw(fenetre)

    def event(self, event):
        self.__left_arrow.event(event)
        self.__right_arrow.event(event)

    def update(self, dt):
        pass