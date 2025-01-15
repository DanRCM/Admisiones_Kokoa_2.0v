import pygame
from proyectil import Proyectil
from constantes import *

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/abajo1.png").convert_alpha(),(40,50))
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
        self.velocidad= 5
        self.tiempo_ultimo_disparo = 0
        self.tiempo_entre_disparos = 1000
        self.vidas = 5
        self.daño = 10
        self.direccion = pygame.Vector2(0, -1)
        self.velocidad_x = 0
        self.velocidad_y = 0

        self.imagenes = {
            "abajo": [pygame.transform.scale(pygame.image.load("assets/abajo1.png").convert_alpha(),(40,50)), pygame.transform.scale(pygame.image.load("assets/abajo2.png").convert_alpha(),(40,50)),pygame.transform.scale(pygame.image.load("assets/abajo3.png").convert_alpha(),(40,50))],
            "arriba": [pygame.transform.scale(pygame.image.load("assets/arriba1.png").convert_alpha(),(40,50)), pygame.transform.scale(pygame.image.load("assets/arriba2.png").convert_alpha(),(40,50)),pygame.transform.scale(pygame.image.load("assets/arriba3.png").convert_alpha(),(40,50))],
            "derecha": [pygame.transform.scale(pygame.image.load("assets/derecha1.png").convert_alpha(),(40,50)), pygame.transform.scale(pygame.image.load("assets/derecha2.png").convert_alpha(),(40,50)),pygame.transform.scale(pygame.image.load("assets/derecha3.png").convert_alpha(),(40,50))],
            "izquierda": [pygame.transform.scale(pygame.image.load("assets/izquierda1.png").convert_alpha(),(40,50)), pygame.transform.scale(pygame.image.load("assets/izquierda2.png").convert_alpha(),(40,50)),pygame.transform.scale(pygame.image.load("assets/izquierda3.png").convert_alpha(),(40,50))]
        }
        self.animacion_actual = "abajo"
        self.indice_imagen = 0
        self.tiempo_ultimo_cambio = 0
        self.tiempo_entre_cambios = 100


    def actualizar(self, paredes, enemigos, corazones):
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

        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_ultimo_cambio > self.tiempo_entre_cambios:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes[self.animacion_actual])
            self.tiempo_ultimo_cambio = ahora

        if self.velocidad_y > 0:
            self.animacion_actual = "abajo"
        elif self.velocidad_y < 0:
            self.animacion_actual = "arriba"
        elif self.velocidad_x > 0:
            self.animacion_actual = "derecha"
        elif self.velocidad_x < 0:
            self.animacion_actual = "izquierda"

        self.image = self.imagenes[self.animacion_actual][self.indice_imagen]

        for enemigo in enemigos:
            if self.rect.colliderect(enemigo.rect):
                corazones.perder_vida()
                # Calcular la dirección del retroceso
                direccion_x = self.rect.x - enemigo.rect.x
                direccion_y = self.rect.y - enemigo.rect.y
                # Aplicar el retroceso
                self.rect.x -= direccion_x * 10  # Ajusta el valor 10 para controlar la fuerza del retroceso
                self.rect.y -= direccion_y * 10


    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)