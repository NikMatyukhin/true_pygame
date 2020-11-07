import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, ms, x, y):
        super().__init__()
        self.surface = pygame.Surface((120, 200))
        self.image = pygame.transform.scale(image, (120, 200))
        self.rect = self.surface.get_rect(center=(x, y))

        self.moving_speed = ms
        self.go_to_right = False

    def update(self, px, py):
        if px > self.rect.centerx:
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = True
        elif px < self.rect.centerx:
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = False
