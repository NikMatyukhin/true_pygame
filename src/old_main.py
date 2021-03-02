import os
import sys
import pygame
from random import randint

FPS = 30
WIN_HEIGHT = 700
WIN_WIDTH = 1200
FLOOR_HEIGHT = 100
DISTANCE = 400
CURRENT_TIME = None
KILLS = 0

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assets')
enemy_folder = os.path.join(img_folder, 'enemies')
boss_folder = os.path.join(img_folder, 'bosses/5g_tower')
player_folder = os.path.join(img_folder, 'main_hero')
sound_folder = os.path.join(game_folder, 'sounds')
music_folder = os.path.join(game_folder, 'music')

pygame.init()

main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

floor_images = [pygame.image.load(os.path.join(img_folder, f'backgrounds/new_floor_back_{i}.png')) for i in range(1, 4)]
ceil_images = [pygame.image.load(os.path.join(img_folder, f'backgrounds/new_ceil_back_{i}.png')) for i in range(1, 4)]
hp_bar_img = pygame.image.load(os.path.join(img_folder, f'hpbar.png'))
wanted = pygame.image.load(os.path.join(img_folder, f'разыскивается.png')).convert_alpha()
trash = pygame.image.load(os.path.join(img_folder, f'урна.png')).convert_alpha()

# предзагрузка ресурсов полицейских
policeman_images = [pygame.transform.scale(pygame.image.load(os.path.join(enemy_folder, f'policeman/police_{i}_frame.png')),
                                           (174, 200)).convert_alpha() for i in range(9)]
policeman_attack_mask_image = pygame.transform.scale(
            pygame.image.load(os.path.join(enemy_folder, 'policeman/police_attack_mask.png')), (174, 200))
policeman_damage_indicator = pygame.transform.scale(
            pygame.image.load(os.path.join(enemy_folder, 'policeman/police_damage.png')).convert_alpha(), (174, 200))

# предзагрузка ресурсов босса
boss_images = [pygame.transform.scale(pygame.image.load(os.path.join(boss_folder, f'5g_tower_{i}.png')),
                                                  (404, 438)).convert_alpha() for i in range(5)]
boss_attack_mask = pygame.transform.scale(
            pygame.image.load(os.path.join(boss_folder, '5g_tower_attack_mask.png')), (404, 438))
boss_damage_indicator = [pygame.transform.scale(pygame.image.load(os.path.join(boss_folder, f'{i}_hit_5g_tower.png')),
                                                  (404, 438)).convert_alpha() for i in range(5)]

fps_clock = pygame.time.Clock()

pygame.mixer.music.load(os.path.join(music_folder, 'main_theme.mp3'))
pygame.mixer.music.play(-1)
moap = pygame.mixer.Sound(os.path.join(sound_folder, 'moap.wav'))
pain = [pygame.mixer.Sound(os.path.join(sound_folder, f'oh{i}.wav')) for i in range (1, 5)]
activity_distance = [3500, 3600, 6900, 7000, 9800, 10000, 13000, 13100, 18000] 
boss_pain = [pygame.mixer.Sound(os.path.join(sound_folder, f'boss_damage_{i}.wav')) for i in range (0, 2)]
boss_hit = [pygame.mixer.Sound(os.path.join(sound_folder, f'boss_hit_{i}.wav')) for i in range (0, 2)]
boss_death = pygame.mixer.Sound(os.path.join(sound_folder, f'boss_death.wav'))

