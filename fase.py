# -*- coding: utf-8 -*-

import pygame, scene
from scene import *
from player import *
from pygame.locals import *
from resourcesmanager import ResourcesManager
from control import *
import os
from utilities import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la screen para hacer scroll horizontal
MIN_X_PLAYER = (WIDTH_SCREEN / 2) - PLAYER_SIZE
MAX_X_PLAYER = WIDTH_SCREEN - MIN_X_PLAYER

# -------------------------------------------------
# Clase Fase

class Fase(Scene):
    def __init__(self, director, num_level):

        # Recibe como parámetro el número de fase, a partir del cual se carga
        #  un fichero donde está la configuración de esa fase en concreto,
        #  con cosas como:
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posición de inicio del jugador
        #  etc.

        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, director)

        # Cargamos el archivo de configuración del nivel
        filename = 'level_' + str(num_level) + '.tmx'
        conf = ResourcesManager.LoadConfigurationFile(filename)

        # Imagen de fondo
        back_layer = conf.get_layer_by_name('Background')
        back_image_name = os.path.basename(back_layer.image[0])

        # Creamos el fondo del nivel
        self.scenary = Scenary(back_image_name)

        # Capa de plataformas
        layer = conf.get_layer_by_name('Platforms')
        self.platformGroup = pygame.sprite.Group()
        for tile in layer.tiles():
            coord_x = tile[0] # Multiplicar por TILE_SIZE para obtener el pixel donde se dibujará
            coord_y = tile[1]
            tile_image = os.path.basename(tile[2][0])
            tile_coords = tile[2][1]
                # tile_coords es una tupla de 4 elementos:
                #  - coord_x en la imagen de bloques
                #  - coord y en la imagen de bloques
                #  - size_x del bloque
                #  - size y del bloque

            rect = pygame.Rect(coord_x*TILE_SIZE, coord_y*TILE_SIZE, tile_coords[2], tile_coords[3])

            # Especificamos que trozo de la imagen se va a dibujar
            subimage_rectangle = pygame.Rect(tile_coords[0], tile_coords[1], tile_coords[2], tile_coords[3])

            platform = Platform(tile_image, rect, subimage_rectangle)
            self.platformGroup.add(platform)


        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos el sprite del jugador
        self.player = Player()

        # Ponemos al jugador en su posición inicial
        layer = conf.get_layer_by_name('Character')
        tile = next(layer.tiles())
        coord_x = tile[0]
        coord_y = tile[1]
        self.player.setposition((coord_x*TILE_SIZE, coord_y*TILE_SIZE))

        # Creamos un grupo donde se guardarán los disparos
        self.grupoShots = pygame.sprite.Group()

        # Y los enemigos que tendran en este decorado
        self.enemyGroup = pygame.sprite.Group()
        layer = conf.get_layer_by_name('Enemies')
        for tile in layer.tiles():
            coord_x = tile[0]
            coord_y = tile[1]
            enemy_name = os.path.basename(tile[2][0])
            enemy = self.__get_enemy(enemy_name)
            enemy.setposition((coord_x*TILE_SIZE, coord_y*TILE_SIZE))
            self.enemyGroup.add(enemy)

        # Creamos un grupo con los Sprites que se mueven (personaje, enemigos, proyectiles,etc.
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.player, self.enemyGroup.sprites() )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.player, self.enemyGroup.sprites(), self.platformGroup.sprites() )

        # Creamos los controles del jugador
        self.control = ControlKeyboard()


     #ANIMATIONS AQUI

    # Devuelve el enemigo que se corresponde con el nombre del fichero
    def __get_enemy(self, name):
        enemy = None
        if name == 'zombie1.png':
            enemy = Zombie1()
        elif name == 'zombie2.png':
            enemy = Zombie2()
        elif name == 'zombie3.png':
            enemy = Zombie3()
        elif name == 'zombie4.png':
            enemy = Zombie4()
        elif name == 'bear.png':
            enemy = Bear()
        else:
            enemy = Zombie1()
        return enemy

    # Devuelve True o False según se ha tenido que desplazar el scroll
    def updateOrderedScroll(self, player):

        # Debug info
        # print(player.rect.right)
        # print(self.scenary.rect.right)

        # Si el jugador se encuentra más allá del borde izquierdo
        
       
        if (player.rect.left<MIN_X_PLAYER):
            offset = MIN_X_PLAYER - player.rect.left

            # Si el escenario ya está a la izquierda del todo, no movemos mas
            #  la camara (player size para compensar)
            if self.scrollx <= 0:
                self.scrollx = 0
              
                #Miramos si el jugador esta en el limte de la ventana, si es así lo colocamos ahi y no desplazamos
                if (player.rect.left<=0):
                    player.setposition(( 0, player.position[1]))

                return False  # No se ha actualizado el scroll

            # Si se puede hacer más scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - offset
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - offset
                return True  # Se ha actualizado el scroll

        # Si el jugador se encuentra más allá del borde derecho
        elif (player.rect.right>MAX_X_PLAYER):

            # Se calcula cuantos pixeles esta fuera del borde
            offset = player.rect.right - MAX_X_PLAYER

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if (self.scrollx + WIDTH_SCREEN >= self.scenary.rect.right ):
               
                self.scrollx = self.scenary.rect.right - WIDTH_SCREEN
               
                # Miramos si el jugador esta en el limite de la derecha

                #IMPORTANTE: POR QUE WIDH SCREEN:
                    #POR COMO ESTA IMPLEMENTADO EL MOVIMIENTO, AL HACER SCROLL EL PJ SE MANTIENE EN LA
                    # MISMA POSICION Y SE ACTUALIZA EL RESTO, ENTONCES LA POSICION RELATIVA SE PIERDA
                    # PERO TAMBIEN SIGNIFICA QUE EL FINAL DEL ESCENARIO PARA LA POSICION DEL JUGADOR 
                    # SERA SIEMPRE EL ANCHO DE LA PANTALLA
                if (player.rect.right >=WIDTH_SCREEN):
                    player.setposition((self.scrollx+WIDTH_SCREEN - PLAYER_SIZE, player.position[1]))

                return False  # No se ha actualizado el scroll

            # Si se puede hacer scroll a la derecha
            else:
                # Calculamos el nivel de scroll actual: el anterior + offset
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + offset
                return True  # Se ha actualizado el scroll

        

    def updateScroll(self, player):
        # Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
     
        stateScroll = self.updateOrderedScroll(player)
      
        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if stateScroll:
            # Actualizamos la posición en screen de todos los Sprites según el scroll actual
            # Cuando se cambia el scroll, se llama al método setpositionscreen()
            # de MiSprite: cambia la posición local pero no la global de los Sprites
            for sprite in iter(self.grupoSprites):
                sprite.setpositionscreen((self.scrollx, 0))

            # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.scenary.update(self.scrollx)



    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
    #  Se mueven los sprites dinámicos, todos a la vez
    #  Se comprueba si hay colision entre algun jugador y algun enemy
    #  Se comprueba si algún jugador ha salido de la screen, y se actualiza el scroll en consecuencia
    #     Actualizar el scroll implica tener que desplazar todos los sprites por screen
    def update(self, time):

        # Primero, se indican las acciones que van a hacer los enemys segun como esten los jugadores
        for enemy in iter(self.enemyGroup):
            enemy.move_cpu(self.player)

        # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
        # En el caso de los jugadores, esto ya se ha realizado

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites

        self.grupoSpritesDinamicos.update(self.platformGroup, time)

        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en screen se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si los disparos colisionan con algún enemigo o plataforma para eliminarlos
        self.grupoShots.update(self.platformGroup, self.enemyGroup, time)

        # Si los disparos colisionan contra una plataforma o un enemigo hay que
        # eliminarlos. Además, en el último caso, hay que restar vida a los
        # enemigos.


        # Comprobamos si hay colision entre el jugador y algun enemigo
        # Si la hay, restamos vida al jugador
        enemy = pygame.sprite.spritecollideany(self.player, self.enemyGroup)
        if enemy is not None:
            self.player.health -= enemy.damage_level
            print("Health = " + str(self.player.health))

        # Si el jugador se queda sin vida porque lo ha matado un enemigo o se
        # ha caído al vacío, se acaba el juego
        if not self.player.alive():
            # Llamada al director para manejar las escenas
            self.director.exitScene()

        # Actualizamos el scroll
        self.updateScroll(self.player)


        
    def paint(self, screen):
        # Dibujamos el decorado
        self.scenary.paint(screen)
        # Luego los Sprites
        self.grupoSprites.draw(screen)
        # Y por ultimo, dibujamos las animaciones por encima del decorado
        # AÑADIR HUD


    def events(self, event_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in event_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player, 0.5, self.scrollx)

                    # self.grupoSpritesDinamicos.add(bullet)
                    self.grupoShots.add(bullet)
                    self.grupoSprites.add(bullet)

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        self.player.mover(self.control)
       

