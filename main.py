# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from player import Player
from fase import Fase
import director
from director import *
from menu import Menu

# Si se pone a True, se cargará directamente la fase indicada en DEBUG_FASE,
# sin necesidad de acceder a través del menú
DEBUG = True
DEBUG_FASE_NUM = 1

if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()

    if DEBUG:
        # Creamos la escena con el nivel a depurar
        scene = Fase(director, DEBUG_FASE_NUM)
    else:
        # Creamos la escena con el menú principal
        scene = Menu(director)

    # Le decimos al director que apile esta escena
    director.stackscene(scene)
    # Y ejecutamos el juego
    director.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
