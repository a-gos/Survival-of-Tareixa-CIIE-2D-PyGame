import pygame
from scene import *
from MySprite import *

from resourcesmanager import ResourcesManager

class Bullet(MySprite):
    def __init__(self, player, speed, scrollx, damage_level=0.5):
        MySprite.__init__(self)
        # Daño que provoca cada disparo
        self.damage_level = damage_level

        # Carga de la imagen del disparo
        self.image = ResourcesManager.LoadImageCharacter('disparo.png', -1)
        self.rect = self.image.get_rect()

        # Dependiendo de hacia donde mire el jugador se crea el disparo en el
        # lado derecho o en el izquierdo de este
        (posx, posy) = player.position
        if player.looking == RIGHT:
            self.setposition((posx+self.rect.width, player.rect.centery))
        else:
            self.setposition((posx-self.rect.width, player.rect.centery))
        self.setpositionscreen((scrollx, 0))

        # Se comprueba si hay que darle la vuelta al disparo
        self.looking = player.looking
        if self.looking == LEFT:
            self.image = pygame.transform.flip(self.image, 1 ,0)
            speed = -speed

        self.speed = (speed, 0)

    def update(self, platformGroup, enemyGroup, time):
        # Comprueba si sobrepasa los límites de la pantalla
        if self.looking == LEFT and self.rect.right < 0:
            self.kill()
        elif self.looking == RIGHT and self.rect.left > WIDTH_SCREEN:
            self.kill()
        else:
            # Comprueba si colisiona con una plataforma o enemigo
            enemy = pygame.sprite.spritecollideany(self, enemyGroup)
            if enemy is not None:
                self.kill()
                # Al colisionar con un enemigo se le resta vida
                # La comprobación de si el enemigo debe ser eliminado se hace
                # en el método update del enemigo
                enemy.health -= self.damage_level
                print("Health enemy = "+str(enemy.health))
            elif pygame.sprite.spritecollideany(self, platformGroup):
                self.kill()
            else:
                MySprite.update(self, time)
