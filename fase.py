# -*- coding: utf-8 -*-

import pygame, scene
from scene import *
from player import *
from pygame.locals import *
from resourcesmanager import ResourcesManager
from control import *
import os

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la screen para hacer scroll horizontal
MIN_X_PLAYER = (WIDTH_SCREEN / 2) - PLAYER_SIZE
MAX_X_PLAYER = WIDTH_SCREEN - MIN_X_PLAYER

# -------------------------------------------------
# Clase Fase

class Fase(Scene):
    def __init__(self, director, num_level):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las platforms
        #   - Posiciones de los enemys
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Primero invocamos al constructor de la clase padre
        Scene.__init__(self, director)

        # Cargamos el archivo de configuración del nivel
        filename = 'level_' + str(num_level) + '.json'
        conf = ResourcesManager.LoadConfigurationFile(filename)

        ######
        from pytmx.pytmx import TiledMap
        file = TiledMap('./data/levels/level_file.tmx')
        # Imagen de fondo
        back_layer = file.get_layer_by_name('Image Layer 1')
        back_image_name = back_layer.image[0]
        # image = ResourcesManager.LoadImageScene(back_image_name, -1)
        # rect = image.get_rect()

        # Capa de plataformas
        layer = file.get_layer_by_name('Tile Layer 1')
        self.platformGroup = pygame.sprite.Group()
        for tile in layer.tiles():
            coord_x = tile[0] # Multiplicar por TILE_SIZE para obtener el pixel donde se dibujará
            coord_y = tile[1]
            # image = file.get_tile_image(coord_x, coord_y, layer)
            tile_image = os.path.basename(tile[2][0])
            tile_coords = tile[2][1]
            rect = pygame.Rect(coord_x*TILE_SIZE, coord_y*TILE_SIZE, tile_coords[2], tile_coords[3])

            tmp = ResourcesManager.LoadImageScene(tile_image)
            # tmp = tmp.convert_alpha()
            image = tmp.subsurface(pygame.Rect(tile_coords[0], tile_coords[1], tile_coords[2], tile_coords[3]))

            platform = Platform(image, rect)
            self.platformGroup.add(platform)
                # Devuelve una tupla de 4 elementos:
                #  - coord_x en la imagen de bloques
                #  - coord y en la imagen de bloques
                #  - size_x del bloque
                #  - size y del bloque
            # Buscar como obtener un bloque de una imagen que contiene varios

        ######

        # Creamos el decorado y el background

        self.scenary = Scenary('background_level_1_scaled.png')
    #   self.background = Sky()

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.player1 = Player()
        self.grupoPlayers = pygame.sprite.Group(self.player1)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.player1.setposition((500, 820))
    

        # Creamos las plataformas del decorado
        # for layer in conf['layers']:
        #     if layer['name'] == 'platforms':
        #         self.platformGroup = pygame.sprite.Group()
        #         for platfConf in layer['objects']:
        #             if platfConf['visible']:
        #                 image_name = platfConf['name']
        #             else:
        #                 image_name = None
        #             for coord in platfConf['coordinates']:
        #                 platform = Platform(image_name, pygame.Rect(coord[0], coord[1]-250, platfConf['width'], platfConf['height']))
        #                 self.platformGroup.add(platform)

        # platformSuelo = Platform(image, pygame.Rect(0, 580, 6020, 20), True)

        # La platform del techo del edificio
       # platformCasa = Platform(pygame.Rect(870, 417, 200, 10))
        # y el grupo con las mismas
        #self.platformGroup = pygame.sprite.Group( platformSuelo)

        #############################
        # Y los enemys que tendran en este decorado
        enemy1 = Zombie()
        enemy1.setposition((900, 820))

        # Creamos un grupo con los enemys
        self.enemyGroup = pygame.sprite.Group(enemy1)

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.player1, enemy1 )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group( self.player1, enemy1, self.platformGroup.sprites() )

        # Creamos los controles del jugador
        self.control = ControlKeyboard()
        # Creamos las animaciones de fuego,
        #  las que estan detras del decorado, y delante

     #ANIMATIONS AQUI

        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def updateOrderedScroll(self, player1):
     
        print(player1.rect.right)
        print(self.scenary.rect.right)
        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if (player1.rect.left<MIN_X_PLAYER):
            offset = MIN_X_PLAYER - player1.rect.left

            # Si el escenario ya está a la izquierda del todo, no movemos mas la camara (player size para compensar)
            if self.scrollx <= 0:
                self.scrollx = 0
              
               #Miramos si el jugador esta en el limte de la ventana, si es así lo colocamos ahi y no desplazamos

                if (player1.rect.left<=0):
                    player1.setposition(( 0, player1.position[1]))
                
                    

                return False; # No se ha actualizado el scroll

       
            # Si se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - offset
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - offset;

                return True; # Se ha actualizado el scroll

        # Si el jugador de la derecha se encuentra más allá del borde derecho
        elif (player1.rect.right>MAX_X_PLAYER):

            # Se calcula cuantos pixeles esta fuera del borde
            offset = player1.rect.right - MAX_X_PLAYER

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if (self.scrollx + WIDTH_SCREEN >= self.scenary.rect.right ):
               
                self.scrollx = self.scenary.rect.right - WIDTH_SCREEN
               
                # Miramos si el jugador esta en el limite de la derecha

                #IMPORTANTE: POR QUE WIDH SCREEN:
                    #POR COMO ESTA IMPLEMENTADO EL MOVIMIENTO, AL HACER SCROLL EL PJ SE MANTIENE EN LA
                    # MISMA POSICION Y SE ACTUALIZA EL RESTO, ENTONCES LA POSICION RELATIVA SE PIERDA
                    # PERO TAMBIEN SIGNIFICA QUE EL FINAL DEL ESCENARIO PARA LA POSICION DEL JUGADOR 
                    # SERA SIEMPRE EL ANCHO DE LA PANTALLA
                if (player1.rect.right >=WIDTH_SCREEN):
                    player1.setposition((self.scrollx+WIDTH_SCREEN - PLAYER_SIZE, player1.position[1]))

                return False; # No se ha actualizado el scroll

            # Si se puede hacer scroll a la derecha
            else:

                # Calculamos el nivel de scroll actual: el anterior + offset
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + offset;

                return True; # Se ha actualizado el scroll

        

    def updateScroll(self, player1):
        # Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
     
        stateScroll = self.updateOrderedScroll(player1)
      
        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if stateScroll:
            # Actualizamos la posición en screen de todos los Sprites según el scroll actual
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
    #  Se actualiza la position del sol y el color del cielo
    def update(self, time):

        # Primero, se indican las acciones que van a hacer los enemys segun como esten los jugadores
        for enemy in iter(self.enemyGroup):
            enemy.mover_cpu(self.player1)
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

        # Comprobamos si hay colision entre algun jugador y algun enemy
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        if pygame.sprite.groupcollide(self.grupoPlayers, self.enemyGroup, False, False)!={}:
            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
            #self.director.exitScene()
            print("muerto")
        # Actualizamos el scroll
        self.updateScroll(self.player1)
  
        # Actualizamos el background:
        #  la position del sol y el color del cielo
     #   self.background.update(tiempo)

        
    def paint(self, screen):
        # Ponemos primero el background
    #    self.background.paint(screen)
        # Despues, las animaciones que haya detras
       
        # Después el decorado
        self.scenary.paint(screen)
        # Luego los Sprites
        self.grupoSprites.draw(screen)
        # Y por ultimo, dibujamos las animaciones por encima del decorado
        


    def events(self, event_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in event_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.exitProgram()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        self.player1.mover(self.control)
        

# -------------------------------------------------
# Clase Platform

#class Platform(pygame.sprite.Sprite):
class Platform(MySprite):
    def __init__(self, image, rectangle):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)
        # Rectangulo con las coordenadas en screen que ocupara
        self.rect = rectangle
        # Y lo situamos de forma global en esas coordenadas
        self.setposition((self.rect.left, self.rect.top))
        # Cargamos la images correspondiente (si la plataforma está visible)
        if image is not None:
            self.image = image
        else:
            self.image = pygame.Surface((0, 0))
