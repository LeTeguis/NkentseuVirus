#!/usr/bin/python3

from Entiter import TypeEntiter, Entiter

class Plateau:

    __ligne = 7
    __colone = 7
    __grille = []

    __joueur_un = Entiter(TypeEntiter.JOUEUR_UN)
    __joueur_deux = __joueur_un.adversaire

    def __init__(self, nbr_colone=7, nbr_ligne=7):
        if type(nbr_ligne) is not int or type(nbr_colone) is not int:
            raise TypeError("le nombre de ligne et de colone est de type entier")
        if nbr_colone < 5 or nbr_ligne < 5:
            raise ValueError("le nombre de ligne et le nombre de colone doit etre supérieur a 4")
        self.__ligne = nbr_ligne
        self.__colone = nbr_colone
        self.__grille = [[TypeEntiter.VIDE for i in range(self.__ligne)] for j in range(self.__colone)]
        self.__grille[0][0] = self.__joueur_un.type
        self.__grille[self.__colone - 1][self.__ligne - 1] = self.__joueur_un.type
        self.__grille[self.__colone - 1][0] = self.__joueur_deux.type
        self.__grille[0][self.__ligne - 1] = self.__joueur_deux.type

    @property
    def ligne(self):
        return self.__ligne

    @property
    def colone(self):
        return self.__colone

    def __str__(self):
        str_g = ""
        for i in range(self.__ligne):
            for j in range(self.__colone):
                if j == 0:
                    str_g += f"[ {self.__grille[j][i].value} "
                elif j == self.__colone - 1:
                    str_g += f"| {self.__grille[j][i].value} ]"
                else:
                    str_g += f"| {self.__grille[j][i].value} "
            str_g += "\n"
        return str_g