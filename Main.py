import pygame
from game_logic import juego

def main():
    juego()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] Ha ocurrido un problema: {e}")
