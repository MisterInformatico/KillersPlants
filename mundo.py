import constantes


class Mundo():
    def __init__(self):
        self.level_lenght = []

    def porcesarData(self, data, listaCasilla):
        self.lenghLevel = len(data)
        # Interactuar con cada valor del archivo de data
        for y, fila in enumerate(data):
            for x, casilla in enumerate(fila):
                image = listaCasilla[casilla]
                image_rect = image.get_rect()
                image_x = x * constantes.CASILLAS_SIZE
                image_y = y * constantes.CASILLAS_SIZE
                image_rect.x = image_x
                image_rect.y = image_y
                image_rect.center = (image_x, image_y)
                casillaData = [image, image_rect, image_x, image_y]

                # Pasar la data a la lista principal
                if casilla >= 0:
                    self.level_lenght.append(casillaData)

    def draw(self, pantalla):
        for casilla in self.level_lenght:
            pantalla.blit(casilla[0], casilla[1])
