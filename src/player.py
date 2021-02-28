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
        self.rect.move_ip(x, y)
