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

        self.__init_joueur_un()
        self.__init_joueur_deux()

    def __init_joueur_un(self):
        # les pions du joueur 1
        self.__grille[0][0] = self.__joueur_un.type
        self.__grille[self.__colone - 1][self.__ligne - 1] = self.__joueur_un.type
        self.__joueur_un.taille = 2

        # possibiliter joueur 1
        self.__joueur_un.possibiliter = [(0, 1), (1, 1), (1, 0), (self.colone - 1, self.ligne - 2),
                                         (self.colone - 2, self.ligne - 2), (self.colone - 2, self.ligne - 1)]

    def __init_joueur_deux(self):
        # les pions du joueur 2
        self.__grille[self.__colone - 1][0] = self.__joueur_deux.type
        self.__grille[0][self.__ligne - 1] = self.__joueur_deux.type
        self.__joueur_deux.taille = 2

        # possibiliter joueur 2
        self.__joueur_deux.possibiliter = [(0, self.ligne - 2), (1, self.ligne - 2), (1, self.ligne - 1),
                                           (self.colone - 2, 0), (self.colone - 2, 1), (self.colone - 1, 1)]

    def logics(self, joueur, x, y):
        if type(joueur) is not Entiter:
            raise TypeError("le joueur doit etre de type Entiter")
        if joueur.type != TypeEntiter.JOUEUR_UN and joueur.type != TypeEntiter.JOUEUR_DEUX:
            raise ValueError("le joueur doit etre sois JOUEUR_UN sois JOUEUR_DEUX")
        if type(x) is not int or type(y) is not int:
            raise TypeError("les coordoner doivent etre de type entier")
        return joueur.est_une_possibiliter(x, y)

    def get_gain(self, joueur, x, y):
        gain_ = []
        if self.logics(joueur, x, y):
            gain_.append((x, y))
            for i in [-1, 0, 1]:
                if 0 <= x + i < self.colone:
                    for j in [-1, 0, 1]:
                        if 0 <= y + j < self.ligne:
                            if self.__grille[x + i][y + j] == joueur.adversaire.type:
                                gain_.append((x + i, y + j))
        return gain_

    @property
    def joueur_un(self):
        return self.__joueur_un

    @property
    def joueur_deux(self):
        return self.__joueur_deux

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