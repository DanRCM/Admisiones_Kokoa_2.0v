#Autor: Isaac Criollo Córdova
#Ninja Survivor es un juego del tipo rougue like con vista desde arriba, se trata de sobrevivir contra enemigos que te persiguen
#Cada partida es diferente debido a que las paredes en el juego se generan aletaoriamente en cada partida!


import pygame
from jugador import Jugador
from enemigo import Enemigo
from proyectil import Proyectil
from corazones import Corazones
import nivel1 as nivel1
import time
from constantes import *

def mostrar_mensaje(mensaje, negro):
    font = pygame.font.Font(None, 36)
    text = font.render(mensaje, True, (255, 255, 255))
    text_rect = text.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
    pantalla.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(1)
    if negro == 1:
        pygame.draw.rect(pantalla, COLOR_NEGRO, text_rect)
        pygame.display.flip()

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

enemigos_muertos = []
enemigos = nivel1.crear_enemigos(limites)
paredes = nivel1.crearParedes(limites)
corazon_lleno = pygame.image.load("assets/corazon_lleno.png")
corazon_vacio = pygame.image.load("assets/corazon_vacio.png")
corazones = Corazones(5, corazon_lleno, corazon_vacio, 1, pantalla)

textura_pared = pygame.image.load("assets/textura_pared.png")

mostrar_mensaje("¡Ninja Survivor! Preparate para sobrevivir",1)
time.sleep(0.3)
mostrar_mensaje("¡Te mueves con WASD y el mouse!",1)

running = True
while running:

    reloj.tick(FPS)
    pantalla.fill(COLOR_FONDO)
    pantalla.blit(fondo, (0, 0))

    if not enemigos:
        mostrar_mensaje("¡Has ganado, Gracias por Jugar!", 0)
        time.sleep(1)
        running = False

    elif corazones.cant <= 0:
        mostrar_mensaje("¡Has perdido!", 0)
        time.sleep(1)
        running = False

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
        if enemigo.vida <= 0:
            enemigos_muertos.append(enemigo)

    if enemigos_muertos != 0:
        for enemigo in enemigos_muertos:
            enemigos.remove(enemigo)
    enemigos_muertos.clear()

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