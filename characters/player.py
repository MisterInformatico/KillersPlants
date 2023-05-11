import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, screenW, screenH):
        super().__init__()
        self.x = screenW
        self.y = screenH