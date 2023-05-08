import pygame
import math
import constantes


class Jugador:
    def __init__(self, x, y, vida, animaciones, tipoDeMob):
        self.tipoDeMob = tipoDeMob
        self.puntos = 0
        self.flip = False
        self.animaciones = animaciones[tipoDeMob]
        self.frameIndex = 0 # controla el index de las animaciones
        self.accion = 0 # 0:idle y 1:run
        self.corriendo = False
        self.vida = vida
        self.vivo = True
        self.update_time = pygame.time.get_ticks()
        self.imagen = self.animaciones[self.accion][self.frameIndex]
        self.rect = pygame.Rect(0, 0, constantes.CASILLAS_SIZE, constantes.CASILLAS_SIZE)
        self.rect.center = (x, y)


    def move(self, dx, dy):
        self.corriendo = False
        # Verificar si el jugador esta caminando
        if dx != 0 or dy != 0:
            self.corriendo = True
        # Verificar si el Jugador esta mirando a la derecha o a la Izquierda
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
        # Controlar la velocidad diagonal
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

        self.rect.x += dx
        self.rect.y += dy

    def actualizar(self):

        # Verificar si murio
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False

        # Verificar la accion del jugador
        if self.corriendo == True:
            self.actualizarAccion(1)
        else:
            self.actualizarAccion(0)

        tiempoAnimaciones = 70
        self.imagen = self.animaciones[self.accion][self.frameIndex]
        # verificar el tiempo de animacion
        if pygame.time.get_ticks() - self.update_time > tiempoAnimaciones:
            self.frameIndex += 1
            self.update_time = pygame.time.get_ticks()
        #verificar si llego a la ultima animacion
        if self.frameIndex >= len(self.animaciones[self.accion]):
            self.frameIndex = 0
    def actualizarAccion(self, nuevaAccion):
        # Verificar si es una nueva accion
        if nuevaAccion != self.accion:
            self.accion = nuevaAccion
            # Actualizar las configuraciones de las animaciones
            self.frameIndex = 0
            self.update_time = pygame.time.get_ticks()

    def dibujar(self, pantalla):
        flippedImagen = pygame.transform.flip(self.imagen, self.flip, False)
        if self.tipoDeMob == 0:
            pantalla.blit(flippedImagen, (self.rect.x, self.rect.y - constantes.ESCALA * constantes.OFFSET))
        else:
            pantalla.blit(flippedImagen, self.rect)
        pygame.draw.rect(pantalla, constantes.ROJO, self.rect, 1)
