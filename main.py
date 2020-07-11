
# Jumpy platform game
import pygame 
from pygame import *
from sprites import *
from settings import *
import random


class Game:
    def __init__(self):
        # initialize game window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jumper")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)


    def new(self):
        # new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST: 
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()
            
    def run(self):
        # game loop
        self.playing = True
        while self.playing :
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()

    def update(self):
        #game loop - update
        self.all_sprites.update()
        # check if player hits the platform
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # if player reaches the top 1/4 of the screen 
        if self.player.rect.top <= 600 / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= 600:
                    plat.kill()
                    self.score += 10
        # DIE 
        if self.player.rect.bottom > 600:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 5)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False


        #spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            width = random.randrange(100, 200)
            p = Platform(self, random.randrange(0, 800 - width),
                        random.randrange(-40, 10))

            self.platforms.add(p)
            self.all_sprites.add(p)
 

    def event(self):
        #for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_UP:
                    self.player.jump()


    def draw(self):
        # game loop - draw
        self.screen.blit(background, background_rect)
        #self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, (255, 255, 255), 400, 15)
        pygame.display.flip()

    def show_start_screen(self):
        #game sart screen 
        self.screen.fill((0, 255, 125))
        self.draw_text("Jumpy", 48, (255, 255, 255), 400, 600 / 4)
        self.draw_text("Arrows to move, Space to Jump", 22, (255, 255, 255), 400, 600 / 2)
        self.draw_text("Press key to play", 22, (255, 255, 255), 400, 600 * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()


    def show_go_screen(self):
        #game over or continue 
        if not self.running:
            return
        self.screen.fill((0, 255, 125))
        self.draw_text("GAME OVER", 48, (255, 255, 255), 400, 600 / 4)
        self.draw_text("Score : " + str(self.score), 22, (255, 255, 255), 400, 600 / 2)
        self.draw_text("Press key to play again", 22, (255, 255, 255), 400, 600 * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()   
pygame.quit()

