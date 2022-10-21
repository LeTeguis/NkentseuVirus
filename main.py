#!/usr/bin/python3

from Plateau import Plateau

if __name__ == "__main__":
    running = True

    plateau = Plateau()
    joueur_actuel = plateau.joueur_un

    while running:
        print(plateau)
        print(f"{joueur_actuel.type.name}: A vous de jouer")
        x, y = -1, -1
        try:
            x = int(input("x = "))
            y = int(input("y = "))
        except TypeError as e:
            print(f"{joueur_actuel.type.name}: {e}")
            continue

        if plateau.jouer(joueur_actuel, x, y):
            print(f"{joueur_actuel.type.name}: Score")
            print(joueur_actuel.possibiliter)
            print(joueur_actuel.taille)
            joueur_actuel = joueur_actuel.adversaire
            print(f"{joueur_actuel.type.name}: Score")
            print(joueur_actuel.possibiliter)
            print(joueur_actuel.taille)
        else:
            print(f"{joueur_actuel.type.name}: votre jeu est incorrecte")