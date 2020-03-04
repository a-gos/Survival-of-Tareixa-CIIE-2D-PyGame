# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from player import Player
from fase import Fase

# SETTINGS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Importar modulos
import pygame
import director
from director import *


# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():

    # Inicializar pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    fase = Fase(director)
    # Le decimos al director que apile esta escena
    director.stackscene(fase)
    # Y ejecutamos el juego
    director.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
