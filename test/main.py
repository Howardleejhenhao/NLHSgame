import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('game')
clock = pygame.time.Clock()

background_surf = pygame.image.load('background.png')
button_surf = pygame.image.load('bottom.png')
player_surf = pygame.image.load('player.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()



    screen.blit(background_surf, (0, 0))
    screen.blit(button_surf, (200, 200))
    screen.blit(player_surf, (100, 0))

    pygame.display.update()

    clock.tick(60)