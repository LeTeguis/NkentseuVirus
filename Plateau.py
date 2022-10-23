#!/usr/bin/python3

from Entiter import TypeEntiter, Entiter
import copy

class Plateau:

    def __init__(self, nbr_colone=7, nbr_ligne=7):
        if type(nbr_ligne) is not int or type(nbr_colone) is not int:
            raise TypeError("le nombre de ligne et de colone est de type entier")
        if nbr_colone < 5 or nbr_ligne < 5:
            raise ValueError("le nombre de ligne et le nombre de colone doit etre supérieur a 4")

        self.__joueur_un = Entiter(TypeEntiter.JOUEUR_UN)
        self.__joueur_deux = self.__joueur_un.adversaire

        self.__ligne = nbr_ligne
        self.__colone = nbr_colone
        self.__grille = [[TypeEntiter.VIDE for i in range(self.__ligne)] for j in range(self.__colone)]

        self.__init_joueur_un()
        self.__init_joueur_deux()

        self.__tmp_gain = []

    def remove_tmp_gain(self):
        if len(self.__tmp_gain) <= 0:
            return None
        e = self.__tmp_gain[0]
        self.__tmp_gain.remove(e)
        #del self.__tmp_gain[0]
        return e

    def copy(self):
        plateau = Plateau(self.__colone, self.__ligne)
        plateau.__grille.clear()
        plateau.__grille = [[self.__grille[i][j] for j in range(self.__ligne)] for i in range(self.colone)]
        #plateau.__grille = copy.deepcopy(self.__grille)
        plateau.__joueur_un = self.__joueur_un.copy()
        plateau.__joueur_deux = self.__joueur_deux.copy()
        plateau.__joueur_un.adversaire = plateau.__joueur_deux
        plateau.__joueur_deux.adversaire = plateau.__joueur_un

        return plateau
    def init_game(self):
        self.__grille = [[TypeEntiter.VIDE for i in range(self.__ligne)] for j in range(self.__colone)]

        self.__init_joueur_un()
        self.__init_joueur_deux()

        self.__tmp_gain.clear()

    def __init_joueur_un(self):
        # les pions du joueur 1
        self.__grille[0][0] = self.__joueur_un.type
        self.__grille[self.__colone - 1][self.__ligne - 1] = self.__joueur_un.type
        self.__joueur_un.taille = 2

        # possibiliter joueur 1
        self.__joueur_un.possibiliter.clear()
        self.__joueur_un.possibiliter = [(0, 1), (1, 1), (1, 0), (self.colone - 1, self.ligne - 2),
                                         (self.colone - 2, self.ligne - 2), (self.colone - 2, self.ligne - 1)]

    def __init_joueur_deux(self):
        # les pions du joueur 2
        self.__grille[self.__colone - 1][0] = self.__joueur_deux.type
        self.__grille[0][self.__ligne - 1] = self.__joueur_deux.type
        self.__joueur_deux.taille = 2

        # possibiliter joueur 2
        self.__joueur_deux.possibiliter.clear()
        self.__joueur_deux.possibiliter = [(0, self.ligne - 2), (1, self.ligne - 2), (1, self.ligne - 1),
                                           (self.colone - 2, 0), (self.colone - 2, 1), (self.colone - 1, 1)]

    def logics(self, joueur, x, y):
        if not isinstance(joueur, Entiter):
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

    def get_possibiliter(self, joueur, gain_):
        if not isinstance(joueur, Entiter):
            raise TypeError("le joueur doit etre de type Entiter")
        if joueur.type != TypeEntiter.JOUEUR_UN and joueur.type != TypeEntiter.JOUEUR_DEUX:
            raise ValueError("le joueur doit etre sois JOUEUR_UN sois JOUEUR_DEUX")
        if type(gain_) is not list:
            raise TypeError("le gain est une liste")
        add_ = []
        aremove_ = []
        for g in gain_:
            if type(g) is not tuple:
                raise TypeError("un element de gain est un tuple")
            if type(g[0]) is not int or type(g[1]) is not int:
                raise TypeError("un element de gain est un tuple d'entier")
            aremove_.append(g)
            for i in [-1, 0, 1]:
                if 0 <= g[0] + i < self.colone:
                    for j in [-1, 0, 1]:
                        if 0 <= g[1] + j < self.ligne:
                            if self.__grille[g[0] + i][g[1] + j] == TypeEntiter.VIDE:
                                add_.append((g[0] + i, g[1] + j))
        for a in add_:
            r_it = True
            for i in [-1, 0, 1]:
                if 0 <= a[0] + i < self.colone:
                    for j in [-1, 0, 1]:
                        if 0 <= a[1] + j < self.ligne:
                            if self.__grille[a[0] + i][a[1] + j] == joueur.adversaire.type:
                                r_it = False
                                break
                    if not r_it:
                        break
            if r_it:
                aremove_.append(a)
        return add_, gain_, aremove_

    def jouer(self, joueur, x, y):
        if len(self.__tmp_gain) <= 0:
            self.__tmp_gain = self.get_gain(joueur, x, y)

        if len(self.__tmp_gain) <= 0:
            return False, False
        e = self.remove_tmp_gain()
        self.__grille[e[0]][e[1]] = joueur.type
        add_j, rm_j, rm_a = self.get_possibiliter(joueur, [e])
        joueur.possibiliter = add_j
        joueur.remove_possibiliter(rm_j)
        joueur.taille += 1
        joueur.adversaire.remove_possibiliter(rm_j)
        joueur.adversaire.remove_possibiliter(rm_a)
        if len(self.__tmp_gain) > 0:
            joueur.adversaire.taille -= 1
            return True, False
        return True, True

    def simulate(self, joueur, x, y):
        _gain = self.get_gain(joueur, x, y)

        if len(_gain) <= 0:
            return False
        joueur.gain = _gain
        for e in _gain:
            self.__grille[e[0]][e[1]] = joueur.type
        add_j, rm_j, rm_a = self.get_possibiliter(joueur, _gain)
        joueur.possibiliter = add_j
        joueur.remove_possibiliter(rm_j)
        joueur.taille += len(_gain)
        joueur.adversaire.remove_possibiliter(rm_j)
        joueur.adversaire.remove_possibiliter(rm_a)
        joueur.adversaire.taille -= len(_gain) - 1
        return True

    def vider(self, joueur):
        fini, remplacer = self.jouer(joueur, -1, -1)
        while fini or remplacer:
            fini, remplacer = self.jouer(joueur, -1, -1)

    def match_terminer(self):
        return len(self.__joueur_un.possibiliter) <= 0 or len(
            self.__joueur_deux.possibiliter) <= 0 or not self.peut_bouffer(self.__joueur_un)

    def peut_bouffer(self, joueur):
        cp_g = copy.deepcopy(self.__grille)

        for (i, j) in joueur.possibiliter:
            if self.__recursion_peut_bouffer(joueur.type, i, j, cp_g, self.__colone, self.__ligne):
                return True
        return False

    def __recursion_peut_bouffer(self, type_, i, j, g, c, l):
        if 0 <= i < c and 0 <= j < l:
            if g[i][j] != TypeEntiter.VIDE and g[i][j] != type_:
                return True
            if g[i][j] == TypeEntiter.VIDE:
                g[i][j] = type_
                for ii in [-1, 0, 1]:
                    for jj in [-1, 0, 1]:
                        if (ii, jj) != (0, 0) and self.__recursion_peut_bouffer(type_, i + ii, j + jj, g, c, l):
                            return True
        return False

    def avantage(self):
        if self.__joueur_un.taille < self.__joueur_deux.taille:
            return self.__joueur_deux
        if self.__joueur_un.taille > self.__joueur_deux.taille:
            return self.__joueur_un
        if len(self.__joueur_un.possibiliter) < len(self.__joueur_deux.possibiliter):
            return self.__joueur_deux
        if len(self.__joueur_un.possibiliter) > len(self.__joueur_deux.possibiliter):
            return self.__joueur_un
        return Entiter(TypeEntiter.VIDE)

    def gagant(self):
        if self.match_terminer():
            return self.avantage()
        return Entiter(TypeEntiter.VIDE)

    @property
    def joueur_un(self):
        return self.__joueur_un

    @property
    def joueur_deux(self):
        return self.__joueur_deux

    @joueur_un.setter
    def joueur_un(self, value):
        if not isinstance(value, Entiter):
            raise TypeError("un adversaire est une entiter")
        if value.type != TypeEntiter.JOUEUR_UN and value.type != TypeEntiter.JOUEUR_DEUX:
            raise ValueError("un adversaire est un Joueur")

        self.__joueur_un = value

    @joueur_deux.setter
    def joueur_deux(self, value):
        if not isinstance(value, Entiter):
            raise TypeError("un adversaire est une entiter")
        if value.type != TypeEntiter.JOUEUR_UN and value.type != TypeEntiter.JOUEUR_DEUX:
            raise ValueError("un adversaire est un Joueur")

        self.__joueur_deux = value

    @property
    def ligne(self):
        return self.__ligne

    @property
    def colone(self):
        return self.__colone

    @property
    def grille(self):
        return self.__grille.copy()

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