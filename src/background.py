import pygame


class Background():
    def __init__(self, surface, image, ms, x, y):
        self.surface = surface
        self.image = image
        self.rect = self.image.get_rect()
        self.moving_speed = ms

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
            if self.X2 >= self.rect.width:
                self.X2 = -self.rect.width

        elif keys[pygame.K_RIGHT]:
            self.X1 -= self.moving_speed
            self.X2 -= self.moving_speed
            if self.X1 <= -self.rect.width:
                self.X1 = self.rect.width
            if self.X2 <= -self.rect.width:
                self.X2 = self.rect.width

        self.surface.blit(self.image, (self.X1, self.Y1))
        self.surface.blit(self.image, (self.X2, self.Y2))
