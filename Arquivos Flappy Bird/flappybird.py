import pygame
import sys
import random
# functions


def draw_floor():
    tela.blit(chao_surface, (chao_posx, 450))
    tela.blit(chao_surface, (chao_posx + 288, 450))


def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midtop=(300, random_pipe_position))
    bottom_pipe = pipe_surface.get_rect(midtop=(300, random_pipe_position - 500))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            tela.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            tela.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 450:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_mov * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 35))
        tela.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Pontuacao: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 35))
        tela.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Pont. Max.: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 400))
        tela.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
tela = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)
# Game Variables
gravity = 0.25
bird_mov = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('sprites/background-night.png')

chao_surface = pygame.image.load('sprites/base.png')
chao_posx = 0

bird_downflap = pygame.image.load('sprites/redbird-downflap.png')
bird_midflap = pygame.image.load('sprites/redbird-midflap.png')
bird_upflap = pygame.image.load('sprites/redbird-upflap.png')
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('sprites/pipe-red.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 250, 300, 350, 400]

game_over_surface = pygame.image.load('sprites/gameover.png')
game_over_rect = game_over_surface.get_rect(center=(144, 220))

flap_sound = pygame.mixer.Sound('audio/wing.wav')
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_mov = 0
                bird_mov -= 7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    tela.blit(bg_surface, (0, 0))

    if game_active:
        # Bird Movement
        bird_mov += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_mov
        tela.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Canos Movement
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 1:
            score_sound.play()
            score_sound_countdown = 100
    else:
        tela.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
# floor movement
    chao_posx -= 1
    draw_floor()
    if chao_posx <= -288:
        chao_posx = 0
    pygame.display.update()
    clock.tick(80)