# -------------------------------------------------
# Clase Sky
"""
class Sky:
    def __init__(self):
        self.sol = GestorRecursos.CargarImagen('sol.png', -1)
        self.sol = pygame.transform.scale(self.sol, (300, 200))

        self.rect = self.sol.get_rect()
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += VELOCIDAD_SOL * tiempo
        if (self.posicionx - self.rect.width >= WIDTH_SCREEN):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + WIDTH_SCREEN) / 2):
            ratio = 2 * ((self.rect.width + WIDTH_SCREEN) - self.posicionx) / (self.rect.width + WIDTH_SCREEN)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + WIDTH_SCREEN)
        self.colorSky = (100*ratio, 200*ratio, 255)
        
    def paint(self,screen):
        # Dibujamos el color del cielo
        screen.fill(self.colorSky)
        # Y ponemos el sol
        screen.blit(self.sol, self.rect)

"""
# -------------------------------------------------
# Clase Scenary

class Scenary:
    def __init__(self, image_name):
        self.imagen = ResourcesManager.LoadImageScene(image_name, -1)

        # TAMAÑO DEL FONDO AQUI (TAMBIEN TAMAÑO NIVEL)
        self.imagen = pygame.transform.scale(self.imagen, (6016, 608))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = HEIGHT_SCREEN

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, WIDTH_SCREEN, HEIGHT_SCREEN)
        self.rectSubimagen.left = 0  # El scroll horizontal empieza en la position 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def paint(self, screen):
        screen.blit(self.imagen, self.rect, self.rectSubimagen)
