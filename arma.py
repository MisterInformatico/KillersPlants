import random

import pygame
import math

import constantes


class Arma():
    def __init__(self, imagen, imagenFlecha):
        self.imagenOriginal = imagen #se guarda la imagen sin angulo
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagenOriginal, self.angulo)
        self.rect = self.imagen.get_rect()
        self.imagenFlecha = imagenFlecha
        self.fire = False
        self.ultimoDisparo = pygame.time.get_ticks()
    def actualizar(self, jugador):
        disparoCoolDown = 300
        flecha = None

        self.rect.center = jugador.rect.center

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angulo = math.degrees(math.atan2(y_dist, x_dist))

        if pygame.mouse.get_pressed()[0] and self.fire == False and (pygame.time.get_ticks() - self.ultimoDisparo) >= disparoCoolDown:
            flecha = Flecha(self.imagenFlecha, self.rect.centerx, self.rect.centery, self.angulo)
            self.fire = True
            self.ultimoDisparo = pygame.time.get_ticks()
        # Reset Click
        if pygame.mouse.get_pressed()[0] == False:
            self.fire = False
        return flecha
    def dibujar(self, pantalla):
        self.imagen = pygame.transform.rotate(self.imagenOriginal, self.angulo)
        pantalla.blit(self.imagen, ((self.rect.centerx - int(self.imagen.get_width()/2)), self.rect.centery - self.imagen.get_height()/2))

class Flecha(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angulo):
        pygame.sprite.Sprite.__init__(self)
        self.imagenOriginal = image
        self.angulo = angulo
        self.image = pygame.transform.rotate(self.imagenOriginal, self.angulo - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Calcular la rapidez verticalmente y horizontalmente basado en el angulo
        self.dx = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_FLECHA
        self.dy = -(math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_FLECHA)

    def actualizar(self, enemigoLista):
        # Inicializar Variables
        damage = 0
        damagePos = None
        # re posicion basado en la velocidad
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Verificar colision de la flecha y el enemigo
        for enemigo in enemigoLista:
            if enemigo.rect.colliderect(self.rect) and enemigo.vivo:
                damage = 10 * random.randint(-5, 5)
                damagePos = enemigo.rect
                enemigo.vida -= damage
                self.kill()
                break

        return damage, damagePos

        # Verificar si la flecha se ve en la pantalla
        if self.rect.right < 0 or self.rect.left > constantes.anchoPantalla or self.rect.bottom < 0 or self.rect.top > constantes.altoPantalla:
            self.kill()

    def dibujar(self, pantalla):
        pantalla.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - self.image.get_height() / 2))
