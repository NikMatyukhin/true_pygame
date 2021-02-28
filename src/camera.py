import pygame


class Camera():
    def __init__(self, surface):
        self.surface = surface
        self.x = 0
        self.y = 0

    def move(self, x, y):
        self.x += x
        self.y += y

    def blit_sprite(self, source: pygame.Surface, rect: pygame.Rect, **kwargs):
        self.surface.blit(source, (rect.x - self.x, rect.y - self.y), **kwargs)

    def blit(self, source: pygame.Surface, dest: tuple, **kwargs):
        self.surface.blit(source, dest, **kwargs)
