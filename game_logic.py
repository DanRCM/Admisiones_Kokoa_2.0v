import random
import pyaudio
import numpy as np
import pygame
from constants import ANCHO, ALTO, GRAVEDAD, SALTO_VELOCIDAD, VELOCIDAD_CAIDA_MAXIMA, MARGEN_IZQUIERDO, MARGEN_DERECHO
import resources
import scores


pygame.mixer.init()
# Cargar sonidos
sonido_salto = pygame.mixer.Sound(resources.sonido_salto)

# Imágenes
imagen_jugador = pygame.image.load(resources.imagen_jugador)
imagen_jugador_salto = pygame.image.load(resources.imagen_jugador_salto)

imagen_jugador = pygame.transform.scale(imagen_jugador, (100, 100))
imagen_jugador_salto = pygame.transform.scale(imagen_jugador_salto, (100, 100))



# Moneda
fotogramas_moneda = [
    pygame.image.load(f"src/frame-{i}.gif") for i in range(1, 9)  # Ajusta el rango según tus fotogramas
]
fotogramas_moneda = [pygame.transform.scale(frame, (20, 20)) for frame in fotogramas_moneda]

# Fondo
fondo = pygame.image.load(resources.fondo_1)
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

def pantalla_final(puntaje, puntuacion_maxima,pantalla):
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

def generar_plataformas(cantidad, imagen_plataforma):
    plataformas = []
    ancho_plataforma = imagen_plataforma.get_width() # Obtener ancho de la imagen
    alto_plataforma = imagen_plataforma.get_height()  # Obtener alto de la imagen
    posicion_x = 0
    ultima_altura = ALTO - 100

    for _ in range(cantidad):
        ancho_adicional = random.randint(0,50)
        imagen_redimensionada = pygame.transform.scale(imagen_plataforma, (ancho_plataforma + ancho_adicional, alto_plataforma))
        es_desmoronable = random.choice([True, False])
        plataformas.append({
            "rect": pygame.Rect(posicion_x, ultima_altura, ancho_plataforma + ancho_adicional, alto_plataforma),
            "imagen": imagen_redimensionada,
            "desmoronable": es_desmoronable,
            "opacidad": 255,
            "tocada": False,
            "ancho": ancho_plataforma + ancho_adicional
        })

        posicion_x += random.randint(200, 250)  # Separación horizontal aleatoria entre plataformas

        nueva_altura = ultima_altura + random.randint(-60, 60)

        # Limitar altura de la nueva plataforma dentro de un rango aceptable
        if nueva_altura > ALTO - 70:
            nueva_altura = ALTO - 100
        elif nueva_altura < 100:
            nueva_altura = 150

        ultima_altura = nueva_altura

    return plataformas


