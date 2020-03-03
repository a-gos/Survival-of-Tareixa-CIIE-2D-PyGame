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
    recursos = {}
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('data', nombre)
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
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('data', nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos