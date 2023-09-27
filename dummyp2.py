import pygame
import string
import os
import random

pygame.init()
pygame.mixer.init()

# Creating global variables
Fly = False
Exit_game = False
ground_scroll = 0
ground_speed = 3
game_over = False
screen_width = 585
screen_height = 600
pipe_gap = 150
pipe_frequency = 1500
score = 0
passed = False
time_last = pygame.time.get_ticks()
print(time_last)

# Creating a screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Setting a caption
pygame.display.set_caption('Flappy bird game')

#loading all required music
wing_music = pygame.mixer.Sound('audio/wing.wav')
die_music = pygame.mixer.Sound('audio/die.wav')
points_music = pygame.mixer.Sound('audio/point.wav')
hit_music = pygame.mixer.Sound('audio/hit.wav')

# Drawing a background
background = pygame.image.load('background.jpg')
ground = pygame.image.load('ground.png')

# Creating a clock
clock = pygame.time.Clock()
fps = 50
image = pygame.image.load('flappybird.png')
gameover_image = pygame.image.load('gameover.jpg')
font = pygame.font.SysFont(None, 40)
font1 = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None,40)
pipes_image = pygame.image.load('pipes.png')

class bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (60, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.rect.inflate_ip(-20,-40)
        self.velocity = 0
        global flying, count,game_over
        self.game_over = False
        self.flying = False
        self.count = 0

    def update(self, game_over):
        keys = pygame.key.get_pressed()  # Get a list of keys currently pressed
        if not any(keys) and not self.flying and not game_over:
            self.rect.x += 2
            self.rect.y = 200
        if keys[pygame.K_UP] and not game_over:  # Check if the UP arrow key is pressed
            global Fly
            self.flying = True
            self.count = 1
            Fly = True
            wing_music.play()

            if self.rect.bottom < 520:
                self.velocity -= 0.5
                self.rect.y += self.velocity
        elif not game_over:
            if self.count == 1:
                self.flying = True
            else:
                self.flying = False
            if self.velocity <= 8:
                self.velocity += 0.5
            if self.rect.bottom < 520:
                self.rect.y += self.velocity

bird_group = pygame.sprite.Group()
flappy = bird(50, int(screen_height / 2))
bird_group.add(flappy)

class pipes(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pipes_image, (60,600))
        self.rect = self.image.get_rect()
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 3)]
            self.rect.inflate_ip(-5, -40)
        if pos == -1:
            self.rect = self.image.get_rect()
            self.rect.topleft = [x, y + int(pipe_gap / 3)]
            self.rect.inflate_ip(-5, -40)

    def update(self, game_over):
        if Fly:  # Only update pipe position when flying
            self.rect.x -= ground_speed
            if self.rect.x < -50:
                self.kill()

pipe_group = pygame.sprite.Group()

def check():
    global game_over, flappy, Fly,score
    global pipe_up, pipe_down
    if event.type == pygame.KEYDOWN:
        game_over = False
        bird_group.remove(flappy)
        flappy.rect.bottom = screen_height / 3 - 10
        flappy = bird(50, int(screen_height / 3))
        bird_group.add(flappy)
        pipe_group.empty()
        Fly = True
        score = 0
while not Exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit_game = True
    screen.blit(background, (0, 0))
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and passed == False:
            passed = True
        if passed == True:
            if bird_group.sprites()[0].rect.left >= pipe_group.sprites()[0].rect.right:
                print("Hi")
                score +=1
                points_music.play()
                passed = False

    bird_group.draw(screen)
    bird_group.update(game_over)
    if flappy.rect.bottom >= 512 :
        game_over = True
        Fly = False
        if game_over == True:
            Score_text =  font.render('Score:' + str(score),True,(0,0,0))
            game_over_text = font.render('Game over', True, (255, 0, 0))
            continue_text = font1.render('Press Enter to continue', True, (255, 0, 0))
            screen.blit(Score_text,(screen_width // 2 - 160, screen_height // 2 -75))
            screen.blit(game_over_text, (screen_width // 2 - 160, screen_height // 2 - 50))
            screen.blit(continue_text, (screen_width // 2 - 200, screen_height // 2 - 25))
        check()
    if game_over == False:
        current = pygame.time.get_ticks()
        if current - time_last > pipe_frequency and Fly == True:
            pipe_height = random.randint(-70, 100)
            pipe_down = pipes(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_up = pipes(screen_width, int(screen_height / 2) + pipe_height, -1)
            pipe_group.add(pipe_down)
            pipe_group.add(pipe_up)
            time_last = current
        pipe_group.draw(screen)
        pipe_group.update(game_over)
    if game_over == False:
        screen.blit(ground, (ground_scroll, 504))
        ground_scroll -= ground_speed
        if abs(ground_scroll) >= 17 and not game_over:
            ground_scroll = 0
    if (pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < -10) and not game_over:
        game_over = True
        hit_music.play()
        flappy.rect.bottom = 512

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
