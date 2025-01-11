import random
import pyaudio
import numpy as np
import pygame
from constants import ANCHO, ALTO, GRAVEDAD, SALTO_VELOCIDAD, VELOCIDAD_CAIDA_MAXIMA
import resources
import scores

pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Screaming MEOWW")

# Cargar sonidos
sonido_salto = pygame.mixer.Sound(resources.sonido_salto)

# Imágenes
imagen_jugador = pygame.image.load(resources.imagen_jugador)
imagen_jugador_salto = pygame.image.load(resources.imagen_jugador_salto)

imagen_jugador = pygame.transform.scale(imagen_jugador, (100, 100))
imagen_jugador_salto = pygame.transform.scale(imagen_jugador_salto, (100, 100))

plataformaBacon = pygame.image.load(resources.plataformaBacon)
plataformaBacon = pygame.transform.scale(plataformaBacon, (200, 30))  # Escalar según necesidad

# Moneda
fotogramas_moneda = [
    pygame.image.load(f"src/frame-{i}.gif") for i in range(1, 9)  # Ajusta el rango según tus fotogramas
]
fotogramas_moneda = [pygame.transform.scale(frame, (20, 20)) for frame in fotogramas_moneda]

# Fondo
fondo = pygame.image.load(resources.fondo)
fondo = pygame.transform.scale(fondo, (1000, 600))

# Configuración de audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

def obtener_volumen():
    datos = np.frombuffer(stream.read(1024), dtype=np.int16)
    volumen = np.linalg.norm(datos) / 1024
    return volumen

