#!/usr/bin/python3
from enum import Enum
import copy


class TypeEntiter(Enum):
    JOUEUR_UN = 1
    JOUEUR_DEUX = 2
    VIDE = 0

    def __str__(self):
        return f"{self.value}"


class Entiter:

    def __init__(self, type_e, recurs=True):
        if type(type_e) is not TypeEntiter:
            raise TypeError("type_e doit etre de type TypeEntiter")

        self.__type = type_e
        self.__possibiliter = []
        self.__adversaire = None
        self.__taille = 0
        self.__gain = 0

        if type_e == TypeEntiter.JOUEUR_UN:
            if recurs:
                self.__adversaire = Entiter(TypeEntiter.JOUEUR_DEUX, False)
                self.__adversaire.__adversaire = self
        if type_e == TypeEntiter.JOUEUR_DEUX and recurs:
            if recurs:
                self.__adversaire = Entiter(TypeEntiter.JOUEUR_UN, False)
                self.__adversaire.__adversaire = self

    def copy(self):
        entiter = Entiter(self.__type, False)
        entiter.__possibiliter.clear()
        for (i, j) in self.__possibiliter:
            entiter.__possibiliter.append((i, j))
        entiter.__adversaire = self.__adversaire
        entiter.__taille = self.__taille
        entiter.__gain = self.__gain

        return entiter

    @property
    def taille(self):
        return self.__taille

    @taille.setter
    def taille(self, value):
        #print(value)
        if self.type == TypeEntiter.VIDE:
            return
        if type(value) is not int:
            raise TypeError("le nombre de virus est de type entier")
        if value < 0:
            raise ValueError("le nombre de virus doit etre plus grand ou egale a 0")
        self.__taille = value

    @property
    def possibiliter(self):
        return self.__possibiliter

    @possibiliter.setter
    def possibiliter(self, value):
        self.__add_or_remove(value)

    def remove_possibiliter(self, value):
        self.__add_or_remove(value, True)

    def __add_or_remove(self, value, remove=False):
        if self.type == TypeEntiter.VIDE:
            return
        if type(value) is not list and type(value) is not tuple:
            raise TypeError("la veur doit etre sois une liste de tuple sois un tuple")
        if type(value) is list:
            for t in value:
                if type(t) is not tuple:
                    raise TypeError("les element de cette liste doivent etre des tuple")
                if type(t[0]) is not int and type(t[1]) is not int:
                    raise TypeError("les element du tuple doivent etre de type entier")
                if t not in self.__possibiliter:
                    if not remove:
                        self.__possibiliter.append(t)
                else:
                    if remove:
                        self.__possibiliter.remove(t)
        else:
            if type(value[0]) is not int and type(value[1]) is not int:
                raise TypeError("les element du tuple doivent etre de type entier")
            if value not in self.__possibiliter:
                if not remove:
                    self.__possibiliter.append(value)
            else:
                if remove:
                    self.__possibiliter.remove(value)

    def est_une_possibiliter(self, x, y):
        if self.type == TypeEntiter.VIDE:
            return False
        if type(x) is not int or type(y) is not int:
            raise TypeError("les coordoner doivent etre de type entier")
        return (x, y) in self.__possibiliter

    @property
    def type(self):
        return self.__type

    @property
    def adversaire(self):
        return self.__adversaire

    @adversaire.setter
    def adversaire(self, value):
        if not isinstance(value, Entiter):
            raise TypeError("un adversaire est une entiter")
        if value.type != TypeEntiter.JOUEUR_UN and value.type != TypeEntiter.JOUEUR_DEUX:
            raise ValueError("un adversaire est un Joueur")

        self.__adversaire = value

    def jouer(self, event, plateau, type):
        if self.type == TypeEntiter.VIDE and self.__type != type:
            return -1, -1
        return 0, 0

    @property
    def gain(self):
        return self.__gain

    @gain.setter
    def gain(self, value):
        self.__gain = value


class Humain(Entiter):

    def __init__(self, type_e, recurs=True):
        Entiter.__init__(self, type_e, recurs)

    def jouer(self, event, plateau, type):
        x, y = Entiter.jouer(self, event, plateau, type)

        if (x, y) == (-1, -1):
            return x, y


class Ordinateur(Entiter):

    def __init__(self, profonteur, algo_data, class_algo, type_e, recurs=True):
        Entiter.__init__(self, type_e, recurs)

        self.profondeur = profonteur
        self.algorithme = algo_data
        self.class_algo = class_algo

    def jouer(self, event, plateau, type):
        x, y = Entiter.jouer(self, event, plateau, type)

        if (x, y) == -1:
            return x, y

        return self.class_algo.decision_algo(self, plateau, self.algorithme, self.profondeur)
