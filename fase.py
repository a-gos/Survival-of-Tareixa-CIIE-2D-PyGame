# -*- coding: utf-8 -*-

import pygame, scene
from scene import *
from player import *
from pygame.locals import *
from resourcesmanager import ResourcesManager
from control import *
import os
from utilities import *
from menu import *
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
        try:
            # Para ejecutar el juego es necesario que haya un Jugador situado
            # en algún punto del mapa donde comienza el juego, sinó lo hay se
            # para la ejecución del juego
            tile = next(layer.tiles())
        except StopIteration:
            raise ResourceWarning("Player's sprite not found. Include it in the"
                                  " maps editor")
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

        # El jefe final del nivel está en una capa diferente y guardamos una
        # referencia a el en la fase para comprobar cuando se termina el nivel
        layer = conf.get_layer_by_name('Boss')
        try:
            # Para ejecutar el juego es necesario que haya un Jefe al final del
            # nivel, sinó lo hay se para la ejecución del juego
            tile = next(layer.tiles())
        except StopIteration:
            raise ResourceWarning("Boss's sprite not found. Include it in the"
                                  " maps editor")
        coord_x = tile[0]
        coord_y = tile[1]
        enemy_name = os.path.basename(tile[2][0])
        self.boss = self.__get_enemy(enemy_name)
        self.boss.setposition((coord_x * TILE_SIZE, coord_y * TILE_SIZE))
        self.enemyGroup.add(self.boss)

        # Creamos un grupo con los Sprites que se mueven (personaje, enemigos, proyectiles,etc.
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.player, self.enemyGroup.sprites() )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.player, self.enemyGroup.sprites(), self.platformGroup.sprites() )

        # Creamos los controles del jugador
        self.control = ControlKeyboard()

        # Creamos el Heads-Up Display con el nivel de vida
        self.hud = HUD()


     #ANIMATIONS AQUI

    # Devuelve el enemigo que se corresponde con el nombre del fichero que lo
    # representa en el directorio data/scene
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
        elif name == 'wild_boar.png':
            enemy = WildBoar()
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
        # y, si lo son, realiza el movimiento de los Sprites

        self.grupoSpritesDinamicos.update(self.platformGroup, self.enemyGroup, time)

        # Si el jugador se queda sin vida porque lo ha matado un enemigo o se
        # ha caído al vacío, se acaba el juego
        if not self.player.alive():
            # print("JUEGO PERDIDO")
            # Llamada al director para manejar las escenas
            self.director.exitScene()
            self.director.stackScene(MenuGameover(self.director))
        elif not self.boss.alive():
            # print("JUEGO GANADO")
            self.director.exitScene()
            self.director.stackScene(MenuNivelCompletado(self.director))

        # Actualizamos el scroll
        self.updateScroll(self.player)

        # Actualizamos el HUD
        self.hud.update(self.player.health)



    def paint(self, screen):
        # Dibujamos el decorado
        self.scenary.paint(screen)
        # Luego los Sprites
        self.grupoSprites.draw(screen)
        # Y por ultimo, dibujamos el HUD por encima del decorado
        self.hud.paint(screen)


    def events(self, event_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in event_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.exitProgram()
            if event.type == pygame.KEYDOWN:

                self.control.shoot(self.player, self.grupoSpritesDinamicos, self.grupoSprites, self.scrollx, event)
               # if event.key == pygame.K_SPACE:
               #    self.player.shoot(self.grupoSpritesDinamicos, self.grupoSprites, self.scrollx)
                if event.key == pygame.K_p:
                    pause_scene = MenuPausa(self.director)
                    self.director.stackScene(pause_scene)
                    # self.director.exit_scene = True

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


# -------------------------------------------------
# Clase Heads-Up Display

class HUD:

    def __init__(self):
        self.sprites = ResourcesManager.LoadImageHud('corazons_con_calavera.png', -1)
        # self.sprites = self.sprites.convert_alpha()

        # Cargamos las coordenadas de cada sprite
        data = ResourcesManager.LoadCoordFileHud('coord_corazons.txt')
        data = data.split()
        self.coords = []
        cont = 0
        for animation in range(7):
            self.coords.append(pygame.Rect((int(data[cont]), int(
                data[cont + 1])), (int(data[cont + 2]), int(data[cont + 3]))))
            cont += 4

        # Establecemos como imagen inicial los 3 corazones
        self.currentImage = 6
        self.rect = self.coords[self.currentImage]
        self.pos_x = 50
        self.pos_y = 50

    def update(self, player_health):
        # Dependiendo de la vida del jugador se carga una imagen u otra
        if player_health >= 0:
            self.currentImage = int(player_health * 2)
        else:
            self.currentImage = 0
        self.rect = self.coords[self.currentImage]

    def paint(self, screen):
        image = self.sprites.subsurface(self.rect)
        screen.blit(image, (self.pos_x, self.pos_y))
