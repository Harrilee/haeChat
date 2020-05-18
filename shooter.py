import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import traceback
from pygame.locals import *
from random import *

#def Shooter():

pygame.init()
pygame.mixer.init()

#load background
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Virus Shooter")
background = pygame.image.load("assets/images/background.png").convert()

#set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#load all sounds
pygame.mixer.music.load("assets/audio/shooter_bg.mp3")
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound("assets/audio/bullet.wav")
bullet_sound.set_volume(0.1)

bomb_sound = pygame.mixer.Sound("assets/audio/use_bomb.wav")
bomb_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound("assets/audio/level_up.wav")
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound("assets/audio/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)

enemy1_down_sound = pygame.mixer.Sound("assets/audio/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)

enemy2_down_sound = pygame.mixer.Sound("assets/audio/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)

enemy3_down_sound = pygame.mixer.Sound("assets/audio/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)

me_down_sound = pygame.mixer.Sound("assets/audio/me_down.wav")
me_down_sound.set_volume(1.0)

#==========================
# My sprite class
#==========================

class MySanitizer(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        #load images
        self.image1 = pygame.image.load("assets/images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("assets/images/me2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("assets/images/me_destroy_1.png").convert_alpha(), \
            pygame.image.load("assets/images/me_destroy_2.png").convert_alpha(), \
            pygame.image.load("assets/images/me_destroy_3.png").convert_alpha(), \
            pygame.image.load("assets/images/me_destroy_4.png").convert_alpha()])
        self.rect = self.image1.get_rect()
        self.width,self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60
        
        self.speed = 10
        self.active = True
        self.invincible = False
        #closer contact between sprites
        self.mask = pygame.mask.from_surface(self.image1)

    #define movements
        
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    #three lives, used to reset each time
    def reset(self):
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60
        self.active = True
        self.invincible = True
        

#==========================
# Small Enemy Sprite class
#==========================
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        #load images
        self.image = pygame.image.load("assets/images/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("assets/images/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy1_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0, self.width-self.rect.width), \
                        randint(-5*self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)

    #movement
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    #reset
    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0, self.width-self.rect.width), \
                        randint(-5*self.height, 0)
#==========================
# Mid Enemy Sprite class
#==========================
class MidEnemy(pygame.sprite.Sprite):
    energy = 8
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        #load images
        self.image = pygame.image.load("assets/images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("assets/images/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("assets/images/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy2_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0, self.width-self.rect.width), \
                        randint(-10*self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.hit = False
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = \
                        randint(0, self.width-self.rect.width), \
                        randint(-10*self.height, -self.height)

#==========================
# Big Enemy Sprite class
#==========================
class BigEnemy(pygame.sprite.Sprite):

    energy = 20
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("assets/images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("assets/images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("assets/images/enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("assets/images/enemy3_down1.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy3_down2.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy3_down3.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy3_down4.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy3_down5.png").convert_alpha(), \
            pygame.image.load("assets/images/enemy3_down6.png").convert_alpha()])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
                        randint(0, self.width-self.rect.width), \
                        randint(-15*self.height, -5* self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigEnemy.energy
        self.hit = False
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left, self.rect.top = \
                        randint(0, self.width-self.rect.width), \
                        randint(-15*self.height, -5* self.height)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

#for use to increase difficulty
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

#not working yet
def menu():

    screen.blit(background,(0,0))
    
    #game start screen
    title_font = pygame.font.Font("assets/font/font.TTF", 48)
    gamestart_font = pygame.font.Font("assets/font/font.TTF", 20)
    gamestart_image = pygame.image.load("assets/images/gamestart.png").convert_alpha()
    gamestart_rect = gamestart_image.get_rect()
    

    #paint start page
    title = title_font.render("Virus Shooter", True, WHITE)
    title_rect = title.get_rect()
    title_rect.left, title_rect.top = \
                              (width - title_rect.width) // 2, height - 500
    screen.blit(title, title_rect)

    #gamestart_rect.left, gamestart_rect.top = \
    #                    (width - gamestart_rect.width) // 2, \
    #                    title_rect.bottom + 200
    #screen.blit(gamestart_image, gamestart_rect)
    #pygame.display.update()

    while True:
        e = pygame.event.poll()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                break
            elif e.key == pygame.K_q:
                pygame.quit()
                quit()
        else:
            gamestart_ent = gamestart_font.render("Press [enter] to start!", True, WHITE)
            gamestart_quit = gamestart_font.render("or [q] to quit!", True, WHITE)
            gamestart_ent_rect = gamestart_ent.get_rect()
            gamestart_ent_rect = gamestart_ent.get_rect()
            gamestart_ent_rect.left, gamestart_ent_rect.top = \
                        (width - gamestart_ent_rect.width) // 2, \
                        title_rect.bottom + 200
            gamestart_quit_rect = gamestart_quit.get_rect()
            gamestart_quit_rect = gamestart_quit.get_rect()
            gamestart_quit_rect.left, gamestart_quit_rect.top = \
                        (width - gamestart_quit_rect.width) // 2, \
                        title_rect.bottom + 250


    screen.blit(background,(0,0))


            
    """
    pressed = False
    while not pressed:
    
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if gamestart_rect.left < pos[0] < gamestart_rect.right and \
               gamestart_rect.top < pos[1] < gamestart_rect.bottom:
                pressed = True"""

                


#==========================================================================
#               main function                                              
#==========================================================================
        
def main():

    #run bg music forever
    pygame.mixer.music.play(-1)
    
    running = True       

    #create my sanitizer

    me = MySanitizer(bg_size)

    #create enemy group
    enemies = pygame.sprite.Group()

    #create enemies
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #create normal bullets
    bullet = []
    bullet_index = 0
    BULLET_NUM = 4
    for i in range(BULLET_NUM):
        bullet.append(Bullet(me.rect.midtop))

        
    #fps controller    
    clock = pygame.time.Clock()

    #when destroyed
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #show score
    score = 0
    score_font = pygame.font.Font("assets/font/font.ttf", 36)

    #set difficulty level
    level = 1

    #full screen bomb (mask)
    bomb_image = pygame.image.load("assets/images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("assets/font/font.ttf", 48)
    bomb_num = 3
    

    #life remaining
    life_image = pygame.image.load("assets/images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3


    #stop recording score over and over again
    recorded = False


    #game over screen
    gameover_font = pygame.font.Font("assets/font/font.TTF", 48)
    gameover_image = pygame.image.load("assets/images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()



    #invincibility period
    INVINCIBLE_TIME = USEREVENT
    
    #switch images
    switch_image = True

    #delay
    delay = 100

#=================================================
#        main loop                                
#=================================================


    while running:
        #if menu_display:
        #    menu()
        #    #screen.blit(background,(0,0))
        #    pygame.time.wait(2000)
        #    menu_display = False

        #event keys 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
                #sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)
                                
        #increase level depending on score
        if level == 1 and score > 10000:
            level = 2
            upgrade_sound.play()
            #increase 3 small enemy, 2 mid enemy, and 1 big enemy
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            #increase speeds
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 50000:
            level = 3
            upgrade_sound.play()
            #increase 3 small enemy, 2 mid enemy, and 1 big enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #increase speeds
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 100000:
            level = 4
            upgrade_sound.play()
            #increase 3 small enemy, 2 mid enemy, and 1 big enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #increase speeds
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 500000:
            level = 5
            upgrade_sound.play()
            #increase 3 small enemy, 2 mid enemy, and 1 big enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #increase speeds
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            
            

        screen.blit(background, (0, 0))

        if life_num: 
            #check key pressed
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            #shoot bullets
            if not(delay % 10):
                bullet[bullet_index].reset(me.rect.midtop)
                bullet_index = (bullet_index + 1) % BULLET_NUM
                bullet_sound.play()

            #check if bullet collided
            for b in bullet:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
                
            #paint big enemies
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #paint blood level
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top-5), \
                                     (each.rect.right, each.rect.top -5), 2)
                    #if blood >20%, green, else red
                    energy_remain = each.energy / BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top-5), \
                                     (each.rect.left + each.rect.width*energy_remain, \
                                      each.rect.top-5), 2)
                                     
                    
                    #play sound
                    if each.rect.bottom == - 50:
                        enemy3_fly_sound.play()
                else:
                    #destroy
                    #if not(delay % 3):
                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()
                    screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) % 6
                    if e3_destroy_index == 0:
                        enemy3_fly_sound.stop()
                        score += 10000
                        each.reset()
                
                
            #paint mid enemies
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    #paint blood level
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top-5), \
                                     (each.rect.right, each.rect.top -5), 2)
                    #if blood >20%, green, else red
                    energy_remain = each.energy / MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top-5), \
                                     (each.rect.left + each.rect.width*energy_remain, \
                                      each.rect.top-5), 2)
                else:
                    #destroy
                    #if not(delay % 3):
                    if e2_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e2_destroy_index == 0:
                        score += 6000
                        each.reset()

            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    #destroy
                    #if not(delay % 3):
                    if e1_destroy_index == 0:
                        enemy1_down_sound.play()
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        score += 1000
                        each.reset()

            #check if my sanitizer has collided
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            
            #paint my sanitizer
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                #destroy
                if not(delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        #print("Game Over!")
                        #running = False
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3*1000)

            #paint bombs
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height-15-bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height -5-text_rect.height))

            #paint remaining lives
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_rect.width, \
                                 height-10-life_rect.height))                    
        #paint end screen
        elif life_num == 0:
            #stop music
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            #record score

            if not recorded:
                recorded = True
                
                with open("shooter_record.txt" ,"w") as f:
                    f.write(str(score))
                                


            gameover_text1 = gameover_font.render("Your Score", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                      (width - gameover_text1_rect.width) // 2, height - 300
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                      (width - gameover_text2_rect.width) // 2, \
                                      gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - gameover_rect.width) // 2, \
                                gameover_text2_rect.bottom + 50
            screen.blit(gameover_image, gameover_rect)
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if gameover_rect.left < pos[0] < gameover_rect.right and \
                   gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    exit()
                    #sys.exit()

            
            
            
            
        #paint score
        score_text = score_font.render("Score : %s" % str(score), True, WHITE)
        screen.blit(score_text, (10, 5))
                        
        #switch between images
        if not(delay % 5):
            switch_image = not switch_image
            
        delay -= 1
        
        if not delay:
            delay = 100
            
        pygame.display.flip()
        clock.tick(60)

    
    #main()
            

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
