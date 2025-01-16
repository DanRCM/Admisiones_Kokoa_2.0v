import pygame 
import constants
import resources

def menu_inicio(pantalla):
    pantalla_menu = True
    fondo_menu = pygame.image.load(resources.fondo_menu)
    fondo_menu = pygame.transform.scale(fondo_menu, (constants.ANCHO, constants.ALTO)) 
    fuente_titulo = pygame.font.SysFont(None, 80)  # Fuente para el título
    fuente_opciones = pygame.font.SysFont(None, 50)  # Fuente para las opciones

    texto_iniciar = fuente_opciones.render("             ", True, (255, 255, 255))
    texto_salir = fuente_opciones.render("             ", True, (255, 255, 255))
    rect_iniciar = texto_iniciar.get_rect(center=(constants.ANCHO // 2, 365))
    rect_salir = texto_salir.get_rect(center=(constants.ANCHO // 2, 445))

    while pantalla_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_iniciar.collidepoint(evento.pos):
                    pantalla_menu = False
                if rect_salir.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

        pantalla.blit(fondo_menu, (0, 0))  # Dibujar el fondo del menú

        pantalla.blit(texto_iniciar, rect_iniciar.topleft)
        pantalla.blit(texto_salir, rect_salir.topleft)

        pygame.display.flip()

        pygame.display.flip()

