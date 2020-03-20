import pygame
from scene import *
from MySprite import *


from resourcesmanager import ResourcesManager

DMG_RL = 4
RELOAD_RL = 2000
MAGAZINE_RL = 1
SPEED_RL=0.5

DMG_SG = 2
RELOAD_SG = 1000
MAGAZINE_SG = 2
SPEED_SG=1

DMG_HG = 1
RELOAD_HG = 500
MAGAZINE_HG = 4
SPEED_HG=0.5



class Bullet(MySprite):
    def __init__(self, player, speed, scrollx, damage_level):
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
        print(self.damage_level)
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

class HealthPack(MySprite):
    def __init__(self,  image, position, heal_level=1):
        MySprite.__init__(self)

      
        self.healing = heal_level
        self.image = image

        self.image = ResourcesManager.LoadImageObjects(image, -1)
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.setposition((position))

        
    def update(self, player, time):
        
 

        healing = player.health + self.healing
        if(player.rect.colliderect(self.rect) and (player.health < MAX_HEALTH) ):
            if(healing <= MAX_HEALTH):
                player.health = healing
            else:
                player.health = MAX_HEALTH
            self.kill()
        else:
            MySprite.update(self, time)


class LicorCafe(HealthPack):
    def __init__(self, position):
        HealthPack.__init__(self, 'bottle.png', position, 0.5)

class Chourizo(HealthPack):
    def __init__(self, position):
        HealthPack.__init__(self, 'chorizo.png', position, 1)

class Weapon(MySprite):
    def __init__(self, image, position, dmg, reloadSpeed, magazine, speed):

        
        MySprite.__init__(self)

        self.dmg=dmg
        self.bulletSpeed = speed
        self.reloadSpeed = reloadSpeed
        self.image=image
        self.magazine = magazine
        self.maxAmmo = magazine
        self.lastBullet = pygame.time.get_ticks()
        self.image = ResourcesManager.LoadImageObjects(image, -1)
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()

        

        self.setposition(position)
        print("init")

    
    def update(self,player,time):
      if player.rect.colliderect(self.rect):
          player.weapon = self
          self.kill()
      else: 
          MySprite.update(self, time)


class Handgun(Weapon):
    def __init__(self,position):
        Weapon.__init__(self, 'chorizo.png', position, DMG_HG, RELOAD_HG, MAGAZINE_HG, SPEED_HG)

class RocketLauncher(Weapon):
    def __init__(self,position):
        Weapon.__init__(self, 'chorizo.png', position, DMG_RL, RELOAD_RL, MAGAZINE_RL, SPEED_RL)

class Shotgun(Weapon):
    def __init__(self,position):
        Weapon.__init__(self, 'chorizo.png', position, DMG_SG, RELOAD_SG, MAGAZINE_SG, SPEED_SG)


