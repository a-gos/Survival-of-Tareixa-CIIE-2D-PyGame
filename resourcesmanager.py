# -*- coding: utf-8 -*-

# -------------------------------------------------
# LIB
# -------------------------------------------------

import pygame, sys, os
from pygame.locals import *
from pytmx.pytmx import TiledMap

# -------------------------------------------------
# CODE
# -------------------------------------------------

class ResourcesManager(object):
    resources = {}

    @classmethod
    def LoadImageHud(cls, name, colorkey=None):
        return cls.LoadImage('hud', name, colorkey)

    @classmethod
    def LoadImageMenu(cls, name, colorkey=None):
        return cls.LoadImage('menu', name, colorkey)

    @classmethod
    def LoadImageStory(cls, name, colorkey=None):
        return cls.LoadImage('story', name, colorkey)

    @classmethod
    def LoadImageScene(cls, name, colorkey=None):
        return cls.LoadImage('scene', name, colorkey)

    @classmethod
    def LoadImageCharacter(cls, name, colorkey=None):
        return cls.LoadImage('characters', name, colorkey)

    @classmethod
    def LoadImage(cls, rel_path, name, colorkey=None):
        # Si el nombre de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            
            current_path = os.path.dirname(__file__) 
            fullname_path = os.path.join(current_path, 'data', rel_path)
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
    def LoadCoordFileCharacter(cls, name):
        return cls.LoadCoordFile('characters', name)

    @classmethod
    def LoadCoordFileHud(cls, name):
        return cls.LoadCoordFile('hud', name)

    @classmethod
    def LoadCoordFile(cls, rel_path, name):
        # Si el nombre de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            current_path = os.path.dirname(__file__) 
            fullname_path = os.path.join(current_path, 'data', rel_path)
            fullname = os.path.join(fullname_path, name)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.resources[name] = datos
            # Se devuelve
            return datos

    @classmethod
    def LoadConfigurationFile(cls, name):

        # Si el nombre de archivo está entre los resources ya cargados
        if name in cls.resources:
            # Se devuelve ese recurso
            return cls.resources[name]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el fichero de configuración indicando la carpeta en la que está

            current_path = os.path.dirname(__file__)
            fullname_path = os.path.join(current_path, 'data/levels')
            fullname = os.path.join(fullname_path, name)

            try:
                data = TiledMap(fullname)
            except:
                print('Cannot load configuration file:', fullname)
                raise SystemExit()

            # Se almacena
            cls.resources[name] = data
            # Se devuelve
            return data