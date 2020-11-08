import os
import sys
from typing import List

import pygame
from random import randint

FPS = 30
WIN_HEIGHT = 700
WIN_WIDTH = 1200
FLOOR_HEIGHT = 100
DISTANCE = 400

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assets')
enemy_folder = os.path.join(img_folder, 'enemies')
boss_folder = os.path.join(img_folder, '5g_tower')
sound_folder = os.path.join(game_folder, 'sounds')
music_folder = os.path.join(game_folder, 'music')

pygame.init()

main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

floor_images = [pygame.image.load(os.path.join(img_folder, f'new_floor_back_{i}.png')) for i in range(1, 4)]
ceil_images = [pygame.image.load(os.path.join(img_folder, f'new_ceil_back_{i}.png')) for i in range(1, 4)]
police_enemy_image = pygame.image.load(os.path.join(enemy_folder, 'police_cut.png')).convert_alpha()
wanted = pygame.image.load(os.path.join(img_folder, f'разыскивается.png')).convert_alpha()
trash = pygame.image.load(os.path.join(img_folder, f'урна.png')).convert_alpha()

fps_clock = pygame.time.Clock()

pygame.mixer.music.load(os.path.join(music_folder, 'main_theme.mp3'))
pygame.mixer.music.play(-1)
moap = pygame.mixer.Sound(os.path.join(sound_folder, 'moap.wav'))
pain = [pygame.mixer.Sound(os.path.join(sound_folder, f'oh{i}.wav')) for i in range (1, 5)]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.all_images = [pygame.image.load(os.path.join(img_folder, f'player_mop_{i}.png')).convert_alpha() for i in
                           range(1, 9)]
        print([im.get_width() for im in self.all_images])
        self.image = self.all_images[0]
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.rect = self.surface.get_rect(center=(400, 500))

        self.floor = WIN_HEIGHT - FLOOR_HEIGHT
        self.player_level = self.floor - self.surface.get_height()

        self.moving_speed = 10
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
                self.vertical_impulse = -16.0

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
                elif int(self.rect.right + self.moving_speed) > WIN_WIDTH:
                    self.horizontal_impulse = False
                    self.rect.move_ip(0 if self.go_to_right else -self.moving_speed, self.vertical_impulse)
                else:
                    self.rect.move_ip(self.moving_speed if self.go_to_right else -self.moving_speed,
                                      self.vertical_impulse)
            else:
                self.rect.move_ip(0, self.vertical_impulse)
            self.vertical_impulse += 0.98

        elif not self.go_to_right and self.rect.left > 0 and self.horizontal_impulse:
            self.rect.move_ip(-self.moving_speed, 0)

        elif self.go_to_right and self.rect.right < WIN_WIDTH and self.horizontal_impulse:
            self.rect.move_ip(self.moving_speed, 0)

        if self.attack:
            self.attack_moment = (self.attack_moment + 1) % 8
            if self.attack_moment == 5:
                moap.play()
            self.image = self.all_images[self.attack_moment] if self.go_to_right else pygame.transform.flip(
                self.all_images[self.attack_moment], 1, 0)
            if not self.attack_moment:
                self.attack = False

        main_surface.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surface = pygame.Surface((120, 200))
        self.image = pygame.transform.scale(
            pygame.image.load(os.path.join(enemy_folder, 'police_cut.png')).convert_alpha(), (120, 200))
        self.rect = self.surface.get_rect(center=(x, y))
        self.damage_inicator = pygame.transform.scale(
            pygame.image.load(os.path.join(enemy_folder, 'police_damage.png')).convert_alpha(), (120, 200))

        self.moving_speed = randint(2, 4)
        self.go_to_right = False
        self.hp = 7
        self.attack = False
        self.damage = 0

    def hit(self, direction):
        self.hp -= 1
        self.damage = 1
        if self.hp == 0:
            self.kill()
        else:
            self.rect.move_ip(self.moving_speed * randint(5, 15) + 40 if direction else -self.moving_speed * randint(5, 15) + 40, 0)
            pain[randint(0,3)].play()

    def update(self):
        if player.rect.centerx > self.rect.centerx:
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = True
        elif player.rect.centerx < self.rect.centerx:
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = False
        main_surface.blit(self.image, self.rect)
        if self.damage: 
            main_surface.blit(self.damage_inicator, self.rect)
            self.damage += 1
        if self.damage > 4:
            self.damage = 0

    def move(self, direction, motion):
        if motion:
            self.rect.move_ip(-background_ceil.moving_speed if direction
                              else background_ceil.moving_speed, 0)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surface = pygame.Surface((404, 438))
        self.all_images = [pygame.transform.scale(pygame.image.load(os.path.join(boss_folder, f'5g_tower_{i}.png')),
                                                  (404, 438)).convert_alpha() for i in range(5)]
        print([im.get_width() for im in self.all_images])
        self.image = self.all_images[0]
        self.rect = self.surface.get_rect(center=(x, y))

        self.moving_speed = 8
        self.go_to_right = False
        self.hp = 30
        self.attack = False
        self.attack_moment = 0

    def hit(self, direction):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
        else:
            self.rect.move_ip(self.moving_speed * randint(5, 15) if direction else -self.moving_speed * randint(5, 15), 0)

    def update(self):
        global player
        if player.rect.centerx > self.rect.centerx:
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = True
        elif player.rect.centerx < self.rect.centerx:
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.go_to_right = False
        if player.rect.left <= self.rect.left <= player.rect.right \
                or player.rect.left <= self.rect.right <= player.rect.right:
            self.attack = True
        if self.attack:
            self.attack_moment = (self.attack_moment + 1) % 8
            self.image = self.all_images[self.attack_moment // 2] if not self.go_to_right else pygame.transform.flip(
                self.all_images[self.attack_moment // 2], 1, 0)
            if not self.attack_moment:
                self.attack = False
        main_surface.blit(self.image, self.rect)

    def move(self, direction, motion):
        if motion:
            self.rect.move_ip(-background_ceil.moving_speed if direction
                              else background_ceil.moving_speed, 0)


class Background():
    def __init__(self, images, x, y):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.order = (0, 1, 1, 2, 0, 1, 1, 0, 0, 1, 1, 1, 1)
        self.moving_speed = 10

        self.first = 0
        self.second = 1

        self.Y1 = y
        self.X1 = x

        self.Y2 = y
        self.X2 = self.rect.width

    def move(self):
        global DISTANCE
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.X1 += self.moving_speed
            self.X2 += self.moving_speed
            DISTANCE -= self.moving_speed
            if self.X1 >= self.rect.width:
                self.X1 = -self.rect.width
                self.first = 12 if (pos := self.first - 2) < 0 else pos
            if self.X2 >= self.rect.width:
                self.X2 = -self.rect.width
                self.second = 12 if (pos := self.second - 2) < 0 else pos

        elif keys[pygame.K_RIGHT]:
            self.X1 -= self.moving_speed
            self.X2 -= self.moving_speed
            DISTANCE += self.moving_speed
            if self.X1 <= -self.rect.width:
                self.X1 = self.rect.width
                self.first = (self.first + 2) % 13
            if self.X2 <= -self.rect.width:
                self.X2 = self.rect.width
                self.second = (self.second + 2) % 13

    def update(self):
        main_surface.blit(self.images[self.order[self.first]], (self.X1, self.Y1))
        main_surface.blit(self.images[self.order[self.second]], (self.X2, self.Y2))


background_floor = Background(floor_images, 0, WIN_HEIGHT - FLOOR_HEIGHT)
background_ceil = Background(ceil_images, 0, 0)
player = Player()

enemies = pygame.sprite.AbstractGroup()
activity_distance = [3500, 3600, 6900, 7000, 9800, 10000, 13000, 13100, 18000] 

font = pygame.font.SysFont('arial', 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.start_attack()

    if player.rect.left - player.moving_speed < 0 and DISTANCE > 400 or player.rect.right + player.moving_speed > WIN_WIDTH and DISTANCE < 20000:
        background_floor.move()
        background_ceil.move()
        keys = pygame.key.get_pressed()
        direction = bool(keys[pygame.K_RIGHT] or not keys[pygame.K_LEFT])
        motion = bool(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])
        for enemy in enemies:
            enemy.move(direction, motion)

    background_floor.update()
    background_ceil.update()

    if activity_distance:
        if activity_distance[0] - DISTANCE < 200:
            activity_distance.pop(0)
            x, y = 1200, 500
            if len(activity_distance) == 0:
                enemies.add(Boss(x, y))
                pygame.mixer.music.load(os.path.join(music_folder, 'boss_theme.mp3'))
                pygame.mixer.music.play(-1)
            else:
                enemies.add(Enemy(x, y))
    for enemy in enemies:
        enemy.update()

    player.update()

    dir = 0 if player.go_to_right else 50
    absolute_pos = DISTANCE - 2 * (WIN_WIDTH - player.rect.centerx - dir)

    if 6200 > absolute_pos > 6000:
        main_surface.blit(wanted, (50, 50))

    if 100 > absolute_pos > -160:
        main_surface.blit(trash, (50, 50))

    hit_list = pygame.sprite.spritecollide(player, enemies, False)
    if hit_list and player.attack:
        for hitted in hit_list:
            hitted.hit(player.go_to_right)

    pygame.display.update()

    fps_clock.tick(FPS)
