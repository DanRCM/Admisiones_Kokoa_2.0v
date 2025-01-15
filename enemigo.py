import pygame
import random
from constantes import *

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/enemigo.png").convert_alpha(),(40,50))
        self.rect = self.image.get_rect()
        self.vida = 20
        self.rect.x = x
        self.rect.y = y
        self.velocidad = 3
        self.velocidad_aleatoria = random.uniform(-1, 1)
        self.velocidad_x = 0
        self.velocidad_y = 0

    def actualizar(self, jugador, paredes):
        direccion_x = jugador.rect.x - self.rect.x
        direccion_y = jugador.rect.y - self.rect.y

        if self.vida <= 0:
            self.vida = 0
            self.kill()

        distancia = ((direccion_x ** 2) + (direccion_y ** 2)) ** 0.5
        if distancia > 0:
            direccion_x /= distancia
            direccion_y /= distancia

        self.velocidad_x = direccion_x * self.velocidad + self.velocidad_aleatoria
        self.velocidad_y = direccion_y * self.velocidad

        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        for pared in paredes:
            if self.rect.colliderect(pared.rect):
                if self.velocidad_x > 0 and self.rect.right > pared.rect.left:
                    self.rect.right = pared.rect.left
                    self.velocidad_x = 0
                elif self.velocidad_x < 0 and self.rect.left < pared.rect.right:
                    self.rect.left = pared.rect.right
                    self.velocidad_x = 0
                if self.velocidad_y > 0 and self.rect.bottom > pared.rect.top:
                    self.rect.bottom = pared.rect.top
                    self.velocidad_y = 0
                elif self.velocidad_y < 0 and self.rect.top < pared.rect.bottom:
                    self.rect.top = pared.rect.bottom
                    self.velocidad_y = 0

        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA))

    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)