import pygame
from pygame import *
from settings import *
from random import choice
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):

    def __init__ (self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load("person.png")
        #self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.pos = (800 / 2, 600 / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        #jump only if standing on platform 
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        #apply friction
        self.acc += self.vel * PLAYER_FRICTION
        #eqution of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #wrap around the sidesof the screen 
        if self.pos.x > 800:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 800

        self.rect.midbottom = self.pos

img_1 = pygame.image.load("ground_1.png")
img_2 = pygame.image.load("ground_2.png")

img_list = [img_1, img_2]

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        
        self.image = choice(img_list)
        #self.image = pygame.Surface((w, h))
        #self.image.fill((50, 225, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


background = pygame.image.load("cloudvwe.jpg")
background_rect = background.get_rect()