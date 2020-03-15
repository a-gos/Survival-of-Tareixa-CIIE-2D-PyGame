import pygame
import sys
import os

# Clase MySprite
# MOVEMENT
IDLE = 0
LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
# ANIMATIONS
SPRITE_IDLE = 0
SPRITE_WALKING = 1
SPRITE_JUMPING = 2
# SPRITE_SHOOTING = 3

BULLET_SPEED = (1,0)
# Character SETTINGS
Character_SPEED = 0.2  # Pixeles per milisecond
Character_JUMP_SPEED = 0.3  # Pixeles per milisecond
Character_ANIMATION_DELAY = 5  # updates that the character model will endure
                            # should be a different number for each animation

GRAVITY = 0.0005

class MySprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)
        self.speed = (0, 0)
        self.scroll = (0, 0)

    def setposition(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    def setpositionscreen(self, scrollDecorado):
        self.scroll = scrollDecorado
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.position
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def increaseposition(self, incremento):
        (posx, posy) = self.position
        (incrementox, incrementoy) = incremento
        self.setposition((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.speed[0]*tiempo
        incrementoy = self.speed[1]*tiempo
        self.increaseposition((incrementox, incrementoy))
