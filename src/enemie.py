import pygame

from game_object import Game_object


class Enemie(Game_object):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = self.__class__.image
        self.rect = self.__class__.rect.copy()
        self.rect.move_ip(x, y)

    def update(self, camera):
        camera.blit_sprite(self.image, self.rect)

    def think_n_move(self, player):
        pass

    def attack(self):
        pass

    def reverse_image(self):
        if self.image is self.__class__.image:
            self.image = self.__class__.reverse_image
        else:
            self.image = self.__class__.image

    @classmethod
    def class_init(cls):
        cls.image = pygame.Surface([100, 100])
        cls.image.fill((220, 150, 150))
        cls.reverse_image = pygame.Surface([100, 100])
        cls.image.fill((200, 130, 130))
        cls.rect = cls.image.get_rect()

    @classmethod
    def set_class_rev_image(cls, image: pygame.Surface):
        cls.reverse_image = image
