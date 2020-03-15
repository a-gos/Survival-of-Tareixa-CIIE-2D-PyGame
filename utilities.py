import pygame, scene
from MySprite import *

from resourcesmanager import ResourcesManager

class Bullet(MySprite):
    def __init__(self,player,speed, scrollx):
        MySprite.__init__(self)
      #  self.rect = rect
        self.rect = pygame.Rect(4,4, 50, 12)

        self.setposition((player.rect.centerx + scrollx, player.rect.centery ))

        self.looking = player.looking
        self.image = ResourcesManager.LoadImage('characters','disparo.png', -1)
        if(self.looking == LEFT):
            self.image = pygame.transform.flip(self.image, 1 ,0)
            speed = -speed

        self.speed = (speed,0)


    def update(self, platformGroup, time):
        if self.rect.left>0 and self.rect.right<800 and self.rect.bottom>0 and self.rect.top<800:
            MySprite.update(self, time)
