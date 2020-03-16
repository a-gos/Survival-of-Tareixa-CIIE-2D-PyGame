import pygame
from scene import *
from MySprite import *

from resourcesmanager import ResourcesManager

class Bullet(MySprite):
    def __init__(self,player,speed, scrollx):
        MySprite.__init__(self)
        self.image = ResourcesManager.LoadImage('characters','disparo.png', -1)

        self.rect = self.image.get_rect()
        (posx, posy) = player.position
        if(player.looking == RIGHT):
            self.setposition((posx+self.rect.width, player.rect.centery))
        else:
            self.setposition((posx-self.rect.width, player.rect.centery))
        self.setpositionscreen(( scrollx, 0 ))

        self.looking = player.looking
        if(self.looking == LEFT):
            self.image = pygame.transform.flip(self.image, 1 ,0)
            speed = -speed

        self.speed = (speed,0)
        # print("spawn: ", self.position)
    #

    def update(self, platformGroup, enemyGroup, scroll, time):
        # Comprueba si sobrepasa los límites de la pantalla
        if self.looking == LEFT and self.rect.right < 0:
            # print("position left: ", self.position, "rect: ", self.rect.right)
            self.kill()
        elif self.looking == RIGHT and self.rect.left > WIDTH_SCREEN:
            # print("position right: ", self.position, "rect: ", self.rect.left)
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