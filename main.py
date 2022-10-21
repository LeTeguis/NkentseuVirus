#!/usr/bin/python3

from Plateau import Plateau

if __name__ == "__main__":
    running = True

    plateau = Plateau()

    while running:
        print(plateau)
        print(plateau.joueur_un.possibiliter)
        print(plateau.joueur_deux.possibiliter)
        x = input()