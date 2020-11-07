import os
import sys
import pygame
import enemy
import background

# полезные константы
FPS = 30
WIN_HEIGHT = 700
WIN_WIDTH = 1200
FLOOR_HEIGHT = 100

# рабочие директории
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assets')
enemy_folder = os.path.join(img_folder, 'enemies')
sound_folder = os.path.join(game_folder, 'sounds')
music_folder = os.path.join(game_folder, 'music')

# инициализация модулей pygame
pygame.init()

# создаем объект главной поверхности
main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# изображения, ассеты и спрайты
floor_images = [pygame.image.load(os.path.join(img_folder, f'new_floor_back_{i}.png')) for i in range(1, 4)]
ceil_images = [pygame.image.load(os.path.join(img_folder, f'new_ceil_back_{i}.png')) for i in range(1, 4)]
police_enemy_image = pygame.image.load(os.path.join(enemy_folder, 'police_cut.png')).convert_alpha()

# создаём тестового противника
enemy = enemy.Enemy(police_enemy_image, 1, 400, 500)

# создаем объект часов задержки
fps_clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.all_images = [pygame.image.load(os.path.join(img_folder, f'player_mop_{i}.png')).convert_alpha() for i in range(1, 9)]
        self.image = self.all_images[0]
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.rect = self.surface.get_rect(center=(400, 500))

        self.floor = 600
        self.screen_width = 1200
        self.player_level = self.floor - self.surface.get_height()

        self.moving_speed = 5
        self.go_to_right = True
        self.vertical_impulse = 0
        self.horizontal_impulse = False

        self.attack = False
        self.attack_moment = 0

    def start_attack(self):
        self.attack = True

    def update(self):
        keys = pygame.key.get_pressed()

        if self.rect.bottom == self.floor:
            self.horizontal_impulse = False
            self.vertical_impulse = 0
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

        if self.attack:
            self.attack_moment = (self.attack_moment + 1) % 8
            self.image = self.all_images[self.attack_moment] if self.go_to_right else pygame.transform.flip(self.all_images[self.attack_moment], 1, 0) 
            if not self.attack_moment:
                self.attack = False

        main_surface.blit(player.image, player.rect)


class Background():
    def __init__(self, images, x, y):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.order = (0, 1, 1, 2, 0, 1, 1, 0, 2, 1, 1, 1, 1)
        self.moving_speed = 5

        self.first = 0
        self.second = 1

        self.Y1 = y
        self.X1 = x

        self.Y2 = y
        self.X2 = self.rect.width

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.X1 += self.moving_speed
            self.X2 += self.moving_speed
            if self.X1 >= self.rect.width:
                self.X1 = -self.rect.width
                self.first = 12 if (pos := self.first - 2) < 0 else pos
            if self.X2 >= self.rect.width:
                self.X2 = -self.rect.width
                self.second = 12 if (pos := self.second - 2) < 0 else pos

        elif keys[pygame.K_RIGHT]:
            self.X1 -= self.moving_speed
            self.X2 -= self.moving_speed
            if self.X1 <= -self.rect.width:
                self.X1 = self.rect.width
                self.first = (self.first + 2) % 13
            if self.X2 <= -self.rect.width:
                self.X2 = self.rect.width
                self.second = (self.second + 2) % 13

        main_surface.blit(self.images[self.order[self.first]], (self.X1, self.Y1))
        main_surface.blit(self.images[self.order[self.second]], (self.X2, self.Y2))


background_floor = Background(floor_images, 0, WIN_HEIGHT - FLOOR_HEIGHT)
background_ceil = Background(ceil_images, 0, 0)
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.start_attack()

    background_floor.update()
    background_ceil.update()
    main_surface.blit(enemy.image, enemy.rect)
    player.update()
    enemy.update(player.rect.centerx, player.rect.centery)

    # обновление экрана
    pygame.display.update()

    # задержка
    fps_clock.tick(FPS)
