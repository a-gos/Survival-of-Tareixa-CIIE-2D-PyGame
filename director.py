# -*- encoding: utf-8 -*-

# Modulos
import pygame
import sys
#import scene
from scene import *
from pygame.locals import *



class Director():

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        self.screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
        pygame.display.set_caption("Survival of Tareixa")
        # Pila de scenes
        self.stack = []
        # Flag que nos indica cuando quieren salir de la scene
        self.exit_scene = False
        # Reloj
        self.clock = pygame.time.Clock()
        # Fase/nivel del juego que se está ejecutando
        self.game_level = 1

    def loop(self, scene):

        self.exit_scene = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada scene
        while not self.exit_scene:

            # Sincronizar el juego a 60 fps
            elapsed_time = self.clock.tick(60)
            
            # Pasamos los eventos a la scene
            scene.events(pygame.event.get())

            # Actualiza la scene
            scene.update(elapsed_time)

            # Se dibuja en pantalla
            scene.paint(self.screen)
            pygame.display.flip()


    def execute(self):

        # Mientras haya scenes en la pila, ejecutaremos la de arriba
        while (len(self.stack)>0):

            # Se coge la scene a ejecutar como la que este en la cima de la pila
            scene = self.stack[len(self.stack)-1]

            # Ejecutamos el bucle de eventos hasta que termine la scene
            self.loop(scene)


    def exitScene(self):
        # Indicamos en el flag que se quiere salir de la scene
        self.exit_scene = True
        # Eliminamos la scene actual de la pila (si la hay)
        if (len(self.stack)>0):
            self.stack.pop()

    def exitProgram(self):
        # Vaciamos la lista de scenes pendientes
        self.stack = []
        self.exit_scene = True

    def changeScene(self, scene):
        self.exitScene()
        # Ponemos la scene pasada en la cima de la pila
        self.stack.append(scene)

    def stackScene(self, scene):
        self.exit_scene = True
        # Ponemos la scene pasada en la cima de la pila
        #  (por encima de la actual)
        self.stack.append(scene)

