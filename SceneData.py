#!/usr/bin/python3

class SceneData:
    scene_info = {}
    left_corner = {}
    rigth_corner = {}

    @staticmethod
    def info():
        return SceneData.scene_info

    @staticmethod
    def add_info(nom, valeur):
        SceneData.scene_info[nom] = valeur

    @staticmethod
    def get_left_corner(data=None):
        if data is None or data not in SceneData.left_corner:
            return SceneData.left_corner
        return SceneData.left_corner[data]

    @staticmethod
    def add_in_left_corner(nom, valeur):
        SceneData.left_corner[nom] = valeur

    @staticmethod
    def get_rigth_corner(data=None):
        if data is None or data not in SceneData.rigth_corner:
            return SceneData.rigth_corner
        return SceneData.rigth_corner[data]

    @staticmethod
    def add_in_rigth_corner(nom, valeur):
        SceneData.rigth_corner[nom] = valeur