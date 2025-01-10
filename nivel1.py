import pygame
import random
from enemigo import Enemigo
from constantes import *

def dentro_de_limites(rect, limites):
    for limite in limites:
        if rect.colliderect(limite):
            return True
    return False
class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

def crear_enemigos(limites):
    enemigos = []
    num_enemigos = 3

    for _ in range(num_enemigos):   
        x = random.randint(limites[0].left, limites[0].right)
        y = random.randint(limites[0].top, limites[0].bottom)

        enemigo = Enemigo(x, y)
        while not dentro_de_limites(enemigo.rect, limites):
            x = random.randint(limites[0].left, limites[0].right)
            y = random.randint(limites[0].top, limites[0].bottom)
            enemigo.rect.x = x
            enemigo.rect.y = y
        enemigos.append(enemigo)

    return enemigos


def crearParedes(limites):
    paredes = []
    num_paredes = 3
    for _ in range(num_paredes):
        ancho = random.randint(50, 150)
        alto = random.randint(50, 150)
        x = random.randint(limites[0].left, limites[0].right)
        y = random.randint(limites[0].top, limites[0].bottom)
        
        pared = Pared(x, y, ancho, alto)
        while not dentro_de_limites(pared.rect, limites):
            x = random.randint(limites[0].left, limites[0].right)
            y = random.randint(limites[0].top, limites[0].bottom)
            pared.rect.x = x
            pared.rect.y = y

        paredes.append(pared)
    
    return paredes


def mantener_dentro_limites(objeto, ancho_pantalla, alto_pantalla):
    if objeto.rect.left < 0:
        objeto.rect.left = 0
    elif objeto.rect.right > ancho_pantalla:
        objeto.rect.right = ancho_pantalla
    if objeto.rect.top < 0:
        objeto.rect.top = 0
    elif objeto.rect.bottom > alto_pantalla:
        objeto.rect.bottom = alto_pantalla