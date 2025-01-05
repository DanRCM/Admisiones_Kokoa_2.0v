import pygame
from proyectil import Proyectil
from constantes import *

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        self.flipH = True
        self.flipV = True
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/playerCentro.png").convert_alpha(),(40,50))
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
        self.velocidad= 5
        self.tiempo_ultimo_disparo = 0
        self.tiempo_entre_disparos = 1000
        self.vidas = 5
        self.daño = 10
        self.proyectiles = []
        self.direccion = pygame.Vector2(0, -1)
        self.velocidad_proyectil = 10
        self.velocidad_x = 0
        self.velocidad_y = 0

    def actualizar(self, paredes):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            self.velocidad_x = -self.velocidad
        elif teclas[pygame.K_d]:
            self.velocidad_x = self.velocidad
        else:
            self.velocidad_x = 0

        if teclas[pygame.K_w]:
            self.velocidad_y = -self.velocidad
        elif teclas[pygame.K_s]:
            self.velocidad_y = self.velocidad
        else:
            self.velocidad_y = 0

        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        for pared in paredes:
            if self.rect.colliderect(pared.rect):
                if self.velocidad_x > 0:
                    self.rect.right = pared.rect.left
                    self.velocidad_x = 0
                elif self.velocidad_x < 0:
                    self.rect.left = pared.rect.right
                    self.velocidad_x = 0
                if self.velocidad_y > 0:
                    self.rect.bottom = pared.rect.top
                    self.velocidad_y = 0
                elif self.velocidad_y < 0:
                    self.rect.top = pared.rect.bottom
                    self.velocidad_y = 0

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)