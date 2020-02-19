# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *

# SETTINGS
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Movimientos
IDLE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

#Posturas
SPRITE_IDLE = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2


# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

if __name__ == '__main__':

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Creamos la fase
    fase = Fase()


    # El bucle de eventos
    while True:

        # Sincronizar el juego a 60 fps
        tiempo_pasado = reloj.tick(60)

        # Coge la lista de eventos y se la pasa a la escena
        # Devuelve si se debe parar o no el juego
        if (fase.eventos(pygame.event.get())):
            pygame.quit()
            sys.exit()

        # Actualiza la escena
        # Devuelve si se debe parar o no el juego
        if (fase.update(tiempo_pasado)):
            pygame.quit()
            sys.exit()

        # Se dibuja en pantalla
        fase.dibujar(pantalla)
        pygame.display.flip()