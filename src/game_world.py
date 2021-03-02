import pygame


class Game_world():
    def __init__(self, player, platforms=(), bosses=(), enemies=()):
        self.platforms = pygame.sprite.Group(*platforms)
        self.bosses = pygame.sprite.Group(*bosses)
        self.enemies = pygame.sprite.Group(*enemies)
        self.player = player

    def update(self, camera):
        self.platforms.update(camera)
        self.bosses.update(camera)
        self.enemies.update(camera)
        self.player.update(camera)
