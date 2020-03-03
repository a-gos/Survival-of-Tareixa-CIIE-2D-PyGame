# -*- encoding: utf-8 -*-

WIDTH_SCREEN = 800
HEIGTH_SCREEN = 600

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplementedError("Tiene que implementar el metodo update.")

    def eventos(self, *args):
        raise NotImplementedError("Tiene que implementar el metodo eventos.")

    def dibujar(self, pantalla):
        raise NotImplementedError("Tiene que implementar el metodo dibujar.")
