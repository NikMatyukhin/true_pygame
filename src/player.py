import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.speed = (0, 0)
        self.max_speed = 50
        self.slowK = 2

    def update(self, camera):
        self.move(*self.speed)
        self.slow()
        camera.blit_sprite(self.image, self.rect)

    def move(self, x, y):
        last_rect = self.rect.copy()
        self.rect.move_ip(x, y)
        if (collided_enemies := pygame.sprite.spritecollide(self, self.world.enemies, 0)):
            self.rect = last_rect
            max_shift_x = x
            max_shift_y = y
            for enemie in collided_enemies:
                dist_x = abs(self.rect.centerx - enemie.rect.centerx)
                dist_x -= (self.rect.width + enemie.rect.width) // 2
                dist_y = abs(self.rect.centery - enemie.rect.centery)
                dist_y -= (self.rect.height + enemie.rect.height) // 2
                max_shift_x = max_shift_x if abs(dist_x) >= abs(max_shift_x) else dist_x * normalize(max_shift_x)
                max_shift_y = max_shift_y if abs(dist_y) >= abs(max_shift_y) else dist_y * normalize(max_shift_y)
            self.rect.move_ip(max_shift_x, max_shift_y)

    def go(self, ax, ay):
        x, y = self.speed
        x = x + ax if abs(x + ax) <= self.max_speed else self.max_speed * normalize(ax)
        y = y + ay if abs(y + ay) <= self.max_speed else self.max_speed * normalize(ay)
        self.speed = x, y

    def set_impulse(self, x, y):
        self.speed = x, y

    def slow(self):
        x, y = self.speed
        x = (abs(x) - self.slowK) * normalize(x) if abs(x) >= self.slowK else 0
        y = (abs(y) - self.slowK) * normalize(y) if abs(y) >= self.slowK else 0
        self.speed = x, y

    def bound_world(self, world):
        self.world = world
        return self


def normalize(x):
    return 1 if x > 0 else -1 if x else 0