font = pygame.font.SysFont('arial', 22)
final_font = pygame.font.SysFont('arial', 16)
final_font.set_bold(True)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.all_images = [pygame.image.load(os.path.join(player_folder, f'mop/player_mop_{i}.png')).convert_alpha() for i in
                           range(1, 9)]
        self.image = self.all_images[0]
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.rect = self.surface.get_rect(center=(400, 500))
        self.right_hitbox = pygame.mask.from_surface(hit_img := pygame.image.load(os.path.join(player_folder, 'mop/player_mop_hitbox.png')))
        self.left_hitbox = pygame.mask.from_surface(pygame.transform.flip(hit_img, 1, 0))
        self.right_attack_mask = pygame.mask.from_surface(atc_img := pygame.image.load(os.path.join(player_folder, 'mop/player_mop_attack_mask.png')))
        self.left_attack_mask = pygame.mask.from_surface(pygame.transform.flip(atc_img, 1, 0))

        self.floor = WIN_HEIGHT - FLOOR_HEIGHT
        self.player_level = self.floor - self.surface.get_height()

        self.hp = 100
        self.moving_speed = 8
        self.go_to_right = True
        self.vertical_impulse = 0
        self.horizontal_impulse = False
        self.locked = False

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
            elif not player.locked and self.horizontal_impulse:
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

        elif not player.locked and not self.go_to_right and self.rect.left > 0 and self.horizontal_impulse:
            self.rect.move_ip(-self.moving_speed, 0)

        elif not player.locked and self.go_to_right and self.rect.right < WIN_WIDTH and self.horizontal_impulse:
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

    def hit(self, direction):
        global final_window
        self.hp -= 3
        if self.hp <= 0:
            final_window = FinalWindow()
            pygame.mixer.music.load(os.path.join(music_folder, 'main_theme.mp3'))
            pygame.mixer.music.play(-1)
        else:
            self.rect.move_ip(self.moving_speed * randint(1, 5) if direction else -self.moving_speed * randint(1, 5), 0)

    def get_hitbox(self):
        return self.right_hitbox if self.go_to_right else self.left_hitbox

    def get_attack_mask(self):
        return self.right_attack_mask if self.go_to_right else self.left_attack_mask


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surface = pygame.Surface((174, 200))
        self.all_images = policeman_images
        self.image = self.all_images[0]
        self.rect = self.surface.get_rect(center=(x, y))
        self.left_hitbox = pygame.mask.from_surface(self.image)
        self.right_hitbox = pygame.mask.from_surface(pygame.transform.flip(self.image, 1, 0))
        self.left_attack_mask = pygame.mask.from_surface(policeman_attack_mask_image)
        self.right_attack_mask = pygame.mask.from_surface(pygame.transform.flip(policeman_attack_mask_image, 1, 0))
        self.damage_indicator = policeman_damage_indicator

        self.moving_speed = randint(1, 5)
        self.go_to_right = False
        self.hp = 7
        self.attack = False
        self.attack_moment = 0
        self.damage = 0

    def hit(self, direction):
        global KILLS
        self.hp -= 1
        self.damage = 1
        if self.hp == 0:
            self.kill()
            KILLS += 1
        else:
            self.rect.move_ip(self.moving_speed * randint(5, 15) + 40 if direction else -self.moving_speed * randint(5, 15) - 40, 0)
            pain[randint(0, 3)].play()

    def update(self):
        if player.rect.centerx > self.rect.centerx:
            self.rect.move_ip(self.moving_speed, 0)
            if not self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.damage_indicator = pygame.transform.flip(self.damage_indicator, 1, 0)
            self.go_to_right = True
        elif player.rect.centerx < self.rect.centerx:
            self.rect.move_ip(-self.moving_speed, 0)
            if self.go_to_right:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self.damage_indicator = pygame.transform.flip(self.damage_indicator, 1, 0)
            self.go_to_right = False
        if self.go_to_right and player.rect.left <= self.rect.right <= player.rect.right:
            self.attack = True
        elif not self.go_to_right and player.rect.left <= self.rect.left <= player.rect.right:
            self.attack = True
        if self.attack:
            self.attack_moment = (self.attack_moment + 1) % 8
            self.image = self.all_images[self.attack_moment] if not self.go_to_right else pygame.transform.flip(
                self.all_images[self.attack_moment], 1, 0)
            if not self.attack_moment:
                self.attack = False
        main_surface.blit(self.image, self.rect)
        if self.damage:
            main_surface.blit(self.damage_indicator, self.rect)
            self.damage += 1
        if self.damage > 4:
            self.damage = 0

    def move(self, direction, motion):
        if motion:
            self.rect.move_ip(-background_ceil.moving_speed if direction
                              else background_ceil.moving_speed, 0)

    def get_hitbox(self):
        return self.right_hitbox if self.go_to_right else self.left_hitbox

    def get_attack_mask(self):
        return self.right_attack_mask if self.go_to_right else self.left_attack_mask


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surface = pygame.Surface((404, 438))
        self.all_images = boss_images
        self.image = self.all_images[0]
        self.rect = self.surface.get_rect(center=(x, y))
        self.left_hitbox = pygame.mask.from_surface(self.image)
        self.right_hitbox = pygame.mask.from_surface(pygame.transform.flip(self.image, 1, 0))
        self.left_attack_mask = pygame.mask.from_surface(boss_attack_mask)
        self.right_attack_mask = pygame.mask.from_surface(pygame.transform.flip(boss_attack_mask, 1, 0))
        self.damage_indicator = boss_damage_indicator

        self.moving_speed = 7
        self.go_to_right = False
        self.hp = 30
        self.damage = 0
        self.attack = False
        self.attack_moment = 0

    def hit(self, direction):
        global KILLS
        global final_window
        self.hp -= 1
        self.damage = 1
        if self.hp <= 0:
            self.kill()
            KILLS += 1
            boss_death.play()
            final_window = FinalWindow()
            pygame.mixer.music.load(os.path.join(music_folder, 'main_theme.mp3'))
            pygame.mixer.music.play(-1)
        else:
            self.rect.move_ip(self.moving_speed * randint(5, 15) if direction else -self.moving_speed * randint(5, 15), 0)
            boss_pain[randint(0, 1)].play()

    def start_attack(self):
        self.attack = True
        if (a := randint(0, 10)) < 2:
            boss_hit[a].play()

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
            self.start_attack()
        if self.attack:
            self.attack_moment = (self.attack_moment + 1) % 8
            self.image = self.all_images[self.attack_moment // 2] if not self.go_to_right else pygame.transform.flip(
                self.all_images[self.attack_moment // 2], 1, 0)
            if not self.attack_moment:
                self.attack = False
        main_surface.blit(self.image, self.rect)
        if self.damage:
            main_surface.blit(self.damage_indicator[self.attack_moment // 2], self.rect)
            self.damage += 1
        if self.damage > 4:
            self.damage = 0

    def move(self, direction, motion):
        if motion:
            self.rect.move_ip(-background_ceil.moving_speed if direction
                              else background_ceil.moving_speed, 0)

    def get_hitbox(self):
        return self.right_hitbox if self.go_to_right else self.left_hitbox

    def get_attack_mask(self):
        return self.right_attack_mask if self.go_to_right else self.left_attack_mask


class FinalWindow():
    def __init__(self):
        global CURRENT_TIME
        global player
        global KILLS
        self.kills = final_font.render(str(KILLS).rjust(11, ' '), 0, (212, 255, 119))
        self.time = final_font.render(f'{CURRENT_TIME // 60000:02}:{CURRENT_TIME % 60000 // 1000:02}:{CURRENT_TIME % 1000:02}', 0, (212, 255, 119))
        self.damage = final_font.render(f'{100 - player.hp} hp'.rjust(10, ' '), 0, (212, 255, 119))
        self.surface = pygame.image.load(os.path.join(img_folder, 'final.png')).convert_alpha()
        self.rect = self.surface.get_rect(center=(600, 350))

    def update(self):
        main_surface.blit(self.surface, (450, 0))
        main_surface.blit(self.time, (655, 346))
        main_surface.blit(self.kills, (655, 372))
        main_surface.blit(self.damage, (655, 398))


class Background():
    def __init__(self, images, x, y):
        self.images = images
        self.rect = self.images[0].get_rect()
        self.order = (0, 1, 1, 2, 0, 1, 1, 0, 0, 1, 1, 1, 1)
        self.moving_speed = 8

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


final_window = None
background_floor = Background(floor_images, 0, WIN_HEIGHT - FLOOR_HEIGHT)
background_ceil = Background(ceil_images, 0, 0)
player = Player()

enemies = pygame.sprite.AbstractGroup()

while True:
    player.locked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.image.save(main_surface, "screenshot.jpg")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.start_attack()

    if final_window is None:
        keys = pygame.key.get_pressed()
        if not enemies and keys[pygame.K_RIGHT] and 400 <= DISTANCE < 20000 and player.rect.right >= WIN_HEIGHT:
            background_floor.move()
            background_ceil.move()
            player.rect.move_ip(-player.moving_speed, 0)
            player.locked = True
        elif not enemies and 400 <= DISTANCE < 20000 and player.rect.left > 200 and player.rect.right < WIN_HEIGHT:
            background_floor.move()
            background_ceil.move()
            player.locked = True
        elif player.rect.left - player.moving_speed < 0 and DISTANCE > 400 or player.rect.right + player.moving_speed > WIN_WIDTH and DISTANCE < 20000:
            background_floor.move()
            background_ceil.move()
            direction = bool(keys[pygame.K_RIGHT] or not keys[pygame.K_LEFT])
            motion = bool(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])
            for enemy in enemies:
                enemy.move(direction, motion)

        background_floor.update()
        background_ceil.update()

        for enemy in enemies:
            enemy.update()

        player.update()

        if activity_distance:
            if activity_distance[0] - DISTANCE < 200:
                activity_distance.pop(0)
                x, y = 1200, 500
                if len(activity_distance) == 0:
                    enemies.add(Boss(x, 381))
                    pygame.mixer.music.load(os.path.join(music_folder, 'boss_theme.mp3'))
                    pygame.mixer.music.play(-1)
                else:
                    enemies.add(Enemy(x, y))

        dir = 0 if player.go_to_right else 50
        absolute_pos = DISTANCE - 2 * (WIN_WIDTH - player.rect.centerx - dir)

        if 6200 > absolute_pos > 6000:
            main_surface.blit(wanted, (780, 10))

        if 100 > absolute_pos > -160:
            main_surface.blit(trash, (780, 10))

        hit_list = pygame.sprite.spritecollide(player, enemies, False)
        if hit_list and player.attack:
            for hitted in hit_list:
                if hitted.get_hitbox().overlap_area(player.get_attack_mask(),
                                            (player.rect.left-hitted.rect.left, player.rect.top-hitted.rect.top)):
                    hitted.hit(player.go_to_right)

        CURRENT_TIME = pygame.time.get_ticks()

        hit_list = pygame.sprite.spritecollide(player, enemies, False)
        if hit_list:
            for hitter in hit_list:
                if hitter.attack and hitter.get_attack_mask().overlap_area(player.get_hitbox(),
                                            (player.rect.left-hitter.rect.left, player.rect.top-hitter.rect.top)):
                    player.hit(hitter.go_to_right)

        main_surface.blit(hp_bar_img, (10, 10))
        if player.hp > 0:
            pygame.draw.rect(main_surface, (240, 10, 10), (13, 13, int(player.hp/100 * 244), 10))

    if final_window:
        final_window.update()

    pygame.display.update()

    fps_clock.tick(FPS)
