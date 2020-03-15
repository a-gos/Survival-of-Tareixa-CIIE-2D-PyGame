import pygame, scene
from MySprite import *

from resourcesmanager import ResourcesManager

class Bullet(MySprite):
    def __init__(self,player,speed):
        MySprite.__init__(self)
      #  self.rect = rect
        self.rect = pygame.Rect(4,4, 50, 12)

        self.setposition((player.rect.centerx, player.rect.centery ))

        self.looking = player.looking
        self.image = ResourcesManager.LoadImage('characters','disparo.png', -1)
        if(self.looking == LEFT):
            self.image = pygame.transform.flip(self.image, 1 ,0)
            speed = -speed

        self.speed = (speed,0)


    def update(self, platformGroup, enemyGroup, scroll, time):
        # Comprueba si sobrepasa los límites de la pantalla
        if self.looking == LEFT and self.rect.right < scroll[0]:
            self.kill()
        elif self.looking == RIGHT and self.rect.left > scroll[1]:
            self.kill()
        else:
            # Comprueba si colisiona con una plataforma o enemigo
            enemy = pygame.sprite.spritecollideany(self, enemyGroup)
            if enemy is not None:
                self.kill()
                # RESTAR VIDA DEL ENEMIGO O ELIMINARLO
            elif pygame.sprite.spritecollideany(self, platformGroup):
                self.kill()
            else:
                MySprite.update(self, time)
