#!/usr/bin/python3
from Entiter import TypeEntiter


class AlgoBase:

    def __init__(self):
        self.algos = {}
        self.nom = ""

    def decision_algo(self, joueur, copy_jeu, algo, profondeur):
        if algo not in self.algos and profondeur < 0 and joueur.type == TypeEntiter.VIDE:
            return -1, -1
        return 0, 0

    def infini(self):
        pass

    def add_algo(self, nom, algo):
        self.algos[nom] = algo

    def list_algo(self):
        liste = []
        for key in self.algos:
            liste.append(key)
        return liste