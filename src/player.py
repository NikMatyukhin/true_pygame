import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def update(self, camera):
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
                max_shift_x = max_shift_x if dist_x >= max_shift_x else dist_x
                max_shift_y = max_shift_y if dist_y >= max_shift_y else dist_y
            max_shift_x = max_shift_x if max_shift_x > 0 else 0
            max_shift_y = max_shift_y if max_shift_y > 0 else 0
            self.rect.move_ip(max_shift_x, max_shift_y)

            


    def bound_world(self, world):
        self.world = world
        return self
