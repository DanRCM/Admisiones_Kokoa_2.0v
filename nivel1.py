import pygame
import random
from enemigo import Enemigo
from constantes import *

class Pared:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

def crear_enemigos():
    enemigos = []
    paredes = []
    num_enemigos = 3
    num_paredes = 3

    for _ in range(num_enemigos):
        x = random.randint(0, ANCHO_PANTALLA-10)
        y = random.randint(0, ALTO_PANTALLA-10)

        enemigo = Enemigo(x, y)
        enemigos.append(enemigo)

    for _ in range(num_paredes):
        ancho = random.randint(50, 150)
        alto = random.randint(50, 150)
        x = random.randint(0, ANCHO_PANTALLA - ancho)
        y = random.randint(0, ALTO_PANTALLA - alto)
        pared = Pared(x, y, ancho, alto)
        paredes.append(pared)

    return enemigos, paredes