import os
import sys
import pygame
import background

# полезные константы
FPS = 60
WIN_HEIGHT = 800
WIN_WIDTH = 1200
FLOOR_HEIGHT = 200

# рабочие директории
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assets')

# изображения, ассеты и спрайты
floor_image = pygame.image.load(os.path.join(img_folder, 'floor_back.bmp'))

# инициализация модулей pygame
pygame.init()

# создаем объект главной поверхности
main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
main_surface.fill('gray')

background_floor = background.Background(main_surface, floor_image, 5, 0,
                                         WIN_HEIGHT - FLOOR_HEIGHT)

# создаем объект часов задержки
fps_clock = pygame.time.Clock()

while True:

    # фильтр событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    background_floor.update(keys[pygame.K_LEFT], keys[pygame.K_RIGHT])

    # задержка
    fps_clock.tick(FPS)

    # обновление экрана
    pygame.display.update()
