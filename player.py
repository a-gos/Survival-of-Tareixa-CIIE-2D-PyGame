# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame
import sys
import os
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


# Character SETTINGS
Character_SPEED = 0.2  # Pixeles per milisecond
Character_JUMP_SPEED = 0.3  # Pixeles per milisecond
Character_ANIMATION_DELAY = 5  # updates that the character model will endure
                            # should be a different number for each animation

GRAVITY = 0.0005

# -------------------------------------------------
#
# -------------------------------------------------
# Clase MySprite


class MySprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)
        self.speed = (0, 0)
        self.scroll = (0, 0)

    def setposition(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    def setpositionscreen(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.position
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def increaseposition(self, incremento):
        (posx, posy) = self.position
        (incrementox, incrementoy) = incremento
        self.setposition((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.speed[0]*tiempo
        incrementoy = self.speed[1]*tiempo
        self.increaseposition((incrementox, incrementoy))


# -------------------------------------------------

class Character(MySprite):
    "Character Principal"

    def __init__(self, imageFile, coordFile, numImages, runSpeed, jumpSpeed, animationDelay):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)
        # Se carga la hoja
        self.hoja = ResourcesManager.LoadImage(imageFile, -1)
        self.hoja = self.hoja.convert_alpha()
        # El movement que esta realizando
        self.movement = IDLE
        # Lado hacia el que esta looking
        self.looking = LEFT

        # Leemos las coordenadas de un archivo de texto
        data = ResourcesManager.LoadCoordFile(coordFile)
        data = data.split()
        self.animationNumber = 1
        self.numImagenPostura = 0
        cont = 0

        self.coordenadasHoja = []
        for linea in range(0, 3):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for animation in range(1, numImages[linea]+1):
                tmp.append(pygame.Rect((int(data[cont]), int(
                    data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.movementDelay = 0

        # En que animation esta inicialmente
        self.animationNumber = IDLE

        # La position inicial del Sprite
        self.rect = pygame.Rect(100, 100, self.coordenadasHoja[self.animationNumber][self.numImagenPostura]
                                [2], self.coordenadasHoja[self.animationNumber][self.numImagenPostura][3])

        # La position x e y que ocupa
        self.runSpeed = runSpeed
        self.jumpSpeed = jumpSpeed

        # speed en el eje y (para los saltos)
        #  En el eje x se utilizaria si hubiese algun tipo de inercia
        self.animationDelay = animationDelay

        # Y actualizamos la animation del Sprite inicial, llamando al metodo correspondiente
        self.updatePosture()

    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, move):
        if move == UP:
            # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
            if self.animationNumber == SPRITE_JUMPING:
                self.movement = IDLE
            else:
                self.movement = UP
        else:
            self.movement = move


    def updatePosture(self):
        self.movementDelay -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva animation
        if (self.movementDelay < 0):
            self.movementDelay = self.animationDelay
            # Si ha pasado, actualizamos la animation
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.animationNumber]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(
                    self.coordenadasHoja[self.animationNumber])-1
            self.image = self.hoja.subsurface(
                self.coordenadasHoja[self.animationNumber][self.numImagenPostura])

            # Si esta looking a la izquiera, cogemos la porcion de la hoja
            if self.looking == RIGHT:
                self.image = self.hoja.subsurface(
                    self.coordenadasHoja[self.animationNumber][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.looking == LEFT:
                self.image = pygame.transform.flip(self.hoja.subsurface(
                    self.coordenadasHoja[self.animationNumber][self.numImagenPostura]), 1, 0)

    def update(self, platformGroup, tiempo):

        (speedx, speedy) = self.speed

        # Si vamos a la izquierda o derecha
        if (self.movement == LEFT) or (self.movement == RIGHT):
          # Si no estamos en el aire, la animation actual sera estar caminando
            self.looking = self.movement
           # Esta looking a la izquierda
            if self.movement == LEFT:
              speedx = -self.runSpeed
            # este looking derecha
            else:
                speedx = self.runSpeed
        # Si no saltamos
            if self.animationNumber != SPRITE_JUMPING:
          # walking
                self.animationNumber = SPRITE_WALKING
           # esto non sei que fai a vdd
                if pygame.sprite.spritecollideany(self, platformGroup) == None:
                  self.animationNumber = SPRITE_JUMPING
        # Si estamos saltando
        elif self.movement == UP:
            # La animation actual sera estar saltando
            self.animationNumber = SPRITE_JUMPING
            # Le imprimimos una speed en el eje y
            speedy = -self.jumpSpeed
        # Si no se ha pulsado ninguna tecla
        elif self.movement == IDLE:
            # Si no estamos saltando, la animation actual será estar quieto
            if not self.animationNumber == SPRITE_JUMPING:
                self.animationNumber = SPRITE_IDLE
            speedx = 0

        # Si estamos en el aire
        if self.animationNumber == SPRITE_JUMPING:
           # Miramos a ver si hay que parar de caer: si hemos llegado a una platform
            #  Para ello, miramos si hay colision con alguna platform del grupo
            platform = pygame.sprite.spritecollideany(self, platformGroup)
            #  Ademas, esa colision solo nos interesa cuando estamos cayendo
            #  y solo es efectiva cuando caemos encima, no de lado, es decir,
            #  cuando nuestra position inferior esta por encima de la parte de abajo de la platform
            if (platform != None) and (speedy > 0) and (platform.rect.bottom>self.rect.bottom):
                # Lo situamos con la parte de abajo un pixel colisionando con la platform
                #  para poder detectar cuando se cae de ella
                self.setposition(
                    (self.position[0], platform.position[1]-platform.rect.height+1))
                # Lo ponemos como quieto
                self.animationNumber = SPRITE_IDLE
                # Y estará quieto en el eje y
                speedy = 0

            # Si no caemos en una platform, aplicamos el efecto de la gravedad
            else:
                speedy +=GRAVITY * tiempo

        # Actualizamos la imagen a mostrar
        self.updatePosture()

        self.speed = (speedx, speedy)

        MySprite.update(self,tiempo)
        return


# -------------------------------------------------
# Clase Player

class Player(Character):
    "Cualquier Character del juego"

    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este Character concreto (jugador 1 en este caso)
        Character.__init__(self, 'Tareixav2.png', 'coordTareixa.txt', [4, 12, 1],Character_SPEED, Character_JUMP_SPEED, Character_ANIMATION_DELAY);


    def mover(self, pressedKeys, arriba, abajo, izquierda, derecha):
        # Indicamos la acción a realizar segun la tecla pulsada para el Character
        if pressedKeys[arriba]:
            Character.mover(self, UP)
        elif pressedKeys[izquierda]:
            Character.mover(self, LEFT)
        elif pressedKeys[derecha]:
            Character.mover(self, RIGHT)
        else:
            Character.mover(self, IDLE)


# -------------------------------------------------
# Clase NPC

class NPC(Character):
    "El resto de Characters no jugadores"

    def __init__(self, imageFile, coordFile, numImagenes, speed, jumpSeed, animationDelay):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Character.__init__(self, imageFile, coordFile,
                           numImages, speed, jumpSeed, animationDelay)

    # Aqui vendria la implementacion de la IA segun las positiones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def move_cpu(self, player1):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return
