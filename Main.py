import pygame
from game_logic import juego
import menu 
import constants

def main():
    pygame.init()
    fuente = pygame.font.SysFont(None, 40)
    pantalla = pygame.display.set_mode((constants.ANCHO, constants.ALTO))
    pygame.display.set_caption("Screaming MEOWW")
    menu.menu_inicio(pantalla)
    juego(pantalla,fuente)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] Ha ocurrido un problema: {e}")
