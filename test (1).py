import pygame
import random


def respawn_target():
    target_rect.x = random.randrange(0,W - target_rect.w)
    target_rect.y = random.randrange(0, H - target_rect.h)

pygame.init()
pygame.font.init()

W = 550
H = 800
SCREEN_SIZE = (W, H)
SCREEN_CENTER = (W//2, H//2)
SCREEN_TOP = (W//2, 0)

screen = pygame.display.set_mode(SCREEN_SIZE)

FPS = 60
clock = pygame.time.Clock()

ARIAL_FONT_PATH = pygame.font.match_font('arial')
ARIAL_64 = pygame.font.Font(ARIAL_FONT_PATH, 64)
ARIAL_36 = pygame.font.Font(ARIAL_FONT_PATH,36)

INIT_DELAY = 2000
finish_delay = INIT_DELAY
DECREASE_BASE = 1.002
last_respawn_time = 0

game_over = False
RETRY_SURFACE = ARIAL_36.render('PRESS ANY KEY', True, (0, 0, 0))
RETRY_RECT = RETRY_SURFACE.get_rect()
RETRY_RECT.midtop = SCREEN_CENTER

score = 0

TARGET_IMAGE = pygame.image.load("komar.png")
TARGET_IMAGE = pygame.transform.scale(TARGET_IMAGE, (110, 120))
target_rect = TARGET_IMAGE.get_rect()

respawn_target()

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if game_over:
                score = 0
                finish_delay = INIT_DELAY
                game_over = False
                last_respawn_time = pygame.time.get_ticks()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == pygame.BUTTON_LEFT:
                if not game_over and target_rect.collidepoint(e.pos):
                    score += 1
                    respawn_target()
                    last_respawn_time = pygame.time.get_ticks()
                    finish_delay = INIT_DELAY / (DECREASE_BASE ** score)

    clock.tick(FPS)

    screen.fill((255, 208, 202))
    score_surface = ARIAL_64.render(str(score), True, (0, 0, 0))
    score_rect = score_surface.get_rect()

    now = pygame.time.get_ticks()
    elapsed = now - last_respawn_time
    if elapsed > finish_delay:
        game_over = True

        score_rect.midbottom = SCREEN_CENTER

        screen.blit(RETRY_SURFACE, RETRY_RECT)
    else:
        h = H - H * elapsed / finish_delay
        time_rect = pygame.Rect((0, 0), (W, h))
        time_rect.bottomleft = (0,H)
        pygame.draw.rect(screen, (232, 255, 208), time_rect)

        screen.blit(TARGET_IMAGE, target_rect)

        score_rect.midtop = SCREEN_TOP
    screen.blit(score_surface, score_rect)

    pygame.display.flip()
pygame.quit()