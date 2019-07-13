"""

DEADWATCH

Created 19th of April 2018
By Kiran Surendran

V.6.0.0
 
"""

# Modules
import pygame
import sys
import random as rnd
import math
import time

FPS = 60
WIDTH = 1200
HEIGHT = 800
from pygame.locals import *
pygame.init()                   # Initialize Pygame

fire_sound = pygame.mixer.Sound("img/gunshot.wav")
menu_music = pygame.mixer.music.load("img/TremLoadingloopl.wav")
death_sound = pygame.mixer.Sound("img/DeathScreenSound.wav")

# End of Modules
name_input = input("Input your name: ")
# Constant Colours

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
GREY = (127, 130, 135)
##timer = 0
# Fonts
FONTSIZE = 30
score_lives_font = pygame.font.SysFont("americantypewriter", FONTSIZE, False, False)
waves_font = pygame.font.SysFont("americantypewriter",25, False, False)
stats_font = pygame.font.SysFont("americantypewrite", 50, False, False)


#LOAD ALL IMAGES
sprite_idle = pygame.image.load("img/sprite_idle_u.png")
sprite_idle = pygame.transform.scale(sprite_idle, (61,36))
sprite_idle_l = pygame.image.load("img/sprite_idle_l.png")
sprite_idle_r = pygame.image.load("img/sprite_idle_r.png")
sprite_idle_u = pygame.image.load("img/sprite_idle_u.png")
sprite_idle_d = pygame.image.load("img/sprite_idle_d.png")
sprite_shootpistol_r = pygame.image.load("img/sprite_shootpistol_r.png")
sprite_shootpistol_l = pygame.image.load("img/sprite_shootpistol_l.png")
sprite_shootpistol_u = pygame.image.load("img/sprite_shootpistol_u.png")
sprite_shootpistol_d = pygame.image.load("img/sprite_shootpistol_d.png")
s_ammo_sprite = pygame.image.load("img/smg_ammo.png")
r_ammo_sprite = pygame.image.load("img/rifle_ammo.png")


#Item images
pistol_image = pygame.image.load("img/pistol_sprite.png")
smg_image = pygame.image.load("img/smg_sprite.png")
rifle_image = pygame.image.load("img/rifle_sprite.png")
combat_image = pygame.image.load("img/combatrifle_sprite.png")
medkit_image = pygame.image.load("img/medkit.png")

#Animation spritesheet for walking in list form
walk_right = [pygame.image.load("img/r1.png"), pygame.image.load("img/r2.png"), pygame.image.load("img/r3.png"),pygame.image.load("img/r4.png"),pygame.image.load("img/r5.png")]
walk_left = [pygame.image.load("img/l1.png"), pygame.image.load("img/l2.png"), pygame.image.load("img/l3.png"),pygame.image.load("img/l4.png"),pygame.image.load("img/l5.png")]
walk_up = [pygame.image.load("img/u1.png"), pygame.image.load("img/u2.png"), pygame.image.load("img/u3.png"),pygame.image.load("img/u4.png"),pygame.image.load("img/u5.png")]
walk_down = [pygame.image.load("img/d1.png"), pygame.image.load("img/d2.png"), pygame.image.load("img/d3.png"),pygame.image.load("img/d4.png"),pygame.image.load("img/d5.png")]


all_sprites = pygame.sprite.Group()     # All sprites group
mobs = pygame.sprite.Group()            #Mobs sprite group
bullets = pygame.sprite.Group()         #Bullet group
weapons_items = pygame.sprite.Group()   #Weapons group

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))    # Set Window Size
pygame.display.set_caption("DEADWATCH")      # Set Title Bar Caption
clock = pygame.time.Clock()



# Classes

