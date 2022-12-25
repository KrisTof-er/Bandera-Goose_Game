import pygame
from pygame.constants import QUIT
from random import randint


pygame.init()

screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255

main_surface = pygame.display.set_mode(screen)
ball = pygame.Surface((20, 20))
ball.fill(WHITE)
bal_rect = ball.get_rect()
ball_speed = [1, 1]

is_working = True

while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

    bal_rect = bal_rect.move(ball_speed)

    if bal_rect.bottom >= height or bal_rect.top <= 0:
        ball.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        ball_speed[1] = -ball_speed[1]

    if bal_rect.left >= width or bal_rect.right <= 0:
        ball.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        ball_speed[0] = -ball_speed[0]

    main_surface.fill(BLACK)
    main_surface.blit(ball, bal_rect)
    pygame.display.flip()
