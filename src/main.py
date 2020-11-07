import os
import sys
import pygame
import player
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
player_image = pygame.image.load(os.path.join(img_folder, 'player_1.png')).convert_alpha()
police_enemy_image = pygame.image.load(os.path.join(enemy_folder, 'police_cut.png')).convert_alpha()

# создаём пол и задники
background_floor = background.Background(main_surface, floor_images, 5, 0, WIN_HEIGHT - FLOOR_HEIGHT)
background_ceil = background.Background(main_surface, ceil_images, 5, 0, 0)

# создаем играбельного персонажа
player = player.Player(player_image, 5)

# создаём тестового противника
enemy = enemy.Enemy(police_enemy_image, 1, 400, 500)

# создаем объект часов задержки
fps_clock = pygame.time.Clock()

while True:

    # фильтр событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    background_floor.update()
    background_ceil.update()
    main_surface.blit(player.image, player.rect)
    main_surface.blit(enemy.image, enemy.rect)
    player.update()
    enemy.update(player.rect.centerx, player.rect.centery)

    # обновление экрана
    pygame.display.update()

    # задержка
    fps_clock.tick(FPS)
