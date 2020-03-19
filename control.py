import pygame
from pygame.locals import *

class Control:

    # Acciones que puede realizar un jugador
    def idle(self):
        raise NotImplementedError()

    def jump(self):
        raise NotImplementedError()

    def left(self):
        raise NotImplementedError()

    def right(self):
        raise NotImplementedError()

    def shoot(self):
        raise NotImplementedError()

    # # Métodos para asignar teclas a acciones
    #
    # def assign_jump(self, key):
    #     raise NotImplementedError()
    #
    # def assign_left(self, key):
    #     raise NotImplementedError()
    #
    # def assign_right(self, key):
    #     raise NotImplementedError()
    #
    # def assign_shoot(self, key):
    #     raise NotImplementedError()


class ControlKeyboard(Control):
    key_jump = K_UP
    key_left = K_LEFT
    key_right = K_RIGHT
    key_shoot = K_SPACE

    def idle(self):
        pressedKeys = pygame.key.get_pressed()
        return all(v == 0 for v in pressedKeys[:290])

    def jump(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_jump]

    def left(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_left]

    def right(self):
        pressedKeys = pygame.key.get_pressed()
        return pressedKeys[self.key_right]

    def shoot(self, player, grupoSpritesDinamicos, grupoSprites, scrollx, event):
       
        if event.key == pygame.K_SPACE:
           player.shoot(grupoSpritesDinamicos, grupoSprites, scrollx)