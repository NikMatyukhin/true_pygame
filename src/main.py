import os
import sys
import pygame
import player
import background

# полезные константы
FPS = 30
WIN_HEIGHT = 800
WIN_WIDTH = 1200
FLOOR_HEIGHT = 200

# рабочие директории
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assets')

# инициализация модулей pygame
pygame.init()

# создаем объект главной поверхности
main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# изображения, ассеты и спрайты
floor_image = pygame.image.load(os.path.join(img_folder,
                                             'floor_back.bmp'))
ceil_image = pygame.image.load(os.path.join(img_folder,
                                            'ceil_back.bmp'))
player_image = pygame.image.load(os.path.join(img_folder,
                                              'player.bmp')).convert()
player_image.set_colorkey((255, 255, 255))

# создаём пол
background_floor = background.Background(main_surface, floor_image, 5, 0,
                                         WIN_HEIGHT - FLOOR_HEIGHT)
background_ceil = background.Background(main_surface, ceil_image, 5, 0,
                                        0)

# создаем играбельного персонажа
player = player.Player(player_image, 10, WIN_WIDTH)

# создаем объект часов задержки
fps_clock = pygame.time.Clock()

while True:

    main_surface.fill('gray')

    # фильтр событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    background_floor.update()
    background_ceil.update()
    main_surface.blit(player.image, player.rect)
    player.update()

    # задержка
    fps_clock.tick(FPS)

    # обновление экрана
    pygame.display.update()
