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
        if algo == "mini":
            return self.decision_mini(joueur, copy_jeu, algo, profondeur)

        return self.auther_decision(joueur, copy_jeu, algo, profondeur)

    def decision_mini(self, joueur, copy_jeu, algo, profondeur):
        x, y = AlgoBase.decision_algo(self, joueur, copy_jeu, algo, profondeur)
        if (x, y) == (-1, -1):
            return -1, -1

        eval = self.infini()
        pos = (-1, -1)
        for (i, j) in joueur.possibiliter:
            e = self.algos[algo](joueur, copy_jeu, i, j, profondeur)

            if eval > e or (eval == e and random.randint(1, 2) == 1):
                eval = e
                pos = (i, j)

        return pos[0], pos[1]

    def auther_decision(self, joueur, copy_jeu, algo, profondeur):
        x, y = AlgoBase.decision_algo(self, joueur, copy_jeu, algo, profondeur)
        if (x, y) == (-1, -1):
            return -1, -1

        eval = -self.infini()
        pos = (-1, -1)
        for (i, j) in joueur.possibiliter:
            e = self.algos[algo](joueur, copy_jeu, i, j, profondeur)

            if eval < e or (eval == e and random.randint(1, 2) == 1):
                eval = e
                pos = (i, j)

        return pos[0], pos[1]

    def mini(self, joueur, plateau, i, j, profondeur):
        if profondeur <= 0 or not plateau.logics(joueur, i, j) or plateau.match_terminer():
            return self.evaluation(joueur, plateau, i, j, profondeur)

        mini_ = self.infini()
        p_copy = plateau.copy()
        n_j = p_copy.joueur_deux if joueur.type == p_copy.joueur_un.type else p_copy.joueur_un

        if p_copy.simulate(n_j, i, j):
            for (i_, j_) in n_j.possibiliter:
                e = self.maxi(n_j, p_copy, i_, j_, profondeur - 1)
                if mini_ > e or (mini_ == e and random.randint(1, 2) == 1):
                    mini_ = e
        return mini_

    def maxi(self, joueur, plateau, i, j, profondeur):
        if profondeur <= 0 or not plateau.logics(joueur, i, j) or plateau.match_terminer():
            return self.evaluation(joueur, plateau, i, j, profondeur)

        maxi_ = -self.infini()
        p_copy = plateau.copy()
        n_j = p_copy.joueur_deux if joueur.type == p_copy.joueur_un.type else p_copy.joueur_un

        if p_copy.simulate(n_j, i, j):
            for (i_, j_) in n_j.possibiliter:
                e = self.maxi(n_j, p_copy, i_, j_, profondeur - 1)
                if maxi_ < e or (maxi_ == e and random.randint(1, 2) == 1):
                    maxi_ = e
        return maxi_

    def minimax(self, joueur, plateau, i, j, profondeur, maximiser=False):
        if profondeur <= 0 or not plateau.logics(joueur, i, j) or plateau.match_terminer():
            return self.evaluation(joueur, plateau, i, j, profondeur)

        eval_actuel = -self.infini() if maximiser else self.infini()
        p_copy = plateau.copy()
        n_j = p_copy.joueur_deux if joueur.type == p_copy.joueur_un.type else p_copy.joueur_un

        if p_copy.simulate(n_j, i, j):
            for (i_, j_) in n_j.possibiliter:
                e = self.minimax(n_j, p_copy, i_, j_, profondeur - 1, not maximiser)
                if maximiser:
                    if eval_actuel < e or (eval_actuel == e and random.randint(1, 2) == 1):
                        eval_actuel = e
                else:
                    if eval_actuel > e or (eval_actuel == e and random.randint(1, 2) == 1):
                        eval_actuel = e
        return eval_actuel

    def nega_max(self):
        pass

    def alpha_betha(self):
        pass