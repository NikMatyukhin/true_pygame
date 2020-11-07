import pygame


class Background():
    def __init__(self, surface, images, ms, x, y):
        self.surface = surface
        self.images = images
        self.rect = self.images[0].get_rect()
        self.order = (0, 1, 1, 2, 0, 1, 1, 0, 2, 1, 1, 1, 1)
        self.moving_speed = ms

        self.first = 0
        self.second = 1

        self.Y1 = y
        self.X1 = x

        self.Y2 = y
        self.X2 = self.rect.width

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.X1 += self.moving_speed
            self.X2 += self.moving_speed
            if self.X1 >= self.rect.width:
                self.X1 = -self.rect.width
                self.first = 12 if (pos := self.first - 2) < 0 else pos
            if self.X2 >= self.rect.width:
                self.X2 = -self.rect.width
                self.second = 12 if (pos := self.second - 2) < 0 else pos

        elif keys[pygame.K_RIGHT]:
            self.X1 -= self.moving_speed
            self.X2 -= self.moving_speed
            if self.X1 <= -self.rect.width:
                self.X1 = self.rect.width
                self.first = (self.first + 2) % 13
            if self.X2 <= -self.rect.width:
                self.X2 = self.rect.width
                self.second = (self.second + 2) % 13

        self.surface.blit(self.images[self.order[self.first]], (self.X1, self.Y1))
        self.surface.blit(self.images[self.order[self.second]], (self.X2, self.Y2))
