#!/usr/bin/python3
from enum import Enum


class TypeEntiter(Enum):
    JOUEUR_UN = 1
    JOUEUR_DEUX = 2
    VIDE = 0

    def __str__(self):
        return f"{self.value}"

class Entiter:
    __type = TypeEntiter.VIDE
    __adversaire = None

    def __init__(self, type_e, recurs=True):
        if type(type_e) is not TypeEntiter:
            raise TypeError("type_e doit etre de type TypeEntiter")
        self.__type = type_e
        if type_e == TypeEntiter.JOUEUR_UN and recurs:
            self.__adversaire = Entiter(TypeEntiter.JOUEUR_DEUX, False)
            self.__adversaire.__adversaire = self
        if type_e == TypeEntiter.JOUEUR_DEUX and recurs:
            self.__adversaire = Entiter(TypeEntiter.JOUEUR_UN, False)
            self.__adversaire.__adversaire = self

    @property
    def type(self):
        return self.__type

    @property
    def adversaire(self):
        return self.__adversaire