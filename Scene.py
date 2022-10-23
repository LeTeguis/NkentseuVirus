#!/usr/bin/python3


class Scene:
    actual = None
    fenetre = None
    largeur = 640
    hauteur = 480
    list_scene = {}

    def __init__(self, fenetre, largeur=640, hauteur=480):
        Scene.fenetre = fenetre
        Scene.largeur = largeur
        Scene.hauteur = hauteur

    def initialiser(self):
        pass

    def draw(self):
        pass

    def update(self, temps):
        pass

    def event(self, event_):
        pass

    @staticmethod
    def get_scene(name):
        if name in Scene.list_scene:
            return Scene.list_scene[name]
        return None

    @staticmethod
    def add_scene(name, scene=None):
        if name not in Scene.list_scene:
            Scene.list_scene[name] = scene
        return Scene.list_scene[name]