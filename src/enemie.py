import pygame


class Enemie(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = self.__class__.image
        self.rect = self.__class__.rect.copy()
        self.rect.move_ip(x, y)

    def update(self, camera):
        camera.blit_sprite(self.image, self.rect)

    @classmethod
    def class_init(cls):
        cls.image = pygame.Surface([100, 100])
        cls.image.fill((220, 150, 150))
        cls.rect = cls.image.get_rect()

    @classmethod
    def set_enemies_image(cls):
        pass

    @classmethod
    def set_enemies_rect(cls):
        pass
