import pygame
from settings import *
from player import Player
from enemie import Enemie
from camera import Camera


def main():
    pygame.init()
    Enemie.class_init()

    main_camera = Camera(pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT)))

    start_game(main_camera)

def start_game(main_camera):
    fps_clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 22)
    player = Player()
    enemie = Enemie(100, 100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
        main_camera.surface.fill((0, 0, 0))
        get_input(player)
        player.update(main_camera)
        enemie.update(main_camera)
        main_camera.blit(font.render(f'FPS: {fps_clock.get_fps():3.2f}', 0, (200, 255, 200)), (0, 0))
        pygame.display.update()

        fps_clock.tick(FPS)


def get_input(player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(0, -50)
    elif keys[pygame.K_DOWN]:
        player.move(0, 50)
    elif keys[pygame.K_LEFT]:
        player.move(-50, 0)
    elif keys[pygame.K_RIGHT]:
        player.move(50, 0)


if __name__ == '__main__':
    main()