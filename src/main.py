import sys
import pygame

# полезные константы
FPS = 60
WIN_HEIGHT = 400
WIN_WIDTH = 800

# инициализация модулей pygame
pygame.init()

# создаем объект главной поверхности и часов задержки
main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
main_surface.fill('white')
fps_clock = pygame.time.Clock()

# если нужно до цикла отобразить объекты
#pygame.display.update()

while True:

    # фильтр событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # задержка
    fps_clock.tick(FPS)

    #main_surface.fill('white')

    # обновление экрана
    pygame.display.update()