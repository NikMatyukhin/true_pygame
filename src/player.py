import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, ms, sw):
        super().__init__()
        self.surface = pygame.Surface((100, 100))
        self.image = image
        self.rect = self.surface.get_rect(center=(100, 550))

        self.screen_width = sw
        self.moving_speed = ms
        self.go_to_right = True

    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = False
        if self.rect.right < self.screen_width and keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = True