# -------------------------------------------------
# Clase Platform

#class Platform(pygame.sprite.Sprite):
class Platform(MySprite):
    def __init__(self, image, rectangle, subimage_rect=None):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)
        # Rectangulo con las coordenadas en screen que ocupara
        self.rect = rectangle
        # Y lo situamos de forma global en esas coordenadas
        self.setposition((self.rect.left, self.rect.top))
        # Cargamos la images correspondiente (si la plataforma está visible)
        if image is not None:
            self.image = ResourcesManager.LoadImageScene(image, -1)
            if subimage_rect is not None:
                # Si la imagen contiene distintos bloques y solo se quiere dibujar uno
                self.image = self.image.subsurface(subimage_rect)
        else:
            self.image = pygame.Surface((0, 0))

# -------------------------------------------------
# Clase Scenary

class Scenary:
    def __init__(self, image_name):
        self.imagen = ResourcesManager.LoadImageScene(image_name, -1)

        # TAMAÑO DEL FONDO AQUI (TAMBIEN TAMAÑO NIVEL)
        # self.imagen = pygame.transform.scale(self.imagen, (6016, 608))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = HEIGHT_SCREEN

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, WIDTH_SCREEN, HEIGHT_SCREEN)
        self.rectSubimagen.left = 0  # El scroll horizontal empieza en la position 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def paint(self, screen):
        screen.blit(self.imagen, self.rect, self.rectSubimagen)
