# -*- encoding: utf-8 -*-

WIDTH_SCREEN = 1088
HEIGHT_SCREEN = 608
PLAYER_SIZE = 31
TILE_SIZE = 32
MAX_HEALTH = 3
NUMBER_LEVELS = 4

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplementedError("Tiene que implementar el metodo update.")

    def events(self, *args):
        raise NotImplementedError("Tiene que implementar el metodo eventos.")

    def paint(self, pantalla):
        raise NotImplementedError("Tiene que implementar el metodo dibujar.")
