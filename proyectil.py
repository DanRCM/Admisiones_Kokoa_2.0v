import pygame
import math
import constantes
from enemigo import Enemigo
from constantes import *

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, image, jugador, imagen_bala):
        self.disparo_cooldown = 580
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.imagen.get_rect()
        self.jugador = jugador
        self.disparada = False
        self.ultimodisparo = pygame.time.get_ticks()

    def update(self, jugador):
        bala = None
        offset_x = 28
        offset_y = 0
        self.rect.centerx = self.jugador.rect.centerx + offset_x
        self.rect.centery = self.jugador.rect.centery + offset_y
        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.rect.centerx
        distancia_y = -(mouse_pos[1] - self.rect.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))

        if pygame.mouse.get_pressed()[0] and self.disparada == False and (pygame.time.get_ticks() - self.ultimodisparo >= self.disparo_cooldown):
            bala = Bala(self.rect.centerx,self.rect.centery, self.angulo, self.imagen_bala)
            self.disparada = True
            self.ultimodisparo = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] == False:
            self.disparada = False
        return bala
    
    def dibujar(self, pantalla):
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        pantalla.blit(self.imagen, self.rect)



class Bala(pygame.sprite.Sprite):
    def __init__(self,x, y, angle, imagen):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = imagen
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.delta_x = math.cos(math.radians(self.angulo))*20
        self.delta_y = -(math.sin(math.radians(self.angulo))*20)

    def update(self, enemigos):
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y

        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_PANTALLA or self.rect.bottom < 0 or self.rect.top > constantes.ALTO_PANTALLA:
            self.kill()

        for enemigo in enemigos:
            if enemigo.rect.colliderect(self.rect):
                daño = 10
                enemigo.vida -= daño
                self.kill()
                if enemigo.vida == 0:
                    enemigo.kill()
                break

    def dibujar(self, pantalla):
        pantalla.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height()/2)))