# Definir las posiciones de las monedas
rect_monedas = [
    pygame.Rect(200, ALTO - 140, 20, 20),  # Moneda 1
    pygame.Rect(ANCHO // 2 + 80, ALTO - 190, 20, 20),  # Moneda 2
    pygame.Rect(ANCHO - 150, ALTO - 240, 20, 20),  # Moneda 3
]

fondos = [
    pygame.transform.scale(pygame.image.load(resources.fondo_1), (1000, 600)),
    pygame.transform.scale(pygame.image.load(resources.fondo_2), (1000, 600)),
    pygame.transform.scale(pygame.image.load(resources.fondo_3), (1000, 600)),
    pygame.transform.scale(pygame.image.load(resources.fondo_4), (1000, 600)),
    pygame.transform.scale(pygame.image.load(resources.fondo_5), (1000, 600))
]

def juego(pantalla,fuente):
    global puntaje, monedas_recolectadas, frame_actual, contador_animacion, desplazamiento_x
    reloj = pygame.time.Clock()
    plataformaBacon = pygame.image.load(resources.plataformaBacon+"255.png")
    plataformaBacon = pygame.transform.scale(plataformaBacon, (160, 30))
    plataformas = generar_plataformas(50, plataformaBacon)
    proyectiles=[]
    contador_cambio_fondo = 0 
    puntaje = 0
    desplazamiento_x = 0
    monedas_recolectadas = 0 
    frame_actual = 0  
    contador_animacion = 0 
    fondo_actual = 0 
    jugador_x = 0  
    jugador_y = ALTO - 200
    velocidad_vertical = 0 
    velocidad_horizontal_salto = 0 
    
    jugador_rect = pygame.Rect(jugador_x + 50, jugador_y, 50, 100)
    #jugador_rect_expandido = jugador_rect.inflate(10, 10)
    genero_Moneda = 0
    puntuacion_maxima = scores.leer_puntuacion_maxima()
    ultima_plataforma = None

    corriendo = True
    velocidad_jugador = 0
    en_salto = False

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Detecta el volumen del micrófono
        volumen = obtener_volumen()

        contador_cambio_fondo += 1
        if contador_cambio_fondo >= 500: 
            fondo_actual = (fondo_actual + 1) % len(fondos)
            contador_cambio_fondo = 0

        if volumen >160 and not en_salto:
            en_salto = True
            velocidad_vertical = -SALTO_VELOCIDAD
            velocidad_horizontal_salto = 7
            sonido_salto.play()
        elif volumen > 120:  # Umbral para hablar
            velocidad_jugador = 8  # Avanza lentamente con una voz moderada
        elif volumen > 60:
            velocidad_jugador = 4
        else:
            velocidad_jugador = 0  # Si no hay sonido, se detiene
        
        sobre_plataforma = False
        for plataforma in plataformas:
            plataforma_rect = plataforma["rect"]
            # Verificar si la base del jugador está en contacto con la plataforma
            if (
                jugador_rect.bottom >= plataforma_rect.top and  # La base del jugador toca el tope de la plataforma
                jugador_rect.bottom <= plataforma_rect.top + 15 and  # Margen para asegurar la colisión
                jugador_rect.centerx > plataforma_rect.left and  # El centro del jugador está dentro de los límites horizontales
                jugador_rect.centerx < plataforma_rect.right and
                velocidad_vertical >= 0  # Solo si el jugador está cayendo
            ):
                sobre_plataforma = True
                jugador_y = plataforma_rect.top - jugador_rect.height  # Ajustar posición para que el jugador esté sobre la plataforma
                en_salto = False
                velocidad_vertical = 0  # Detener la velocidad vertical

                if ultima_plataforma != plataforma_rect:
                    puntaje += 1
                    ultima_plataforma = plataforma_rect
                break

        # Si el jugador no está sobre ninguna plataforma, activar el estado de salto
        if not sobre_plataforma and not en_salto:
            en_salto = True
        
  
        if en_salto:
            jugador_x += velocidad_horizontal_salto
            jugador_y += velocidad_vertical           
            velocidad_vertical += GRAVEDAD           
            if velocidad_vertical > VELOCIDAD_CAIDA_MAXIMA:
                velocidad_vertical = VELOCIDAD_CAIDA_MAXIMA 

            sobre_plataforma = False
            for plataforma in plataformas:
                plataforma_rect = plataforma["rect"]
                if (
                        jugador_rect.bottom >= plataforma_rect.top and  # La base del jugador toca el tope de la plataforma
                        jugador_rect.bottom <= plataforma_rect.top and
                        jugador_rect.centerx > plataforma_rect.left and  # El centro del jugador está dentro de los límites horizontales
                        jugador_rect.centerx < plataforma_rect.right and
                        velocidad_vertical >= 0  # Solo si el jugador está cayendo
                    ):
                    sobre_plataforma = True
                    jugador_y = plataforma_rect.y - 100  # Ajustar posición para que el jugador esté justo sobre la plataforma
                    en_salto = False
                    velocidad_vertical = 0  # Detener el movimiento hacia abajo
                    velocidad_horizontal_salto = 0  # Detener el movimiento horizontal del salto


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
            pantalla_final(puntaje, puntuacion_maxima,pantalla)
            corriendo = False

        if jugador_x > ANCHO - MARGEN_DERECHO:  # Si el gato se acerca al margen derecho
            jugador_x = ANCHO - MARGEN_DERECHO
            desplazamiento_x -= velocidad_jugador  # Desplaza el escenario hacia la izquierda
        else:
            jugador_x += velocidad_jugador  # El gato puede moverse libremente dentro del margen

        ultima_altura = max(plataforma["rect"].y for plataforma in plataformas)
        ultima_posicionX = max(plataforma["rect"].x for plataforma in plataformas)

        for plataforma in plataformas:
            plataforma["rect"].x -= velocidad_jugador

            if plataforma["rect"].right < 0: 
                plataforma["rect"].x = ultima_posicionX + random.randint(ANCHO, ANCHO + 125)  

                nueva_altura = ultima_altura + random.randint(-70, 70)
                
                # Limitar la altura dentro del rango permitido
                if nueva_altura > ALTO - 70:  # Altura máxima cercana al suelo
                    nueva_altura = ALTO - 100
                elif nueva_altura < 100:  # Altura mínima cercana al techo
                    nueva_altura = 150
                
                plataforma["rect"].y = nueva_altura  # Asignar nueva altura
                ultima_altura = nueva_altura  # Actualizar última altura

                if random.randint(0, 1):  # 50% de probabilidad
                    moneda_x = plataforma["rect"].x + random.randint(20, plataforma["rect"].width - 20)
                    moneda_y = plataforma["rect"].y - 30
                    rect_monedas.append(pygame.Rect(moneda_x, moneda_y, 20, 20))
                


        jugador_rect.topleft = (jugador_x + 20, jugador_y)
        jugador_rect_expandido = jugador_rect.inflate(10, 10)

        for plataforma in plataformas:
            if plataforma["desmoronable"] and jugador_rect.colliderect(plataforma["rect"]):
                plataforma["tocada"] = True

        for plataforma in plataformas[:]:
            if plataforma["desmoronable"] and plataforma["tocada"]:
                plataforma["opacidad"] -= 2
                if plataforma["opacidad"] > 200:
                    nueva_imagen  = pygame.image.load(resources.plataformaBacon+"255.png")
                elif plataforma["opacidad"] > 150:
                    nueva_imagen = pygame.image.load(resources.plataformaBacon+"150.png")
                elif plataforma["opacidad"] > 100:
                    nueva_imagen = pygame.image.load(resources.plataformaBacon+"100.png")
                else:
                    nueva_imagen = pygame.image.load(resources.plataformaBacon+"50.png")
                
                nueva_imagen = pygame.transform.scale(nueva_imagen, (plataforma["ancho"], 30))
                plataforma["imagen"] = nueva_imagen
                
                if plataforma["opacidad"] <= 0:
                    plataformas.remove(plataforma)


        for moneda_rect in rect_monedas:
            moneda_rect.x -= velocidad_jugador
            if moneda_rect.right < 0:  
                moneda_rect.x = random.randint(ANCHO, ANCHO + 300) 
                moneda_rect.y = random.randint(ALTO - 300, ALTO - 100)

        # Animación de las monedas
        contador_animacion += 1
        if contador_animacion >= 5:
            frame_actual = (frame_actual + 1) % len(fotogramas_moneda)
            contador_animacion = 0

        pantalla.blit(fondos[fondo_actual], (desplazamiento_x, 0))  # Fondo principal
        pantalla.blit(fondos[fondo_actual], (desplazamiento_x + ANCHO, 0))  # Fondo adicional

        desplazamiento_x -= velocidad_jugador
        if desplazamiento_x <= -ANCHO:  # Si el fondo principal se ha movido completamente fuera de la pantalla
            desplazamiento_x = 0  # Reiniciar desplazamiento


        if en_salto:
            pantalla.blit(imagen_jugador_salto, (jugador_x, jugador_y)) 
        else:
            pantalla.blit(imagen_jugador, (jugador_x, jugador_y)) 
            
        for plataforma in plataformas:
            superficie = pygame.Surface(plataforma["rect"].size, pygame.SRCALPHA)
            #pygame.draw.rect(pantalla, (255, 0, 0), plataforma["rect"], 2)
            color = (255, 0, 0) if plataforma["desmoronable"] else (0, 255, 0) 
            #superficie.fill((*color, max(0, int(plataforma["opacidad"]))))  
            pantalla.blit(superficie, plataforma["rect"].topleft)
            pantalla.blit(plataforma["imagen"], plataforma["rect"].topleft)

        #pygame.draw.rect(pantalla, (0, 255, 0), jugador_rect, 2)
        
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