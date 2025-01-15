class Corazones:
    def __init__(self, cantidad_inicial, imagen_llena, imagen_vacia, margen, pantalla):
        self.corazones = [imagen_llena] * cantidad_inicial
        self.cant = cantidad_inicial
        self.imagen_llena = imagen_llena
        self.imagen_vacia = imagen_vacia
        self.margen = margen
        self.pantalla = pantalla

    def dibujar(self):
        x = 10
        y = 560
        for corazon in self.corazones:
            self.pantalla.blit(corazon, (x, y))
            x += corazon.get_width() + self.margen

    def perder_vida(self):
        if self.corazones:
            for i, corazon in enumerate(self.corazones):
                if corazon == self.imagen_llena:
                    self.corazones[i] = self.imagen_vacia
                    self.cant -=1
                    return