# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from scene import *
from resourcesmanager import *
from fase import Fase

# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    # Guarda una referencia a la pantalla a la que pertenece, y el rectángulo
    # que ocupa en pantalla, para saber si se ha hecho clic
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    # Método para situarlo en pantalla
    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    # Método que dice si se ha hecho clic en él
    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False

    # Métodos abstractos a implementar por las subclases

    # Dibuja el elemento en pantalla
    def paint(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")

    # Acción a realizar si se hace clic en el elemento
    def action(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = ResourcesManager.LoadImageMenu(nombreImagen,-1)
        # self.imagen = pygame.transform.scale(self.imagen, (20, 20))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def paint(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class BotonJugar(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'xogar.png', (615,224))
    def action(self):
        self.pantalla.menu.ejecutarJuego()

class BotonInstrucciones(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'instruccions.png', (622,340))
    def action(self):
        self.pantalla.menu.mostrarIntrucciones()

class BotonSalir(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'sair_gris.png', (626,451))
    def action(self):
        self.pantalla.menu.salirPrograma()

class BotonVolver(Boton):
    def __init__(self, pantalla):
        Boton.__init__(self, pantalla, 'volver.png', (50,498))
    def action(self):
        self.pantalla.menu.mostrarPantallaInicial()


# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = ResourcesManager.LoadImageMenu(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (WIDTH_SCREEN, HEIGHT_SCREEN))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []

    def events(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClic = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClic = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClic):
                            elemento.action()

    def paint(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.paint(pantalla)

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondo_principal.png')
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self)
        botonInstrucciones = BotonInstrucciones(self)
        botonSalir = BotonSalir(self)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonInstrucciones)
        self.elementosGUI.append(botonSalir)

class PantallaIntruccionesGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondo_instruccions.png')
        # Creamos el boton y lo metemos en la lista
        botonVolver = BotonVolver(self)
        self.elementosGUI.append(botonVolver)


# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Scene):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(self))
        self.listaPantallas.append(PantallaIntruccionesGUI(self))
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def events(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
            elif evento.type == pygame.QUIT:
                self.director.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].events(lista_eventos)

    def paint(self, pantalla):
        self.listaPantallas[self.pantallaActual].paint(pantalla)

    #--------------------------------------
    # Metodos propios del menu

    def salirPrograma(self):
        self.director.exitProgram()

    def ejecutarJuego(self):
        fase = Fase(self.director, 1)
        self.director.stackscene(fase)

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    def mostrarIntrucciones(self):
        self.pantallaActual = 1

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
