#!/usr/bin/python3
import random

from AlgoBase import AlgoBase


class FirstIA(AlgoBase):

    def __init__(self):
        AlgoBase.__init__(self)

        self.add_algo("mini", self.mini)
        self.add_algo("maxi", self.maxi)
        self.add_algo("minimax", self.minimax)
        self.add_algo("nega-max", self.nega_max)
        self.add_algo("alpha-betha", self.alpha_betha)

    def infini(self):
        return 100

    def evaluation(self, joueur, plateau, i, j, profondeur):
        '''
        :param joueur:
        :param plateau:
        :param i:
        :param j:
        :param profondeur:
        :return: x - y ou x est le nombre de pion du joueur actuel et y pour l'adversaire
        '''
        print(f"eval: {joueur.taille - joueur.adversaire.taille}")
        return joueur.taille - joueur.adversaire.taille

    def decision_algo(self, joueur, copy_jeu, algo, profondeur):
        x, y = AlgoBase.decision_algo(self, joueur, copy_jeu, algo, profondeur)
        if (x, y) == (-1, -1):
            return -1, -1

        eval = -self.infini()
        if algo == "mini":
            eval = self.infini()
        pos = (-1, -1)
        for (i, j) in joueur.possibiliter:
            e = self.algos[algo](joueur, copy_jeu, i, j, profondeur)

            if algo == "mini":
                if eval > e or (eval == e and random.randint(1, 2) == 1):
                    eval = e
                    pos = (i, j)
            else:
                if eval < e or (eval == e and random.randint(1, 2) == 1):
                    eval = e
                    pos = (i, j)

        return pos[0], pos[1]

    def mini(self, joueur, plateau, i, j, profondeur):
        print(f"profondeur: {profondeur} | joueur: {joueur.type.name} | ({i}, {j})")
        if profondeur <= 0 or not plateau.logics(joueur, i, j) or plateau.match_terminer():
            return self.evaluation(joueur, plateau, i, j, profondeur)

        mini = self.infini()
        p_copy = plateau.copy()
        n_j = None
        if joueur.type == p_copy.joueur_un.type:
            n_j = p_copy.joueur_deux
        else:
            n_j = p_copy.joueur_un
        if p_copy.jouer(n_j, i, j):
            p_copy.vider(joueur)

            for (i_, j_) in n_j.possibiliter:
                e = self.maxi(n_j, p_copy, i_, j_, profondeur - 1)
                if mini > e or (mini == e and random.randint(1, 2) == 1):
                    mini = e
        return mini

    def maxi(self, joueur, plateau, i, j, profondeur):
        print(f"profondeur: {profondeur} | joueur: {joueur.type.name} | ({i}, {j})")
        if profondeur <= 0 or not plateau.logics(joueur, i, j) or plateau.match_terminer():
            return self.evaluation(joueur, plateau, i, j, profondeur)

        maxi = -self.infini()
        p_copy = plateau.copy()
        if p_copy.jouer(joueur, i, j):
            n_j = None
            if joueur.type == p_copy.joueur_un.type:
                n_j = p_copy.joueur_deux
            else:
                n_j = p_copy.joueur_un

            for (i_, j_) in n_j.possibiliter:
                e = self.maxi(n_j, p_copy, i_, j_, profondeur - 1)
                if maxi < e or (maxi == e and random.randint(1, 2) == 1):
                    maxi = e
        return maxi

    def minimax(self):
        pass

    def nega_max(self):
        pass

    def alpha_betha(self):
        pass