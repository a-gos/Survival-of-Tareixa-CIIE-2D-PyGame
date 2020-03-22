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
from menu import *
from resourcesmanager import ResourcesManager

# Si se pone a True, se cargará directamente la fase indicada en DEBUG_FASE,
# sin necesidad de acceder a través del menú
DEBUG = False
DEBUG_FASE_NUM = 4
MUSIC_ON = False

if __name__ == '__main__':
    # Inicializamos el módulo para los sonidos y cargamos la música de fondo
    pygame.mixer.pre_init(44100, 16, 2, 512)
    pygame.mixer.init()
    # Inicializamos la libreria de pygame
    pygame.init()


    if MUSIC_ON:
        ResourcesManager.LoadMusic('background_music.ogg')
        # Reproducimos la música de forma que se repite continuamente
        pygame.mixer.music.play(-1)

    # Creamos el director
    director = Director()

    if DEBUG:
        # Creamos la escena con el nivel a depurar
        scene = Fase(director, DEBUG_FASE_NUM)
        director.game_level = DEBUG_FASE_NUM
    else:
        # Creamos la escena con el menú principal
        scene = MenuPrincipal(director)

    # Le decimos al director que apile esta escena
    director.stackScene(scene)
    # Y ejecutamos el juego
    director.execute()

    if MUSIC_ON:
        # Paramos la reproducción de música
        pygame.mixer.music.stop()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