def pantalla_final(puntaje, puntuacion_maxima):
    fuente_perdiste = pygame.font.SysFont(None, 100)  # Fuente grande para el mensaje
    texto_perdiste = fuente_perdiste.render("¡Perdiste!", True, (255, 0, 0))  # Texto en color rojo

    fuente_puntuacion = pygame.font.SysFont(None, 50)
    texto_puntaje = fuente_puntuacion.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    texto_maximo = fuente_puntuacion.render(f"Puntuación Máxima: {puntuacion_maxima}", True, (255, 255, 255))

    pantalla.fill((0, 0, 0))  # Fondo negro
    pantalla.blit(texto_perdiste, (ANCHO // 2 - texto_perdiste.get_width() // 2, ALTO // 2 - 150))
    pantalla.blit(texto_puntaje, (ANCHO // 2 - texto_puntaje.get_width() // 2, ALTO // 2 - 50))
    pantalla.blit(texto_maximo, (ANCHO // 2 - texto_maximo.get_width() // 2, ALTO // 2 + 50))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  
                esperando = False
    pygame.quit()
    exit()

def generar_plataformas(cantidad, ancho_plataforma, alto_plataforma):
    plataformas = []
    posicion_x = 0
    ultima_altura = ALTO - 100  # Altura inicial de la primera plataforma

    for _ in range(cantidad):
        plataformas.append({
            "rect": pygame.Rect(posicion_x, ultima_altura, ancho_plataforma, alto_plataforma),
            "imagen": plataformaBacon,
        })

        # Generar nueva posición aleatoria cercana
        posicion_x += random.randint(200, 350)  # Separación horizontal entre plataformas
        nueva_altura = ultima_altura + random.randint(-70, 70)  # Variación limitada de altura
        # Limitar la altura dentro de un rango válido
        if nueva_altura > ALTO - 70:
            nueva_altura = ALTO - 100
        elif nueva_altura < 100:
            nueva_altura = 150
        ultima_altura = nueva_altura 

    return plataformas

plataformas = generar_plataformas(5, 180, 20)

# Definir las posiciones de las monedas
rect_monedas = [
    pygame.Rect(200, ALTO - 140, 20, 20),  # Moneda 1
    pygame.Rect(ANCHO // 2 + 80, ALTO - 190, 20, 20),  # Moneda 2
    pygame.Rect(ANCHO - 150, ALTO - 240, 20, 20),  # Moneda 3
]

# Fuente para mostrar el puntaje
fuente = pygame.font.SysFont(None, 40)

# Inicializar el puntaje y variables de animación
puntaje = 0 
monedas_recolectadas = 0 
frame_actual = 0  
contador_animacion = 0  # Contador para cambiar fotogramas

# Variable para el desplazamiento del escenario
desplazamiento_x = 0

# Función principal del juego
def juego():
    global puntaje, monedas_recolectadas, frame_actual, contador_animacion, desplazamiento_x
    reloj = pygame.time.Clock()
    jugador_x = 100  
    jugador_y = ALTO - 200
    velocidad_vertical = 0 
    velocidad_horizontal_salto = 0 
    jugador_rect = pygame.Rect(jugador_x, jugador_y, 100, 100)
    jugador_rect_expandido = jugador_rect.inflate(10, 10)

    puntuacion_maxima = scores.leer_puntuacion_maxima()
    ultima_plataforma = None  # Para rastrear la última plataforma donde estuvo el jugador

    corriendo = True
    velocidad_jugador = 0
    en_salto = False

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Detecta el volumen del micrófono
        volumen = obtener_volumen()

        if volumen > 120:  # Umbral para un "grito"
            velocidad_jugador = 8  # El gato avanza con un grito
        elif volumen > 60:  # Umbral para hablar
            velocidad_jugador = 4  # Avanza lentamente con una voz moderada
        else:
            velocidad_jugador = 0  # Si no hay sonido, se detiene

        if volumen > 130 and not en_salto:  # Salta con un volumen fuerte
            en_salto = True
            velocidad_vertical = -SALTO_VELOCIDAD
            velocidad_horizontal_salto = 5
            sonido_salto.play()
        if en_salto:
            jugador_y += velocidad_vertical
            jugador_x += velocidad_horizontal_salto
            velocidad_vertical += GRAVEDAD           
            if velocidad_vertical > VELOCIDAD_CAIDA_MAXIMA:
                velocidad_vertical = VELOCIDAD_CAIDA_MAXIMA 

        sobre_plataforma = False
        for plataforma in plataformas:
            plataforma_rect = plataforma["rect"]
            if (jugador_x + 100 > plataforma_rect.x and
                jugador_x < plataforma_rect.x + plataforma_rect.width and
                jugador_y + 100 >= plataforma_rect.y and
                jugador_y + 100 <= plataforma_rect.y + 20 and
                velocidad_vertical >= 0): 
                sobre_plataforma = True
                jugador_y = plataforma_rect.y - 100
                en_salto = False
                velocidad_vertical = 0

                if ultima_plataforma != plataforma_rect:
                    puntaje += 1
                    ultima_plataforma = plataforma_rect
                break

        if not sobre_plataforma and not en_salto:
            en_salto = True

        if jugador_y > ALTO:
            if puntaje > puntuacion_maxima:
                scores.guardar_puntuacion_maxima(puntaje)
                puntuacion_maxima = puntaje
            pantalla_final(puntaje, puntuacion_maxima)
            corriendo = False

        # Desplazar el escenario
        desplazamiento_x -= velocidad_jugador

        ultima_altura = plataformas[-1]["rect"].y  # Altura de la última plataforma visible

        for plataforma in plataformas:
            plataforma["rect"].x -= velocidad_jugador
            if plataforma["rect"].right < 0: 
                plataforma["rect"].x = random.randint(ANCHO, ANCHO + 300)  # Reaparecer más adelante
                nueva_altura = ultima_altura + random.randint(-70, 70)  # Variación limitada de altura
                if nueva_altura > ALTO - 70:
                    nueva_altura = ALTO - 100
                elif nueva_altura < 100:
                    nueva_altura = 150
                plataforma["rect"].y = nueva_altura  # Asignar nueva altura
                ultima_altura = nueva_altura  # Actualizar última altura

        for moneda_rect in rect_monedas:
            moneda_rect.x -= velocidad_jugador
            if moneda_rect.right < 0:  # Si la moneda sale por el lado izquierdo
                moneda_rect.x = random.randint(ANCHO, ANCHO + 300)  # Reaparecer más adelante
                moneda_rect.y = random.randint(ALTO - 300, ALTO - 100)  # Cambiar altura

        # Animación de las monedas
        contador_animacion += 1
        if contador_animacion >= 5:  # Cambiar fotograma cada 5 iteraciones
            frame_actual = (frame_actual + 1) % len(fotogramas_moneda)
            contador_animacion = 0

        pantalla.blit(fondo, (desplazamiento_x % ANCHO, 0))
        pantalla.blit(fondo, ((desplazamiento_x % ANCHO) - ANCHO, 0))

        if en_salto:
            pantalla.blit(imagen_jugador_salto, (jugador_x, jugador_y))  # Usar imagen de salto
        else:
            pantalla.blit(imagen_jugador, (jugador_x, jugador_y))  # Usar imagen normal
            
        # Dibujar las plataformas
        for plataforma in plataformas:
            pantalla.blit(plataforma["imagen"], plataforma["rect"].topleft)
        
        # Verificar colisiones con monedas
        for moneda_rect in rect_monedas[:]:
            if jugador_rect_expandido.colliderect(moneda_rect):
                rect_monedas.remove(moneda_rect)  
                monedas_recolectadas += 1 

        for moneda_rect in rect_monedas:
            pantalla.blit(fotogramas_moneda[frame_actual], moneda_rect.topleft)

        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (550, 540))

        texto_monedas = fuente.render(f"Monedas: {monedas_recolectadas}", True, (255, 255, 0))
        pantalla.blit(texto_monedas, (550, 570))

        pygame.display.flip()
        reloj.tick(40)

    pygame.quit()
    stream.stop_stream()
    stream.close()
    p.terminate()