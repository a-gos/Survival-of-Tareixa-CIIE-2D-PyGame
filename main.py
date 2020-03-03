# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from player import Player

# SETTINGS
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():

    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Ejemplo de uso de Sprites')

    # Creamos los jugadores
    player1 = Player()
    player2 = Player()

    # Creamos el grupo de Sprites de jugadores
    grupoJugadores = pygame.sprite.Group( player1, player2 )


    # El bucle de eventos
    while True:

        # Hacemos que el reloj espere a un determinado fps
        tiempo_pasado = reloj.tick(60)
        # Para cada evento, hacemos
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Miramos que teclas se han pulsado
        teclasPulsadas = pygame.key.get_pressed()

        # Si la tecla es Escape
        if teclasPulsadas[K_ESCAPE]:
            # Se sale del programa
            pygame.quit()
            sys.exit()


        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        player1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        player2.mover(teclasPulsadas, K_w,  K_s,    K_a,    K_d)



        # Actualizamos los jugadores actualizando el grupo
        grupoJugadores.update(tiempo_pasado)


        # Dibujar el fondo de color
        pantalla.fill((133,133,133))

        # Dibujar el grupo de Sprites
        grupoJugadores.draw(pantalla)
        
        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
