import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, ms):
        super().__init__()
        self.surface = pygame.Surface((120, 200))
        self.image = image
        self.rect = self.surface.get_rect(center=(200, 500))

        self.floor = 600
        self.screen_width = 1200
        self.player_level = self.floor - self.surface.get_height()

        self.moving_speed = ms
        self.go_to_right = True
        self.vertical_impulse = 0
        self.horizontal_impulse = False

    def update(self):
        keys = pygame.key.get_pressed()

        if self.rect.bottom == self.floor:
            self.horizontal_impulse = False
            if keys[pygame.K_UP]:
                self.vertical_impulse = -14.0

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

        if self.vertical_impulse:
            if int(self.rect.bottom + self.vertical_impulse) > self.floor:
                self.rect.y = self.player_level
                self.vertical_impulse = 0
            elif self.horizontal_impulse:
                if int(self.rect.left - self.moving_speed) < 0:
                    self.horizontal_impulse = False
                    self.rect.move_ip(self.moving_speed if self.go_to_right else 0, self.vertical_impulse)
                elif int(self.rect.right + self.moving_speed) > self.screen_width:
                    self.horizontal_impulse = False
                    self.rect.move_ip(0 if self.go_to_right else -self.moving_speed, self.vertical_impulse)
                else:
                    self.rect.move_ip(self.moving_speed if self.go_to_right else -self.moving_speed, self.vertical_impulse)
            else:
                self.rect.move_ip(0, self.vertical_impulse)
            self.vertical_impulse += 0.98

        elif not self.go_to_right and self.rect.left > 0 and self.horizontal_impulse:
            self.rect.move_ip(-self.moving_speed, 0)
        elif self.go_to_right and self.rect.right < self.screen_width and self.horizontal_impulse:
            self.rect.move_ip(self.moving_speed, 0)