class Player(pygame.sprite.Sprite):
    # Player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_idle.convert()   #Sprite image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speedx = 0      #Player Speedx
        self.speedy = 0      #Player Speedy
        self.direction = "none" #Player direction
        self.maxnum = 5
        self.curnum = 0
        self.timer = 0
        
    def update(self):
        # MOVEMENT AND CONTROLS
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -6
            self.direction = "left"
        if keystate[pygame.K_RIGHT]:
            self.speedx = 6
            self.direction = "right"
        if keystate[pygame.K_UP]:
            self.speedy = -6
            self.direction = "up"
        if keystate[pygame.K_DOWN]:
            self.speedy = 6
            self.direction = "down"
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #Animation for sprite and counting number of frames
        if self.curnum >= self.maxnum -1 :
            self.curnum = 0           
        else:
            self.curnum += 1
        if self.direction == "right" and self.timer % 7 == 1:
            self.image = walk_right[self.curnum].convert()
        if self.direction == "left" and self.timer % 7 == 1:
            self.image = walk_left[self.curnum].convert()
        if self.direction == "up" and self.timer % 7 == 1:
            self.image = walk_up[self.curnum].convert()
        if self.direction == "down" and self.timer % 7 == 1:
            self.image = walk_down[self.curnum].convert()
            
        #Check if sprite not moving
        if self.speedx == 0 and self.speedy == 0:
             if self.direction == "up":
                self.image = sprite_idle_u.convert()    #Change Image
             if self.direction == "down":
                self.image = sprite_idle_d.convert()    #Change Image
             if self.direction == "left":
                self.image = sprite_idle_l.convert()  #Change Image
             if self.direction == "right":
                self.image = sprite_idle_r.convert()    #Change Image
        self.image.set_colorkey(WHITE)
        
        
        # WALL BOUNDS
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        self.timer += 1

    def shoot(self, damage):
        # When player shoots gun

        #Animation change
        if self.direction == "up":
            self.image = sprite_shootpistol_u.convert()
            self.image.set_colorkey(WHITE)
        elif self.direction == "down":
            self.image = sprite_shootpistol_d.convert()
            self.image.set_colorkey(WHITE)
        elif self.direction == "right":
            self.image = sprite_shootpistol_r.convert()
            self.image.set_colorkey(WHITE)
        elif self.direction == "left":
            self.image = sprite_shootpistol_l.convert()
            self.image.set_colorkey(WHITE)

        #Bullet object creation 
        bullet = Bullet(self.rect.centerx, self.rect.top, self.direction, damage)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    #Other Mob sprites
    def __init__(self, imge, health, maxspeed, species):
        pygame.sprite.Sprite.__init__(self)
        self.image = imge
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = rnd.randrange (0,WIDTH)
        self.rect.y = 0
        self.speedy = rnd.randrange(2,maxspeed)
        self.speedx = rnd.randrange(2,maxspeed)
        self.type = species
##        self.speedx = 2
##        self.speedy = 2
        self.health = health
        
    def move_towards_player(self, player):
        #Figures out a normalized vectort for the player and mob
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dx != 0 or dy != 0:
            dx = dx / dist
            dy = dy /dist
            xdir = dx * self.speedx
            ydir = dy * self.speedy
            self.rect.x += dx * self.speedx
            self.rect.y += dy * self.speedy
        

