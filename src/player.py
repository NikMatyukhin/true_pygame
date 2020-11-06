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
        self.vertical_impulse = 0
        self.horizontal_impulse = False

    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom == 600. and keys[pygame.K_UP]:
            self.horizontal_impulse = False
            if keys[pygame.K_LEFT]:
                self.horizontal_impulse = True
                if self.go_to_right:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                self.go_to_right = False
            elif keys[pygame.K_RIGHT]:
                self.horizontal_impulse = True
                if not self.go_to_right:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                self.go_to_right = True
            self.vertical_impulse = -14.
        if self.vertical_impulse:
            if self.rect.bottom + self.vertical_impulse > 600:
                self.rect.y = 550.
                self.vertical_impulse = 0
            else:
                if self.horizontal_impulse:
                    self.rect.move_ip(self.moving_speed if self.go_to_right else -self.moving_speed, self.vertical_impulse)
                else:
                    self.rect.move_ip(0, self.vertical_impulse)
                self.vertical_impulse += 0.98
        elif self.rect.left > 0 and keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = False
        elif self.rect.right < self.screen_width and keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = True
