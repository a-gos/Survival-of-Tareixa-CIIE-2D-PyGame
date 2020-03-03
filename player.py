# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from resourcesmanager import ResourcesManager


# MOVEMENT
IDLE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4

# ANIMATIONS
SPRITE_IDLE = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2


# PLAYER SETTINGS
PLAYER_SPEED = 0.2 # Pixeles per milisecond
PLAYER_JUMP_SPEED = 0.3 # Pixeles per milisecond
PLAYER_ANIMATION_DELAY = 5 # updates that the character model will endure
                              # should be a different number for each animation

GRAVITY = 0.0003

# -------------------------------------------------
#
# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))



# -------------------------------------------------

class Player(pygame.sprite.Sprite):
    "Player"

    def __init__(self):
        # Primero invocamos al constructor de la clase padre
        pygame.sprite.Sprite.__init__(self);
        # Se carga la hoja
        self.hoja = ResourcesManager.CargarImagen('Tareixa.png',-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = IDLE
        # Lado hacia el que esta mirando
        self.mirando = LEFT

        # Leemos las coordenadas de un archivo de texto
        datos = ResourcesManager.CargarArchivoCoordenadas('coordTareixa.txt')
        datos = datos.split()
        self.animationNumber = 1;
        self.numImagenPostura = 0;
        cont = 0;
        numImagenes = [6, 12, 6]        
        self.coordenadasHoja = [];
        for linea in range(0, 3):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for animation in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que animation esta inicialmente
        self.animationNumber = IDLE

        # La posicion inicial del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.animationNumber][self.numImagenPostura][2],self.coordenadasHoja[self.animationNumber][self.numImagenPostura][3])

        # La posicion x e y que ocupa
        self.posicionx = 300
        self.posiciony = 300
        self.rect.left = self.posicionx
        self.rect.bottom = self.posiciony
        # Velocidad en el eje y (para los saltos)
        #  En el eje x se utilizaria si hubiese algun tipo de inercia
        self.velocidady = 0

        # Y actualizamos la animation del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()



    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva animation
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = PLAYER_ANIMATION_DELAY
            # Si ha pasado, actualizamos la animation
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.animationNumber]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.animationNumber])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.animationNumber][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.mirando == RIGHT:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.animationNumber][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.mirando == LEFT:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.animationNumber][self.numImagenPostura]), 1, 0)



    def mover(self,teclasPulsadas, arriba, abajo, izquierda, derecha):

        # Indicamos la acción a realizar segun la tecla pulsada para el Player
        if teclasPulsadas[arriba]:
            # Si estamos en el aire y han pulsado arriba, ignoramos este movimiento
            if self.animationNumber == SPRITE_JUMPING:
                self.movimiento = IDLE
            else:
                self.movimiento = UP
        elif teclasPulsadas[izquierda]:
            self.movimiento = LEFT
        elif teclasPulsadas[derecha]:
            self.movimiento = RIGHT
        else:
            self.movimiento = IDLE




    def update(self, tiempo):
        # Si vamos a la izquierda
        if self.movimiento == LEFT:
            # Si no estamos en el aire, la animation actual sera estar caminando
            if not self.animationNumber == SPRITE_JUMPING:
                self.animationNumber = SPRITE_WALKING
            # Esta mirando a la izquierda
            self.mirando = LEFT
            # Actualizamos la posicion
            self.posicionx -= PLAYER_SPEED * tiempo
            self.rect.left = self.posicionx
        # Si vamos a la derecha
        elif self.movimiento == RIGHT:
            # Si no estamos en el aire, la animation actual sera estar caminando
            if not self.animationNumber == SPRITE_JUMPING:
                self.animationNumber = SPRITE_WALKING
            # Esta mirando a la derecha
            self.mirando = RIGHT
            # Actualizamos la posicion
            self.posicionx += PLAYER_SPEED * tiempo
            self.rect.left = self.posicionx
        # Si estamos saltando
        elif self.movimiento == UP:
            # La animation actual sera estar saltando
            self.animationNumber = SPRITE_JUMPING
            # Le imprimimos una velocidad en el eje y
            self.velocidady = PLAYER_JUMP_SPEED
        # Si no se ha pulsado ninguna tecla
        elif self.movimiento == IDLE:
            # Si no estamos saltando, la animation actual será estar quieto
            if not self.animationNumber == SPRITE_JUMPING:
                self.animationNumber = SPRITE_IDLE

        # Si estamos en el aire
        if self.animationNumber == SPRITE_JUMPING:
            # Actualizamos la posicion
            self.posiciony -= self.velocidady * tiempo
            # Si llegamos a la posicion inferior, paramos de caer y lo ponemos como quieto
            if (self.posiciony>300):
                self.animationNumber = SPRITE_IDLE
                self.posiciony = 300
                self.velovidady = 0
            # Si no, aplicamos el efecto de la gravedad
            else:
                self.velocidady -= 0.004
            # Nos ponemos en esa posicion en el eje y
            self.rect.bottom = self.posiciony

        # Actualizamos la imagen a mostrar
        self.actualizarPostura()
        return
        