class Bullet(pygame.sprite.Sprite):
    # Sprite for bullets and weapons
    def __init__(self, x, y, direction, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.direction = direction
        self.speedy = 50
        self.speedx = 50
        self.damage = damage
        
    def update(self):
        # Sends bullet moving in direction of last movement of player
        if self.direction == 'left':
           self.rect.x += -(self.speedx)
        if self.direction == "right":
            self.rect.x += (self.speedx)
        if self.direction == "up":
           self.rect.y += -(self.speedy)  
        if self.direction == "down":
           self.rect.y += self.speedy
        # kill the bullet when it leaves screen
        if self.rect.x > 1000 or self.rect.x < 0 or self.rect.y > 800 or self.rect.y < 0:
            self.kill()

class Item(pygame.sprite.Sprite):
    # Sprite for all pickable items
    def __init__(self, x, y, image, Type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(self.image, (40,40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.rect.centerx = x
        self.type = Type
    def picked_up(self):
        self.kill()
    
        

# End of Classes

"""VERSION 2 OF GAME RUNNING """

def main_game(WINDOW):

    #LOADING ALL ASSETS AND RESETTING DATA
    #Load all game graphics
    background = pygame.image.load('img/Background.jpg')
    background_rect = background.get_rect()
    items = pygame.sprite.Group()
    mainPlayer = Player()
    all_sprites.add(mainPlayer)
    #Player Inventory
    inventory = {"pistol": False, "smg": False, "rifle" : False, "combatrifle" : False, "coins" : False}

    # Other constants
    score = 0
    lives_remaining = 5
    hit_time = 0
    current_weapon = 0
    wave_num = 1
    text_wavenum = 1
    spawn_num = 5
    mobsleft = 5
    pistol_exist = False
    smg_exist = False
    rifle_exist = False
    combat_exist = False
    do_once = True
    do_once1 = True
    do_once2 = True
    do_once3 = True
    ammo_spawn_timer = 1500
    medspawn = 0
    maxspeed = 6
    spawn = True
    healthd = 1
    # Timeout/Knockback constants
    knockback_pistol = 0
    knockback_smg = 0
    knockback_rifle = 0
    knockback_combat = 0
    # Ammo Constants
    smg_ammo = 35
    rifle_ammo = 30
    combat_ammo = 20

    # Zombie image idle scaled
    zombie_idle = pygame.image.load("img/zombie_idle_d.png").convert()
    zombie_idle = pygame.transform.scale(zombie_idle, (52,52))
    boss1_sprite = pygame.image.load("img/boss1.png").convert()
##    ouch = pygame.image.load('img\ouch.jpeg')
    # LOADING ALL ASSETS AND RESETTING DATA DONE
    
    #TEST WAVE OF 20 ZOMBIES
    ##for i in range(spawn_num):
    ##    m = Mob(zombie_idle, 2)
    ##    all_sprites.add(m)
    ##    mobs.add(m)
    ##    wave_num == 0

    

    running = True  # Check if Running
    while running:     # Main Program Loop
        # Keep loop running at right speed
        clock.tick(FPS)

        #Get keystate of all keys
        keystate = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # EQUIPPING PISTOL
                    current_weapon = 1
                if event.key == pygame.K_2: # EQUIPPING SMG
                    current_weapon = 2
                if event.key == pygame.K_3: # EQUIPPING RIFLE
                    current_weapon = 3
                if event.key == pygame.K_4: # EQUIPPING COMBAT RIFLE
                    current_weapon = 4
                
            if keystate[pygame.K_SPACE]:   #WHEN GUN IS SHOT
                if inventory["pistol"] and current_weapon == 1 and knockback_pistol == 0:
                    pygame.mixer.Sound.play(fire_sound)
                    mainPlayer.shoot(1)
                    knockback_pistol = 30
                    
                if inventory["smg"] and current_weapon == 2 and knockback_smg == 0 and smg_ammo != 0:
                    pygame.mixer.Sound.play(fire_sound)
                    mainPlayer.shoot(1)
                    knockback_smg = 2
                    smg_ammo -= 1

                if inventory["rifle"] and current_weapon == 3 and knockback_rifle == 0 and rifle_ammo != 0:
                    pygame.mixer.Sound.play(fire_sound)
                    mainPlayer.shoot(2)
                    knockback_rifle = 10
                    rifle_ammo -= 1

                if inventory["combatrifle"] and current_weapon == 4 and knockback_combat == 0 and combat_ammo != 0:
                    pygame.mixer.Sound.play(fire_sound)
                    mainPlayer.shoot(4)
                    knockback_combat = 15
                    combat_ammo -= 1

            if keystate[pygame.K_m]:
                running = pause_menu(WINDOW,score, wave_num, stats_font)

        #Checks how long since player was last hit
        if hit_time != 0:
            hit_time -= 2


        #Spawn in enemies and weapons
        if spawn:
            mobsleft = spawn_num
            for i in range(spawn_num):
                m = Mob(zombie_idle, healthd, maxspeed,"zombie")
                all_sprites.add(m)
                mobs.add(m)
            spawn = False
            if wave_num == 1:
                pistol = Item(500,500, pistol_image, "pistol")
                all_sprites.add(pistol)
                weapons_items.add(pistol)
            elif wave_num == 3:
                smg_exist = True
                smg = Item(400,300, smg_image, "smg")
                all_sprites.add(smg)
                weapons_items.add(smg)
            elif wave_num == 6:
                rifle_exist = True
                rifle = Item(600,600, rifle_image, "rifle")
                all_sprites.add(rifle)
                weapons_items.add(rifle)
            elif wave_num == 10:
                m = Mob(boss1_sprite, 15, 6, "squidboss")
                all_sprites.add(m)
                mobs.add(m)
            elif wave_num == 12:
                combat_exist = True
                combatrifle = Item(800,600, combat_image, "combatrifle")
                all_sprites.add(combatrifle)
                weapons_items.add(combatrifle)

        if mobsleft == 0:
            wave_num += 1
            spawn = True
            if wave_num % 5 == 0 and wave_num % 2 != 0: # Health increase by 1
                healthd += 1
            elif wave_num % 2 == 0 and wave_num % 5 != 0:   # Spawn num increase by 2
                spawn_num += 2
            if wave_num % 12 == 0:
                maxspeed += 1

        # check if mob is hit by player bullet
        for mob in mobs:
            for bullet in bullets:
                if pygame.sprite.collide_rect(mob, bullet):
                    mob.health -= bullet.damage
                    bullet.kill()
                    
            if mob.health <= 0:
                mob.kill()
                mobsleft -= 1
                score += 100


        #Spawn in ammo and medkits at random at random
        
        if ammo_spawn_timer <= 0:
            ammo_spawn_timer = 1000
            x = rnd.randrange(0,3)
            if x == 0:
                s = Item(rnd.randrange(0, WIDTH), rnd.randrange(0, HEIGHT), s_ammo_sprite, "smgammo")
                all_sprites.add(s)
                items.add(s)

            if x == 1:
                r = Item(rnd.randrange(0, WIDTH), rnd.randrange(0, HEIGHT), r_ammo_sprite, "rifleammo")
                all_sprites.add(r)
                items.add(r)
            if x == 2:
                cr = Item(rnd.randrange(0, WIDTH), rnd.randrange(0, HEIGHT), r_ammo_sprite, "crifleammo")
                all_sprites.add(cr)
                items.add(cr)
                
        if medspawn == 2018:
            medspawn = 0 
            medkit = Item(rnd.randrange(0, WIDTH), rnd.randrange(0, HEIGHT), medkit_image, "medkit")
            all_sprites.add(medkit)
            items.add(medkit)
        medspawn += 1 
        
        #Update
        all_sprites.update()
        for mob in mobs:
            mob.move_towards_player(mainPlayer)
        #Knockback/Timeout for weapons
        if knockback_pistol > 0:
            knockback_pistol -= 1
        if knockback_smg > 0:
            knockback_smg -= 1
        if knockback_rifle > 0:
            knockback_rifle -= 1
        if knockback_combat > 0:
            knockback_combat -= 1
            
        # check to see if collision
        hits = pygame.sprite.spritecollide(mainPlayer, mobs, False)
        for i in hits:
            if i and hit_time == 0:
                lives_remaining -= 1
                hit_time = 100 
                
        # Check if dead
        if lives_remaining == 0:
            death_screen(WINDOW, score, wave_num, name_input, stats_font)
         #check if gun item is near player
        if pygame.sprite.collide_rect(mainPlayer, pistol):
            inventory["pistol"] = True
            pistol.picked_up()
        if smg_exist:
            if pygame.sprite.collide_rect(mainPlayer, smg):
                inventory["smg"] = True
                smg.picked_up()
        if rifle_exist:
            if pygame.sprite.collide_rect(mainPlayer, rifle):
                inventory["rifle"] = True
                rifle.picked_up()
        if combat_exist:
            if pygame.sprite.collide_rect(mainPlayer, combatrifle):
                inventory["combatrifle"] = True
                combatrifle.picked_up()
            

        # check if other types of items collides with player
        for item in items:
            if pygame.sprite.collide_rect(mainPlayer, item):
                if item.type == "smgammo":
                    smg_ammo += 35
                    item.picked_up()
                if item.type == "rifleammo":
                    rifle_ammo += 30
                    item.picked_up()
                if item.type == "crifleammo":
                    combat_ammo += 20
                    item.picked_up()
                if item.type == "medkit" and lives_remaining <= 8: 
                    lives_remaining += 1
                    item.picked_up()
                
        

        #Draw/Render
        WINDOW.fill(WHITE)
        WINDOW.blit(background, background_rect)
        all_sprites.draw(WINDOW)

        #Show score and lives remaining
        if current_weapon == 1 and inventory["pistol"]:
            pistol_text = score_lives_font.render("PISTOL EQUIPPED" , True, (0,0,0))
            WINDOW.blit(pistol_text, (30,95))
            pistol_text2 = score_lives_font.render("AMMO: INFINITE" , True, (0,0,0))
            WINDOW.blit(pistol_text2, (700,65))
        if current_weapon == 2 and inventory["smg"]:
            smg_text = score_lives_font.render("SMG EQUIPPED" , True, (0,0,0))
            WINDOW.blit(smg_text, (30,95))
            smg_text2 = score_lives_font.render(("AMMO: "+str(smg_ammo)) , True, (0,0,0))
            WINDOW.blit(smg_text2, (700,65))
        if current_weapon == 3 and inventory["rifle"]:
            rifle_text = score_lives_font.render("RIFLE EQUIPPED" , True, (0,0,0))
            WINDOW.blit(rifle_text, (30,95))
            rifle_text2 = score_lives_font.render(("AMMO: "+str(rifle_ammo)) , True, (0,0,0))
            WINDOW.blit(rifle_text2, (700,65))
        if current_weapon == 4 and inventory["combatrifle"]:
            crifle_text = score_lives_font.render("COMBAT RIFLE EQUIPPED" , True, (0,0,0))
            WINDOW.blit(crifle_text, (30,95))
            crifle_text2 = score_lives_font.render(("AMMO: "+str(combat_ammo)) , True, (0,0,0))
            WINDOW.blit(crifle_text2, (700,65))


        # SHOW HUD ELEMENTS
        temp_waveenemies = "WAVE: {} | Enemies Remaining: {}".format(str(wave_num), str(mobsleft))      
        temp_score = "Score: "+ str(score)
        temp_lives = "Lives: "+ str(lives_remaining)
        score_text = score_lives_font.render(temp_score, True, (0,0,0))
        lives_text = score_lives_font.render(temp_lives, True, (0,0,0))
        waveenemies_text = score_lives_font.render(temp_waveenemies, True, (0,0,0))
        WINDOW.blit(score_text, (30,30))
        WINDOW.blit(lives_text, (30,65))
        WINDOW.blit(waveenemies_text, (600,30))

        
        ammo_spawn_timer -= 1
        
        #After doing everything/ Update
        pygame.display.flip()
        
def button(img,x,y , xdist, ydist, action = None):
    """
    Creates a button that is interactive
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < xdist + x and y < mouse[1] < ydist + y:
        WINDOW.blit(img, (x,y))
        if click[0] == 1 and action != None:
            time.sleep(1)
            if action == 'resume':
                return 1
            for sprite in all_sprites:
                sprite.kill()
            pygame.mixer.music.stop()
            action(WINDOW)
        
    else:
        WINDOW.blit(img, (x,y))
    


def game_intro(WINDOW):
    """
    Game Main Menu Loop
    """
    print('game intro')
    
    intro = True
    background = pygame.image.load('img/titlescreen.jpg')
    background = pygame.transform.scale(background, (1000,800))
    background_rect = background.get_rect()
    title = pygame.image.load('img/title.png')
    start_campaign = pygame.image.load('img/startcampaign.png')
    quitbutton = pygame.image.load('img/QuitGame.png')
    instructionbutton = pygame.image.load('img/instructions.png')
    pygame.mixer.music.play(50)

    # Main Loop beginning
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #MAIN MENU BACKGROUND
        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)
        WINDOW.blit(title, (275,38))

        button(instructionbutton, 100,400, 200, 50, instructions)
        button(quitbutton, 100, 500, 200, 50, exit_game)
        button(start_campaign, 100, 300, 200, 50, main_game)
        pygame.display.flip()  #Update screen

def exit_game(window):
    """
    EXITS PYGAME AND PROGRAM
    """
    pygame.quit()
    quit()

def pause_menu(WINDOW, score, wave_num, font):
    """
    Pause Menu screen
    """
    
    screen = True
    menubutton = pygame.image.load('img/MainMenu.png')
    pausedtext = pygame.image.load('img/game_paused.png')
    resume = pygame.image.load('img/resume.png')
    quitbutton = pygame.image.load('img/QuitGame.png')
    stats = pygame.image.load('img/stats.png')
    
    while screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
    #MAIN MENU BACKGROUND
        WINDOW.fill((159, 168, 183))
        WINDOW.blit(pausedtext, (250, 100))

        temp_text = "Score : {}   |   Wave : {}".format(str(score), str(wave_num))
        out_text = font.render(temp_text, True, (255,255,255))
        WINDOW.blit(out_text, (320,350))
        WINDOW.blit(stats, (360,200))
    
    # Buttons
        button(menubutton, 100, 500, 200, 50, game_intro)
        out = button(resume, 400,500,200,50, 'resume')
        button(quitbutton, 700, 500, 200, 50, exit_game)

    # Check if exit pause menu
        if out == 1:
            return True
            
        pygame.display.flip()  #Update screen
    
    
    
def death_screen(WINDOW, score, wave_num, player_name, font):
    """
    Death screen menu
    """
    screen = True

    # Highscore writing and reading
    f = open('highscore.txt','a')
    f.write( '\n' + "player: " + player_name + " " + "score: " + str(score) + " " + "wave: " + str(wave_num))
    f.close()


    
    background = pygame.image.load('img/death.jpg')
    background = pygame.transform.scale(background, (1000,800))
    background_rect = background.get_rect()
    menubutton = pygame.image.load('img/MainMenu.png')
    quitbutton = pygame.image.load('img/QuitGame.png')
    restartbutton = pygame.image.load('img/RestartGame.png')
    stats = pygame.image.load('img/stats.png')
    pygame.mixer.Sound.play(death_sound)
        
    # Main Loop beginning
    while screen:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
         #MAIN MENU BACKGROUND
         WINDOW.fill(BLACK)
         WINDOW.blit(background, background_rect)

         #Stats
         temp_text = "Score : {}   |   Wave : {}".format(str(score), str(wave_num))
         out_text = font.render(temp_text, True, (255,255,255))
         WINDOW.blit(out_text, (320,200))
         WINDOW.blit(stats, (360,50))
         # Buttons
         button(menubutton, 100, 600, 200, 50, game_intro)
         button(restartbutton, 400, 600, 200, 50, main_game)
         button(quitbutton, 700, 600, 200, 50, exit_game)
         pygame.display.flip()  #Update screen

def instructions(window):
    """
    Instruction Screen
    """
    screen = True
    background = pygame.image.load('img/instruction_slide.png')
    background_rect = background.get_rect()
    menubutton = pygame.image.load('img/MainMenu.png')
                      
    # Main Loop Beginning
    while screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        WINDOW.fill(BLACK)
        WINDOW.blit(background, background_rect)
        button(menubutton,450, 600, 200, 50, game_intro)
        pygame.display.flip() # Update screen
    
         
game_intro(WINDOW)





    
