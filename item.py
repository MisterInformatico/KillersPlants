import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, tipoItem, animaciones):
        pygame.sprite.Sprite.__init__(self)
        self.tipoItem = tipoItem # 0: moneda, 1: posion
        self.animaciones = animaciones
        self.frameIndex = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, jugador):
        # Verificar si esta colectando un objeto
        if self.rect.colliderect(jugador.rect):
            # Moneda Colectada
            if self.tipoItem == 0:
                jugador.puntos += 1
            elif self.tipoItem == 1:
                jugador.vida += 10
                if jugador.vida > 100:
                    jugador.vida = 100
            self.kill()

        animacionCoolDown = 150
        # Actualizar imagen
        self.image = self.animaciones[self.frameIndex]
        # Verificar el tiempo
        if pygame.time.get_ticks() - self.update_time > animacionCoolDown:
            self.frameIndex += 1
            self.update_time = pygame.time.get_ticks()
            # Verificar si termino la animacion
            if self.frameIndex >= len(self.animaciones):
                self.frameIndex = 0
    def dibujar(self, pantalla):
        pantalla.blit(self.image, self.rect)
