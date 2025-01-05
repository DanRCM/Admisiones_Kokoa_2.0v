import pygame
from constantes import *

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, velocidad):
        super().__init__()
        self.image_original = pygame.image.load("assets/proyectil.png").convert_alpha()
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.image_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.rect = self.image.get_rect()

    def update(self, jugador):
        self.forma.center = jugador.forma.center
    
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.forma)

    def actualizar(self):
        self.rect.x += self.direccion.x * self.velocidad
        self.rect.y += self.direccion.y * self.velocidad

        if self.rect.right < 0 or self.rect.left > ANCHO_PANTALLA or self.rect.top < 0 or self.rect.bottom > ALTO_PANTALLA:
            self.kill()