import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from random import randint


pygame.init()

FPS = pygame.time.Clock()
screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)

font = pygame.font.SysFont('Verdana', 20)
BLACK = 0, 0, 0

background = pygame.transform.scale(pygame.image.load('media/background.png').convert(), screen)
background_X = 0
background_X2 = background.get_width()
background_speed = 3

player = pygame.image.load('media/player.png').convert_alpha()
player_rect = player.get_rect()
player_speed = 5


def create_character(enemy=False):
    if enemy:
        character = pygame.image.load('media/enemy.png').convert_alpha()
        character_rect = pygame.Rect(width, randint(0, height-70), *character.get_size())
    else:
        character = pygame.image.load('media/bonus.png').convert_alpha()
        character_rect = pygame.Rect(randint(0, width-150), -280, *character.get_size())
    character_speed = randint(2, 5)
    return [character, character_rect, character_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_ENEMY, 3000)
pygame.time.set_timer(CREATE_BONUS, 2000)

enemies = []
bonuses = []
score = 0
is_working = True
while is_working:
    FPS.tick(60)
    pressed_keys = pygame.key.get_pressed()

    background_X -= background_speed
    background_X2 -= background_speed
    if background_X < -background.get_width():
        background_X = background.get_width()
    if background_X2 < -background.get_width():
        background_X2 = background.get_width()
    
    main_surface.blit(background, (background_X, 0))
    main_surface.blit(background, (background_X2, 0))
    main_surface.blit(player, player_rect)
    main_surface.blit(font.render(f"Score: {score}", True, BLACK), (width-110, 0))

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
        if enemy[1].left < -200:
            enemies.pop(enemies.index(enemy))
        if player_rect.colliderect(enemy[1]):
            print("\n!!!Game Over!!!\n")
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom >= height + 270:
            bonuses.pop(bonuses.index(bonus))
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    if pressed_keys[K_DOWN] and player_rect.bottom < height:
        player_rect = player_rect.move(0, player_speed)
    if pressed_keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(0, -player_speed)
    if pressed_keys[K_RIGHT] and player_rect.right < width:
        player_rect = player_rect.move(player_speed, 0)
    if pressed_keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(-player_speed, 0)

    pygame.display.flip()
