# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from scene import *
from resourcesmanager import *
import fase

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
        self.rect.top = posiciony

    # Método que dice si se ha hecho clic en él
    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and \
                (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
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


# Representa imágenes estáticas que no realizan ninguna acción
class ElementoEstaticoGUI(ElementoGUI):

    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del elemento estático
        self.imagen = ResourcesManager.LoadImageMenu(nombreImagen, -1)
        # Se llama al método de la clase padre con el rectángulo que ocupa
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def paint(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def action(self):
        pass
# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, pantalla, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = ResourcesManager.LoadImageMenu(nombreImagen,-1)
        # Se llama al método de la clase padre con el rectángulo que ocupa el
        # botón
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def paint(self, pantalla):
        pantalla.blit(self.imagen, self.rect)


class BotonJugar(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.ejecutarJuego()


class BotonInstrucciones(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.mostrarIntrucciones()


class BotonSalir(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.salirPrograma()


class BotonVolver(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.mostrarPantallaInicial()


class BotonContinuar(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.continuarJuego()


class BotonRepetirNivel(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.repetirNivel()


class BotonSiguienteNivel(Boton):
    def __init__(self, pantalla, nombreImagen, posicion):
        Boton.__init__(self, pantalla, nombreImagen, posicion)

    def action(self):
        self.pantalla.menu.siguienteNivel()

# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = ResourcesManager.LoadImageMenu(nombreImagen)
        # self.imagen = self.imagen.convert_alpha()
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


class PantallaInicial(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondo_principal.png')
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self, 'xogar.png', (615,204))
        botonInstrucciones = BotonInstrucciones(self, 'instruccions.png', (622,290))
        botonSalir = BotonSalir(self, 'sair_gris.png', (626,410))
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonInstrucciones)
        self.elementosGUI.append(botonSalir)


class PantallaIntrucciones(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondo_instruccions.png')
        # Creamos el boton y lo metemos en la lista
        botonVolver = BotonVolver(self, 'volver.png', (50,485))
        self.elementosGUI.append(botonVolver)


class PantallaPausa(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondo_pausa.png')
        botonSalir = BotonSalir(self, 'sair_blanco.png', (302,320))
        botonContinuar = BotonContinuar(self, 'continuar_blanco.png', (590,324))
        self.elementosGUI.append(botonSalir)
        self.elementosGUI.append(botonContinuar)


class PantallaGameover(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondo_gameover.png')
        botonSalir = BotonSalir(self, 'sair_blanco.png', (42,520))
        botonRepetirNivel = BotonRepetirNivel(self, 'denovo.png', (417,252))
        self.elementosGUI.append(botonSalir)
        self.elementosGUI.append(botonRepetirNivel)


class PantallaNivelCompletado(PantallaGUI):
    def __init__(self, menu, nivel):
        PantallaGUI.__init__(self, menu, 'fondo_nivel.png')
        filename = 'nivel' + str(nivel) + '.png'
        tituloNivel = ElementoEstaticoGUI(self, filename, (570,34))
        botonSalir = BotonSalir(self, 'sair_blanco.png', (473,539))
        botonRepetirNivel = BotonRepetirNivel(self, 'denovo.png', (95,260))
        botonSiguienteNivel = BotonSiguienteNivel(self, 'continuar.png', (674,324))
        self.elementosGUI.append(botonSalir)
        self.elementosGUI.append(botonRepetirNivel)
        self.elementosGUI.append(botonSiguienteNivel)
        self.elementosGUI.append(tituloNivel)


# class PantallaJuegoCompletado(PantallaGUI):
#     def __init__(self, menu):
#         PantallaGUI.__init__(self, menu, 'nombre_del_fondo.png')
#         botonSalir = BotonSalir(self, 'sair_blanco.png', (0,0))
#         self.elementosGUI.append(botonSalir)

# -------------------------------------------------
# Clase Menu, que será utilizada por los diferentes tipos de menús del juego

class Menu(Scene):

    def __init__(self, director, pantallas):
        # Llamamos al constructor de la clase padre
        Scene.__init__(self, director)
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        # y las metemos en la lista
        for pantalla in pantallas:
            self.listaPantallas.append(pantalla)
        # Establecemos la pantalla inicial del menú como la pantalla actual
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
    # Metodos genéricos de cualquier menu

    def salirPrograma(self):
        self.director.exitProgram()

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0


class MenuPrincipal(Menu):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre pasándole las distintas
        # pantallas que va a tener el menú
        pantallas = [PantallaInicial(self), PantallaIntrucciones(self)]
        Menu.__init__(self, director, pantallas)

    #--------------------------------------
    # Metodos propios del menu principal del juego

    def ejecutarJuego(self):
        self.director.game_level = 1
        level = fase.Fase(self.director, self.director.game_level)
        self.director.stackScene(level)

    def mostrarIntrucciones(self):
        self.pantallaActual = 1


class MenuPausa(Menu):

    def __init__(self, director):
        pantallas = [PantallaPausa(self)]
        Menu.__init__(self, director, pantallas)

    # Se redefine el método events para incluír la pulsación de la tecla P
    # para continuar el juego
    def events(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    self.salirPrograma()
                elif evento.key == K_p:
                    self.continuarJuego()
            elif evento.type == pygame.QUIT:
                self.director.exitProgram()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].events(lista_eventos)

    # --------------------------------------
    # Metodos propios del menu de pausa
    def continuarJuego(self):
        # Sacamos el menú de pausa de la pila de escenas para continuar el juego
        self.director.exitScene()

class MenuGameover(Menu):

    def __init__(self, director):
        pantallas = [PantallaGameover(self)]
        Menu.__init__(self, director, pantallas)

    # --------------------------------------
    # Metodos propios del menu Gameover
    def repetirNivel(self):
        self.director.exitScene()
        self.director.stackScene(
            fase.Fase(self.director, self.director.game_level))

class MenuNivelCompletado(Menu):

    def __init__(self, director):
        pantallas = [PantallaNivelCompletado(self, director.game_level)]
        Menu.__init__(self, director, pantallas)

    # --------------------------------------
    # Metodos propios del menu de nivel completado
    def repetirNivel(self):
        self.director.exitScene()
        self.director.stackScene(
            fase.Fase(self.director, self.director.game_level))

    def siguienteNivel(self):
        self.director.exitScene()
        self.director.game_level += 1
        self.director.stackScene(
            fase.Fase(self.director, self.director.game_level))


# class MenuJuegoCompletado(Menu):
#
#     def __init__(self, director):
#         pantallas = [PantallaJuegoCompletado(self)]
#         Menu.__init__(self, director, pantallas)