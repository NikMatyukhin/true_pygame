import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image, ms):
        super().__init__()
        self.surface = pygame.Surface((100, 100))
        self.image = image
        self.rect = self.surface.get_rect(center=(100, 550))

        self.floor = 600
        self.player_level = self.floor - self.surface.get_height()
        self.screen_width = 1200
        self.moving_speed = ms
        self.go_to_right = True
        self.vertical_impulse = 0
        self.horizontal_impulse = False

    def update(self):
        keys = pygame.key.get_pressed()

        # проверка что мы стоим на полу и нажали клавишу вверх - начало прыжка
        if self.rect.bottom == self.floor and keys[pygame.K_UP]:

            # обнуляем горизонтальный импульс
            # дабы не прыгать на месте в разные стороны
            self.horizontal_impulse = False

            # если прыгаем налево
            if keys[pygame.K_LEFT]:
                self.horizontal_impulse = True
                if self.go_to_right:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                self.go_to_right = False

            # если прыгаем направо
            elif keys[pygame.K_RIGHT]:
                self.horizontal_impulse = True
                if not self.go_to_right:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                self.go_to_right = True

            # уменьшение импульса... потому что ноль вверху, точно
            # FIXME: Эмпирически выяснено, что это лучший прыжок
            self.vertical_impulse = -10.

        # если вертикальный импульс отличен от нуля
        # (скорее всего отрицательный)
        if self.vertical_impulse:

            # если направление изменено в ПОЛЁТЕ
            if keys[pygame.K_LEFT]:
                if self.go_to_right:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                self.go_to_right = False

            if keys[pygame.K_RIGHT]:
                if not self.go_to_right:
                    self.image = pygame.transform.flip(self.image, 1, 0)
                self.go_to_right = True

            # проверяем не перелетим ли мы пол
            if int(self.rect.bottom + self.vertical_impulse) > self.floor:
                self.rect.y = self.player_level
                self.vertical_impulse = 0
            else:
                # если присутствует горизонтальный импульс
                if self.horizontal_impulse:

                    # проверяем на выход за границы экрана
                    if self.rect.left - self.moving_speed < 0 or self.rect.right + self.moving_speed > self.screen_width:
                        # зануляем импульс вбок, так как упёрлись
                        self.horizontal_impulse = False
                    else:
                        # сдвигаем по диагонали
                        self.rect.move_ip(self.moving_speed if self.go_to_right else -self.moving_speed,
                                          self.vertical_impulse)
                else:
                    # сдвигаем строго вертикально
                    self.rect.move_ip(0, self.vertical_impulse)
                # FIXME: почему так? откуда снова магические константы?
                self.vertical_impulse += 0.98

        # если внутри экрана и нажато влево
        elif self.rect.left >= 0 and keys[pygame.K_LEFT]:
            # двигаем влево и по надобности флипаем картинку
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = False

        # если внутри экрана и нажато вправо
        elif self.rect.right <= self.screen_width and keys[pygame.K_RIGHT]:
            # двигаем влево и по надобности флипаем картинку
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = True
