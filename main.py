import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from random import randint


pygame.init()

FPS = pygame.time.Clock()
screen = width, height = 800, 600
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

font = pygame.font.SysFont('Verdana', 20)
main_surface = pygame.display.set_mode(screen)
ball = pygame.Surface((20, 20))
ball.fill(BLUE)
ball_rect = ball.get_rect()
ball_speed = 5


def create_character(enemy=False):
    character = pygame.Surface((20, 20))
    if enemy:
        character.fill(RED)
        character_rect = pygame.Rect(
            width-10, randint(0, height-20), *character.get_size())
    else:
        character.fill(GREEN)
        character_rect = pygame.Rect(
            randint(0, width-20), 0, *character.get_size())
    character_speed = randint(2, 5)
    return [character, character_rect, character_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 2000)

enemies = []
bonuses = []
score = 0
is_working = True
while is_working:
    FPS.tick(60)
    pressed_keys = pygame.key.get_pressed()
    main_surface.fill(BLACK)
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(f"Score: {score}", True, WHITE), (width-110, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_character(enemy=True))
        if event.type == CREATE_BONUS:
            bonuses.append(create_character(enemy=False))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            # enemies.pop(enemies.index(enemy))
            print("\n!!!Game Over!!!\n")
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    if pressed_keys[K_DOWN] and ball_rect.bottom < height:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and ball_rect.top > 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_keys[K_RIGHT] and ball_rect.right < width:
        ball_rect = ball_rect.move(ball_speed, 0)
    if pressed_keys[K_LEFT] and ball_rect.left > 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    # print(f"{len(enemies)}___{len(bonuses)}")
    pygame.display.flip()
