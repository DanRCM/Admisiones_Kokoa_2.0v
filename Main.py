import pygame
from jugador import Jugador
from enemigo import Enemigo
from proyectil import Proyectil
from corazones import Corazones
import nivel1 as nivel1  
from constantes import *

#FALTA SISTEMA DE COLISIONES ENEMIGOS, PROYECTIL, MENU, GAMEOVER POR PERDIDA DE VIDAS
#FALTA COMENTARIO AUTOR Y MODULARIZAR FUNCIONES

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
fondo = pygame.image.load("assets/fondo.png")
fondo = pygame.transform.scale(fondo, (800, 600))
reloj = pygame.time.Clock()
limites = [pygame.Rect(100, 100, 500, 400)]

imagen_pistola = pygame.transform.scale(pygame.image.load("assets/proyectil.png").convert_alpha(),(95,90))
imagen_bala = pygame.image.load("assets/proyectil2.png").convert_alpha()
jugador = Jugador()
proyectil = Proyectil(imagen_pistola, jugador, imagen_bala)

grupo_balas = pygame.sprite.Group()


enemigos = nivel1.crear_enemigos(limites)
paredes = nivel1.crearParedes(limites)
corazon_lleno = pygame.image.load("assets/corazon_lleno.png")
corazon_vacio = pygame.image.load("assets/corazon_vacio.png")
corazones = Corazones(5, corazon_lleno, corazon_vacio, 1, pantalla)

textura_pared = pygame.image.load("assets/textura_pared.png")

running = True
while running:
    reloj.tick(FPS)

    pantalla.fill(COLOR_FONDO)
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    jugador.actualizar(paredes,enemigos,corazones)
    nivel1.mantener_dentro_limites(jugador, ANCHO_PANTALLA, ALTO_PANTALLA)
    bala = proyectil.update(jugador)
    if bala:
        grupo_balas.add(bala)

    for bala in grupo_balas:
        bala.update(enemigos)

    for enemigo in enemigos:
        enemigo.actualizar(jugador,paredes)
        nivel1.mantener_dentro_limites(enemigo, ANCHO_PANTALLA, ALTO_PANTALLA)
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
    proyectil.dibujar(pantalla)
    for bala in grupo_balas:
        bala.dibujar(pantalla)

    for enemigo in enemigos:
        enemigo.dibujar(pantalla)

    corazones.dibujar()
    pygame.display.flip()

pygame.quit()