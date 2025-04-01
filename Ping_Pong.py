from all_colors import *
import sys
import pygame
pygame.init()

#2 При отскоке увеличиваеться скорость мяча, 3 Ограничить скорость

ball_sound = pygame.mixer.Sound('resours/Отбитие Мяча.mp3')
score_sound = pygame.mixer.Sound('resours/Счёт.mp3')
win_sound = pygame.mixer.Sound('resours/Победа.mp3')

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("My Game")

paddle_width = 25
paddle_height = 100
paddle_speed = 10

ball_size = 10
ball_speed_x = 5
ball_speed_y = 5

paddle1_rect = pygame.Rect(0, screen_height//2 - paddle_height//2, paddle_width, paddle_height)
paddle2_rect = pygame.Rect(screen_width - paddle_width, screen_height//2 - paddle_height//2, paddle_width, paddle_height)

ball_rect = pygame.Rect(screen_width//2 - ball_size//2, screen_height//2 - ball_size//2, ball_size, ball_size)

score1 = 0
score2 = 0
speed = 5

font = pygame.font.SysFont(None, 32)

Background = Black
screen.fill(Background)

ai_mode = True
if len(sys.argv) > 1:
    if sys.argv[1] == '--human':
        ai_mode = False

def update_ai():
    if ball_rect.x > screen_width//2:
        if ball_rect.centery < paddle2_rect.centery:
            paddle2_rect.y -= paddle_speed
        elif ball_rect.centery > paddle2_rect.centery:
            paddle2_rect.y += paddle_speed

        if paddle2_rect.top < 0:
            paddle2_rect.top = 0
        if paddle2_rect.bottom > screen_height:
            paddle2_rect.bottom = screen_height
    else:
        paddle2_rect.centery += (screen_height//2 - paddle2_rect.centery) / paddle_speed

FPS = 60
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle2_rect.top > 5:
        paddle2_rect.y -= paddle_speed
    elif keys[pygame.K_DOWN] and paddle2_rect.bottom < screen_height - 5:
        paddle2_rect.y += paddle_speed
    if keys[pygame.K_w] and paddle1_rect.top > 5:
        paddle1_rect.y -= paddle_speed
    elif keys[pygame.K_s] and paddle1_rect.bottom < screen_height - 5:
        paddle1_rect.y += paddle_speed
    if ai_mode:
        update_ai()

    ball_rect.y += ball_speed_y
    ball_rect.x += ball_speed_x

    if ball_rect.top < 0 or ball_rect.bottom > screen_height:
        ball_speed_y *= -1

    if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
        ball_speed_x = -ball_speed_x
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        if ball_speed_x >= 30:
            ball_speed_x = 30
        if speed < 30:
            speed += 1
        else:
            speed = 30
        ball_sound.play()

    if ball_rect.left <= 0:
        ball_rect = pygame.Rect(screen_width//2 - ball_size//2, screen_height//2 - ball_size//2, ball_size, ball_size)
        score2 += 1
        score_sound.play()

    if ball_rect.right > screen_width:
        ball_rect = pygame.Rect(screen_width//2 - ball_size//2, screen_height//2 - ball_size//2, ball_size, ball_size)
        score1 += 1
        score_sound.play()

    if score1 == 10 or score2 == 10:
        ball_rect = pygame.Rect(screen_width//2 - ball_size//2, screen_height//2 - ball_size//2, ball_size, ball_size)
        ball_speed_x = 0
        ball_speed_y = 0
        win_sound.play()

    screen.fill(Background)

    pygame.draw.rect(screen, White, paddle1_rect)
    pygame.draw.rect(screen, White, paddle2_rect)

    pygame.draw.ellipse(screen, White, ball_rect)

    pygame.draw.line(screen, White, (screen_width//2, 0), (screen_width//2, screen_height), 1)

    score_text = font.render(f'{score1} : {score2}', True, White)
    screen.blit(score_text, (screen_width//2 - score_text.get_width() // 2, 10))

    speed_text = font.render(f'Скорость: {speed}', True, White)
    screen.blit(speed_text, (1100, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()