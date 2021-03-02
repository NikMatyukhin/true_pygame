import pygame


class Game_object(pygame.sprite.Sprite):
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
        cls.image.fill((150, 150, 150))
        cls.rect = cls.image.get_rect()

    @classmethod
    def set_class_image(cls, image: pygame.Surface):
        cls.image = image

    @classmethod
    def set_class_rect(cls, rect: pygame.Rect):
        cls.rect = rect
