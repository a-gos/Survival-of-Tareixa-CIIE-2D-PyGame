# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from player import Player
from fase import Fase

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importar modulos
import pygame
import director
from director import *


if __name__ == '__main__':

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    fase = Fase(director)
    # Le decimos al director que apile esta escena
    director.stackscene(fase)
    # Y ejecutamos el juego
    director.execute()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()
