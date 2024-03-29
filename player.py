# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame
import sys
import os
from pygame.locals import *
from resourcesmanager import ResourcesManager
from scene import *
from utilities import *



# MOVEMENT
IDLE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
SHOOTING = 5
HURT = 6

# ANIMATIONS
SPRITE_IDLE = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2
SPRITE_SHOOTING = 3
SPRITE_DYING = 4
SPRITE_DYINGAIR = 5
SPRITE_KNOCKED = 6


# Character SETTINGS
Character_SPEED = 0.2  # Pixeles per milisecond
Character_JUMP_SPEED = 0.33  # Pixeles per milisecond
Character_ANIMATION_DELAY = 5  # updates that the character model will endure
                            # should be a different number for each animation
Character_INVULNERABILITY = 2000 # Número de milisegundos que el personaje 
                                #está sin recibir daño tras recibirlo una primera vez
Character_KNOCKDOWN = 300       # Tiempo que el personaje está volando por el golpe
GRAVITY = 0.0005

MAGAZINE_SIZE = 4
MAGAZINE_CD = 500
DMG_INIT = 0.5
SPEED_INIT = 0.5




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

    # Método para cambiar la posición global: cambia también la posición en
    # pantalla gracias a la copia del scroll
    def setposition(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    # Recibe un valor de scroll y cambia su valor en pantalla, pero no su
    # posición global en el entorno. Un cambio de pos. local NO implica un
    # cambio de pos. global
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
    "Cualquier personaje del juego"

    def __init__(self, imageFile, coordFile, numImages, runSpeed, jumpSpeed,
                 animationDelay, health):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)
        # Se carga la hoja
        self.hoja = ResourcesManager.LoadImageCharacter(imageFile, -1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movement = IDLE
        # Lado hacia el que esta mirando
        self.looking = LEFT

        self.isJumping = False
        self.isKnocked = False
        self.lastHit = pygame.time.get_ticks()
        self.cooldownHit = Character_INVULNERABILITY

        #cargamos el death sound
        self.deathSound = ResourcesManager.LoadSound(self.deathSound)
  

        # Leemos las coordenadas de un archivo de texto
        data = ResourcesManager.LoadCoordFileCharacter(coordFile)
        data = data.split()
        self.animationNumber = 1
        self.numImagenPostura = 0
        cont = 0

        self.coordenadasHoja = []
        for linea in range(0, 7):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for animation in range(1, numImages[linea]+1):
                tmp.append(pygame.Rect((int(data[cont]), int(
                    data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se
        # mueva demasiado rápido)
        self.movementDelay = 0

        # En que animacion esta inicialmente
        self.animationNumber = IDLE

        # La posicion inicial del Sprite
        self.rect = pygame.Rect(100, 100,
                                self.coordenadasHoja[self.animationNumber][self.numImagenPostura][2],
                                self.coordenadasHoja[self.animationNumber][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.runSpeed = runSpeed
        self.jumpSpeed = jumpSpeed

        # speed en el eje y (para los saltos)
        #  En el eje x se utilizaria si hubiese algun tipo de inercia
        self.animationDelay = animationDelay

        # Establecemos el nivel de vida inicial
        self.health = health

        # Y actualizamos la animacion del Sprite inicial, llamando al metodo
        # correspondiente
        self.updatePosture()

    # Metodo base para realizar el movimiento: simplemente se le indica cual
    # va a hacer, y lo almacena
    def mover(self, move):
        if not(self.isKnocked):
            if move == UP:
                # Si estamos en el aire y el personaje quiere saltar, ignoramos
                # este movimiento
                if self.animationNumber == SPRITE_JUMPING:
                    self.isJumping = True
                else:
                    self.movement = UP
            elif move == HURT:
                if self.animationNumber == SPRITE_KNOCKED:
                    self.isKnocked = True
                else:
                    self.movement = HURT
            else:
                self.movement = move


    def updatePosture(self):
        self.movementDelay -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva animacion
        if (self.movementDelay < 0):
            self.movementDelay = self.animationDelay
            # Si ha pasado, actualizamos la animacion
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.animationNumber]):
                self.numImagenPostura = 0
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(
                    self.coordenadasHoja[self.animationNumber])-1
            self.image = self.hoja.subsurface(
                self.coordenadasHoja[self.animationNumber][self.numImagenPostura])

            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            if self.looking == RIGHT:
                self.image = self.hoja.subsurface(
                    self.coordenadasHoja[self.animationNumber][self.numImagenPostura])
            #  Si no, si mira a la derecha, invertimos esa imagen
            elif self.looking == LEFT:
                self.image = pygame.transform.flip(self.hoja.subsurface(
                    self.coordenadasHoja[self.animationNumber][self.numImagenPostura]), 1, 0)

    def update(self, platformGroup, enemyGroup, tiempo):

        # Si el personaje ha caído al vacío
        if self.position[1] > HEIGHT_SCREEN:
            self.health = 0
            self.deathSound.play()
            self.kill()
            # print("Personaje muerto")

        # Si al personaje lo han matado
        elif self.health <= 0:
            self.deathSound.play()
            self.kill()
            # print("Personaje muerto")

        # Si el personaje sigue vivo se actualiza su estado
        else:

            (speedx, speedy) = self.speed
            # print(self.rect)
            now = pygame.time.get_ticks()
            # Si estamos knockeados, no se hace ninguna otra animación
            if not (self.animationNumber == SPRITE_KNOCKED and ((now - self.lastHit) < Character_KNOCKDOWN)):

                # Si vamos a la izquierda o derecha
                if (self.movement == LEFT) or (self.movement == RIGHT):
                    # Cogemos el lado hacia el que mira
                    self.looking = self.movement
                    # Si mirando a la izquierda
                    if self.movement == LEFT:
                        speedx = -self.runSpeed
                    # o si está mirando a la derecha
                    else:
                        speedx = self.runSpeed
                    # Si no estamos saltando
                    if self.animationNumber != SPRITE_JUMPING:
                        # La postura actual será estar caminando
                        self.animationNumber = SPRITE_WALKING
                        # Ademas, si no estamos encima de ninguna plataforma, caeremos
                        if pygame.sprite.spritecollideany(self, platformGroup) == None:
                            self.animationNumber = SPRITE_JUMPING
                # Si queremos saltar
                if self.movement == UP:
                    if not(self.isJumping):
                        # La animation actual sera estar saltando
                        self.animationNumber = SPRITE_JUMPING
                        # Le imprimimos una speed en el eje y
                        speedy = -self.jumpSpeed

                # Si está disparando
                if self.animationNumber == SPRITE_IDLE and self.movement == SHOOTING:
                    self.animationNumber = SPRITE_SHOOTING

                # Si acaba de recibir daño
                if self.movement == HURT:
                    self.animationNumber = SPRITE_KNOCKED
                    if not(self.isKnocked):
                        if(self.looking == RIGHT):
                            speedx = -self.runSpeed
                        else:
                            speedx = self.runSpeed
                        speedy = (-self.jumpSpeed / 3)

                # Si no se ha pulsado ninguna tecla
                if self.movement == IDLE:
                    # Si no estamos saltando o en knock, la animación actual será estar quieto
                    if not (self.animationNumber == SPRITE_JUMPING or self.animationNumber == SPRITE_KNOCKED):
                        self.animationNumber = SPRITE_IDLE
                    speedx = 0

                # Obtenemos las plataformas contra las que está colisionando el
                # personaje
                platforms_collided = pygame.sprite.spritecollide(self, platformGroup, False)

                # Si estamos en el aire
                if self.animationNumber == SPRITE_JUMPING or self.animationNumber == SPRITE_KNOCKED:
                    # Miramos a ver si hay que parar de caer: si hemos llegado a una
                    # platforma. Para ello, miramos si hay colision con alguna
                    # platforma del grupo
                    # Ademas, esa colision solo nos interesa cuando estamos cayendo
                    # y solo es efectiva cuando caemos encima, no de lado, es decir,
                    # cuando nuestra position inferior esta por encima de la parte de
                    # abajo de la platform
                    (speedx,speedy) = self.check_collisions_with_floor_ceiling(platforms_collided, (speedx,speedy), tiempo)

                # Comprobamos si el jugador colisiona contra un muro lateralmente
                (speedx, speedy) = self.check_collisions_with_wall(platforms_collided, (speedx, speedy))

            elif self.animationNumber == SPRITE_KNOCKED and  ((now - self.lastHit) < Character_KNOCKDOWN):
                # Obtenemos las plataformas contra las que está colisionando el personaje
                platforms_collided = pygame.sprite.spritecollide(self, platformGroup, False)
                (speedx, speedy) = self.check_collisions_with_floor_ceiling(
                    platforms_collided, (speedx, speedy), tiempo)
                (speedx, speedy) = self.check_collisions_with_wall(
                    platforms_collided, (speedx, speedy))

            # Actualizamos la imagen a mostrar
            self.updatePosture()

            self.speed = (speedx, speedy)

            MySprite.update(self, tiempo)
        return

    def check_collisions_with_floor_ceiling(self, platforms_collided, speed, tiempo):
        (speedx, speedy) = speed
        floor_collision = False
        for platform in platforms_collided:
            if (speedy > 0) and (platform.rect.bottom > self.rect.bottom) \
                    and platform.rect.left < self.rect.centerx < platform.rect.right:
                floor_collision = True
                # Lo situamos con la parte de abajo un pixel colisionando con
                # la plataforma para poder detectar cuando se cae de ella
                self.setposition(
                    (self.position[0],
                     platform.position[1] - platform.rect.height + 1))
                # Lo ponemos como quieto
                self.animationNumber = SPRITE_IDLE
                # Y estará quieto en el eje y
                speedy = 0
                self.isJumping = False
                self.isKnocked = False

            # Si no cae sobre una plataforma, comprobamos si ha chocado
            # contra el techo
            elif (speedy < 0) and (platform.rect.bottom < self.rect.bottom) \
                    and platform.rect.left < self.rect.centerx < platform.rect.right:
                self.setposition(
                    (self.position[0],
                     platform.position[1] + platform.rect.height))
                speedy = 0

        # Si no caemos en una platform, aplicamos el efecto de la gravedad
        if not floor_collision:
            if self.animationNumber == SPRITE_JUMPING:
                speedy += GRAVITY * tiempo
            else:
                speedy += GRAVITY * tiempo

        return (speedx, speedy)

    def check_collisions_with_wall(self, platforms_collided, speed):
        (speedx, speedy) = speed
        for platform in platforms_collided:
            # Colisión lateral
            if platform.rect.top < self.rect.centery < platform.rect.bottom:
                # Si colisiona por la izquierda de la plataforma
                if platform.rect.centerx > self.rect.centerx:
                    # Se mueve un poco el personaje para que no quede
                    # bloqueado contra el muro
                    self.setposition(
                        (platform.position[0] - self.rect.width,
                         self.position[1]))

                # Si colisiona por la derecha de la plataforma
                else:
                    self.setposition(
                        (platform.position[0] + platform.rect.width,
                         self.position[1]))

                # Para al personaje para que no pueda atravesar el muro
                speedx = 0
                break

        return (speedx,speedy)

# -------------------------------------------------
# Clase Player

class Player(Character):
    "Protagonista juego"

    def __init__(self, initialWeapon):
        # Invocamos al constructor de la clase padre con la configuracion para
        # el personaje protagonista
        
        self.weapon = initialWeapon
        self.weapon.kill()

        self.knockSound = ResourcesManager.LoadSound("knocktareixa.ogg")

        self.deathSound = "tareixadeath.ogg"

        #efecto de sonido para morte, por defecto efecto zombie
       
        Character.__init__(self, 'Tareixa.png', 'coordTareixa.txt',
                           [4, 12, 1, 1, 21, 18, 1], Character_SPEED, Character_JUMP_SPEED,
                           Character_ANIMATION_DELAY, MAX_HEALTH )

    def mover(self, control):
        # Indicamos la acción a realizar segun la tecla pulsada por el jugador
        if control.jump():
            Character.mover(self, UP)
        elif control.left():
            Character.mover(self, LEFT)
        elif control.right():
            Character.mover(self, RIGHT)
        elif control.isShooting():
            Character.mover(self, SHOOTING)
        else:
            Character.mover(self, IDLE)

    def shoot(self,grupoSpritesDinamicos, grupoSprites, scrollx):
        Character.mover(self, SHOOTING)
        self.weapon.shoot(self,scrollx, grupoSpritesDinamicos, grupoSprites)

            
    
        
      
            

    def update(self, platformGroup, enemyGroup, tiempo):
        # Comprobamos si hay colision entre el jugador y algun enemigo
        # Si la hay, restamos vida al jugador
        enemy = pygame.sprite.spritecollideany(self, enemyGroup)
        now = pygame.time.get_ticks()
        if enemy is not None:
            if now - self.lastHit >= self.cooldownHit:
                self.knockSound.play()
                self.lastHit = now
                self.health -= enemy.damage_level
                print("Health = " + str(self.health))
                Character.mover(self, HURT)

        if (self.weapon.magazine<=0 ) and ( (now - self.weapon.lastBullet) >= self.weapon.reloadSpeed):
            self.weapon.magazine = self.weapon.maxAmmo
           
        Character.update(self, platformGroup, enemyGroup, tiempo)
# -------------------------------------------------
# Clase NPC

class NPC(Character):
    "El resto de personajes no jugadores"

    def __init__(self, imageFile, coordFile, numImages, speed, jumpSpeed,
                 animationDelay, health):
        # Primero invocamos al constructor de la clase padre con los parametros
        # pasados
        
        Character.__init__(self, imageFile, coordFile, numImages, speed,
                           jumpSpeed, animationDelay, health)

    # Método que implementa la IA de los personajes que no son jugadores.
    # Este método será implementado en las clases inferiores
    def move_cpu(self, player):
        # Por defecto un enemigo no hace nada
        return

# -------------------------------------------------
# Clase Enemy

# Clase que van a utilizar todos los tipos de enemigos
class Enemy(NPC):

    def __init__(self, image, coord, numImages, enemy_speed=0.05,
                 enemy_jump_speed=0.05, enemy_animation_delay=6, health=0.5,
                 damage_level=0.5, deathSound = "zombiedeath.ogg"):

        self.deathSound = deathSound
        # Invocamos al constructor de la clase padre con la configuracion de
        # este enemigo concreto
        NPC.__init__(self, image, coord, numImages, enemy_speed,
                     enemy_jump_speed, enemy_animation_delay, health)

        # Establecer el nivel de daño que provoca el enemigo. Es un valor que
        # varía con incrementos de 0.5
        self.damage_level = damage_level



    # La implementacion de la IA para un enemigo básico.
    # En este caso el enemigo sigue al jugador.
    def move_cpu(self, player):

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left > 0 and self.rect.right < WIDTH_SCREEN and \
                self.rect.bottom > 0 and self.rect.top < HEIGHT_SCREEN:

            # Y nos movemos andando hacia el jugador según su posición en el
            # eje X
            if player.position[0] < self.position[0]:
                Character.mover(self, LEFT)
            else:
                Character.mover(self, RIGHT)

        # Si este enemigo no esta en pantalla, no hara nada
        else:
            Character.mover(self, IDLE)



# Zombie de nivel 1
class Zombie1(Enemy):

    def __init__(self):
        Enemy.__init__(self,'zombie1.png', 'coordZombie1.txt', [1,8,1,1, 1, 1, 1],
                       enemy_speed=0.05, enemy_jump_speed=0.05, health=1,
                       damage_level=0.5)


# Zombie de nivel 2
class Zombie2(Enemy):

    def __init__(self):
        Enemy.__init__(self,'zombie2.png', 'coordZombie2.txt', [1,7,1,1, 1, 1, 1],
                       enemy_speed=0.1, enemy_jump_speed=0.2, health=1.5,
                       damage_level=0.5)


# Zombie de nivel 3
class Zombie3(Enemy):

    def __init__(self):
        Enemy.__init__(self,'zombie3.png', 'coordZombie3.txt', [1,8,1,1, 1, 1, 1],
                       enemy_speed=0.13, enemy_jump_speed=0.2, health=2,
                       damage_level=1)


# Zombie de nivel 4
class Zombie4(Enemy):

    def __init__(self):
        Enemy.__init__(self,'zombie4.png', 'coordZombie4.txt', [1,8,3,1, 1, 1, 1],
                       enemy_speed=0.15, enemy_jump_speed=0.2, health=2.5,
                       damage_level=1)


# Oso (Boss)
class Bear(Enemy):

    def __init__(self):
        Enemy.__init__(self,'bear.png', 'coordBear.txt', [1,11,1,1, 1, 1, 1],
                       enemy_speed=0.07, enemy_jump_speed=0.2, health=3,
                       damage_level=1)


# Jabalí (Boss)
class WildBoar(Enemy):

    def __init__(self):
        Enemy.__init__(self,'wild_boar.png', 'coordWildBoar.txt', [1,9,1,1, 1, 1, 1],
                       enemy_speed=0.1, enemy_jump_speed=0.2, health=4,
                       damage_level=0.5)


class Chicken(Enemy):

    def __init__(self):
        Enemy.__init__(self,'chicken.png', 'coordChicken.txt', [1,16,4,1, 1, 1, 1],
                       enemy_speed=0.1, enemy_jump_speed=0.2, health=5,
                       damage_level=1, deathSound='chicken_clucking.ogg')


class Crab(Enemy):

    def __init__(self):
        Enemy.__init__(self,'crab.png', 'coordCrab.txt', [1,12,1,1, 1, 1, 1],
                       enemy_speed=0.12, enemy_jump_speed=0.2, health=5,
                       damage_level=1.5)


# WARNING: CADA VEZ QUE SE AÑADE UN ENEMIGO NUEVO HAY QUE AÑADIR UNA REFERENCIA
# A SU CLASE EN EL MÉTODO __get_enemy() EN EL FICHERO fase.py
