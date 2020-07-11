import pygame
from pygame import *
import random

FPS = 30 

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jumper")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()

#game loop
running = True

while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    all_sprites.update()
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()