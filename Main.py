import pygame
from jugador import Jugador
from enemigo import Enemigo
from proyectil import Proyectil
from corazones import Corazones
import nivel1 as nivel1  
from constantes import *

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
fondo = pygame.image.load("assets/fondo.png")
fondo = pygame.transform.scale(fondo, (800, 600))
reloj = pygame.time.Clock()

jugador = Jugador()
enemigos, paredes = nivel1.crear_enemigos()
corazon_lleno = pygame.image.load("assets/corazon_lleno.png")
corazon_vacio = pygame.image.load("assets/corazon_vacio.png")
corazones = Corazones(5, corazon_lleno, corazon_vacio, 1, pantalla)

textura_pared = pygame.image.load("assets/textura_pared.png")
arma = Proyectil()

camara_x = 0
camara_y = 0

running = True
while running:

    pantalla.fill(COLOR_FONDO)
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jugador.disparar()

    jugador.actualizar(paredes)
    for proyectil in jugador.proyectiles:
        proyectil.actualizar()
        pantalla.blit(proyectil.image, proyectil.rect)

    jugador.proyectiles = [proyectil for proyectil in jugador.proyectiles if proyectil.rect.y > 0]

    for enemigo in enemigos:
        enemigo.actualizar(jugador,paredes)
        pantalla.blit(enemigo.image, enemigo.rect)
    for pared in paredes:
        pygame.draw.rect(pantalla, (128, 128, 128), pared.rect)
        textura_escalada = pygame.transform.scale(textura_pared, (pared.rect.width, pared.rect.height))
        pantalla.blit(textura_escalada, pared.rect)

    jugador_pos = pygame.math.Vector2(jugador.rect.topleft)
    jugador.rect.topleft = jugador_pos
    for enemigo in enemigos:
        enemigo_pos = pygame.math.Vector2(enemigo.rect.topright)
        enemigo.rect.topright = enemigo_pos

    jugador.dibujar(pantalla)
    for enemigo in enemigos:
        enemigo.dibujar(pantalla)
    corazones.dibujar()

    pantalla.blit(enemigo.image, enemigo.rect)
    pygame.display.flip()
    
    reloj.tick(FPS)

pygame.quit()