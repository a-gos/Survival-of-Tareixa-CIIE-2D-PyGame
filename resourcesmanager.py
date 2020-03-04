# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *

# -------------------------------------------------
# CODE
# -------------------------------------------------

class ResourcesManager(object):
    resources = {}
            
    @classmethod
    def LoadImage(cls, name, colorkey=None):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            
            current_path = os.path.dirname(__file__) 
            fullname_path = os.path.join(current_path, 'data')
            fullname = os.path.join(fullname_path, name)

            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print('Cannot load image:', fullname)
                raise SystemExit(message)
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.resources[name] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def LoadCoordFile(cls, name):
        # Si el name de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el name de su carpeta
            current_path = os.path.dirname(__file__) 
            fullname_path = os.path.join(current_path, 'data')
            fullname = os.path.join(fullname_path, name)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.resources[name] = datos
            # Se devuelve
            return datos