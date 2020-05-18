"""
Snake Game

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import time
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/audio/snake_bg.mp3")
pygame.mixer.music.set_volume(0.2)

bg_size = width, height = 700, 480
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Snake")

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
RED = pygame.Color(255, 0, 0)
ORANGE = pygame.Color(255, 165, 0)
YELLOW = pygame.Color(255, 255, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
INDIGO = pygame.Color(75, 0, 130)
VIOLET = pygame.Color(128, 0, 128)

RAINBOW = [RED,ORANGE,YELLOW,GREEN,BLUE,INDIGO,VIOLET]



clock = pygame.time.Clock()

snake_pos = [100, 50]
snake_body = [[100,50],[90, 50], [80,50]]

food_pos = [random.randrange(1, (width//10))*10, \
            random.randrange(1, (height//10))*10]

food = True
speed = 10


direction = 'RIGHT'
d_update = direction

score = 0

pygame.mixer.music.play(-1)

def gameover():
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    
    #show score
    font = pygame.font.SysFont('Courier New', 50)
    screen.fill(BLACK)
    
    gameover_text1 = font.render("Your Score", True, WHITE)
    gameover_text1_rect = gameover_text1.get_rect()
    gameover_text1_rect.left, gameover_text1_rect.top = \
            (width - gameover_text1_rect.width) // 2, height - 240
    screen.blit(gameover_text1, gameover_text1_rect)

    gameover_text2 = font.render(str(score), True, WHITE)
    gameover_text2_rect = gameover_text2.get_rect()
    gameover_text2_rect.left, gameover_text2_rect.top = \
                        (width - gameover_text2_rect.width) // 2, \
                        gameover_text1_rect.bottom + 10
    screen.blit(gameover_text2, gameover_text2_rect)

    """
    quit_text = font.render("Quit Game", True, WHITE)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.left, quit_text_rect.top = \
            (width - quit_text_rect.width) // 2, height - 100
    screen.blit(quit_text, quit_text_rect)"""

    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    exit()
    
    
    """
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if quit_text_rect.left < pos[0] < quit_text_rect.right and \
           quit_text_rect.top < pos[1] < quit_text_rect.bottom:
            pygame.quit()
            quit()"""

#main game loop
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            try:
                pygame.quit()
                exit()
            except:
                sys.exit()
        
            
    # key is pressed down
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                d_update = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                d_update = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                d_update = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                d_update = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))


    #color
    screen.fill((0, 0, 0, 0.2))
    screen.set_alpha(100)
    
    #debug
    if d_update == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if d_update == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if d_update == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if d_update == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #move snake
    if direction == 'UP':
        snake_pos[1] -= speed
    if direction == 'DOWN':
        snake_pos[1] += speed
    if direction == 'LEFT':
        snake_pos[0] -= speed
    if direction == 'RIGHT':
        snake_pos[0] += speed

    #snake grow
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food = False
    else:
        snake_body.pop()

    #spawning food
    if not food:
        food_pos = [random.randrange(1, (width//10)) * 10, \
                    random.randrange(1, (height//10)) * 10]
    food = True
    
    #create snake
    for pos in snake_body:
        pygame.draw.rect(screen, WHITE, pygame.Rect(pos[0], pos[1], 10, 10))

    #create food
    food_color = random.choice(RAINBOW)
    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    #wall 
    if snake_pos[0] < 0:
        snake_pos[0] = width-10
    if snake_pos[0] > width-10:
        snake_pos[0] = 0
    if snake_pos[1] < 0:
        snake_pos[1] = height - 10
    if snake_pos[1] > height-10:
        snake_pos[1] = 0
        
    #collision
    for rect in snake_body[1:]:
        if snake_pos == rect:
            gameover()
            break;
            
            

    
    #show score 
    score_font = pygame.font.SysFont('Courier New', 25)
    score_text = score_font.render("Score: " + str(score), True, WHITE)
    score_text_rect = score_text.get_rect()
    score_text_rect.left, score_text_rect.top = 10, 10
    screen.blit(score_text, score_text_rect)
    
    
    #refresh
    pygame.display.flip()
    clock.tick(20)


if __name__ == "__main__":
    try:
        SnakeS()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

        
    
    
    


