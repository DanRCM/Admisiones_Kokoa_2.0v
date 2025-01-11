def leer_puntuacion_maxima(archivo="puntuacion_maxima.txt"):
    try:
        with open(archivo, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def guardar_puntuacion_maxima(puntuacion, archivo="puntuacion_maxima.txt"):
    with open(archivo, "w") as f:
        f.write(str(puntuacion))
