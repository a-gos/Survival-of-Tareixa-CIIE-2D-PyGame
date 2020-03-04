# -*- coding: utf-8 -*-

import pygame, scene
from scene import *
from player import *
from pygame.locals import *
from resourcesmanager import ResourcesManager


# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Los bordes de la screen para hacer scroll horizontal
MIN_X_PLAYER = 50
MAX_X_PLAYER = WIDTH_SCREEN - MIN_X_PLAYER

# -------------------------------------------------
# Clase Fase

class Fase(Scene):
    def __init__(self, director):

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

        # Creamos el decorado y el background
        self.scenary = Scenary()
    #    self.background = Sky()

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.player1 = Player()
        self.grupoPlayers = pygame.sprite.Group( self.player1)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.player1.setposition((200, 551))
    

        # Creamos las platforms del decorado
        # La platform que conforma todo el suelo
        platformSuelo = Platform(pygame.Rect(0, 550, 1200, 15))
        # La platform del techo del edificio
       # platformCasa = Platform(pygame.Rect(870, 417, 200, 10))
        # y el grupo con las mismas
        self.platformGroup = pygame.sprite.Group( platformSuelo)

        # Y los enemys que tendran en este decorado
     #   enemy1 = Sniper()
     #   enemy1.setposition((1000, 418))

        # Creamos un grupo con los enemys
        self.grupoEnemy = pygame.sprite.Group()

        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.player1 )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group( self.player1, self.grupoEnemy )

        # Creamos las animaciones de fuego,
        #  las que estan detras del decorado, y delante

     #ANIMATIONS AQUI

        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def updateOrderedScroll(self, player1):
      

        # Si el jugador de la izquierda se encuentra más allá del borde izquierdo
        if (player1.rect.left<MIN_X_PLAYER):
            offset = MIN_X_PLAYER - player1.rect.left

            # Si el escenario ya está a la izquierda del todo, no lo movemos mas
            if self.scrollx <= 0:
                self.scrollx = 0

                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                player1.setposition((MIN_X_PLAYER, player1.position[1]))

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
            if self.scrollx + WIDTH_SCREEN >= self.scenary.rect.right:
                self.scrollx = self.scenary.rect.right - WIDTH_SCREEN

                # En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
                player1.setposition((self.scrollx+MAX_X_PLAYER-player1.rect.width, player1.position[1]))

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
        if pygame.sprite.groupcollide(self.grupoPlayers, self.grupoEnemy, False, False)!={}:
            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
            self.director.exitScene()

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
        pressedKeys = pygame.key.get_pressed()
        self.player1.mover(pressedKeys, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        

# -------------------------------------------------
# Clase Platform

#class Platform(pygame.sprite.Sprite):
class Platform(MySprite):
    def __init__(self,rectangle):
        # Primero invocamos al constructor de la clase padre
        MySprite.__init__(self)
        # Rectangulo con las coordenadas en screen que ocupara
        self.rect = rectangle
        # Y lo situamos de forma global en esas coordenadas
        self.setposition((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las platforms no se van a ver, asi que no se carga ninguna imagen
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
    def __init__(self):
        self.imagen = ResourcesManager.LoadImage('level1/fondoNivel1.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (1200, 300))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = HEIGHT_SCREEN

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, WIDTH_SCREEN, HEIGHT_SCREEN)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la position 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def paint(self, screen):
        screen.blit(self.imagen, self.rect, self.rectSubimagen)
