import pygame
from scene import *
from MySprite import *

from resourcesmanager import ResourcesManager

class Bullet(MySprite):
    def __init__(self,player,speed, scrollx):
        MySprite.__init__(self)
      #  self.rect = rect
        self.rect = pygame.Rect(4,4, 50, 12)
        (posx, posy) = player.position
        self.setposition((posx, player.rect.centery))
        self.setpositionscreen(( scrollx, 0 ))

        # Establecer la orientación, la posición y la velocidad del sprite
        self.looking = player.looking
        pos_y = player.rect.centery
        if(self.looking == LEFT):
            pos_x = player.rect.left - self.rect.width
            self.setposition((pos_x, pos_y))
            self.image = pygame.transform.flip(self.image, 1, 0)
            speed = -speed
        else:
            pos_x = player.rect.right
            self.setposition((pos_x, pos_y))

        self.speed = (speed,0)
        print("spawn: ", self.position)


    def update(self, platformGroup, enemyGroup, scroll, time):
        # Comprueba si sobrepasa los límites de la pantalla
        if self.looking == LEFT and self.rect.right < 0:
            print("position left: ", self.position, "rect: ", self.rect.right)
            self.kill()
        elif self.looking == RIGHT and self.rect.left > WIDTH_SCREEN:
            print("position right: ", self.position, "rect: ", self.rect.left)
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
