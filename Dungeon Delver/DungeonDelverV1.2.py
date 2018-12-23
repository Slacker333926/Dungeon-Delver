#Throughout this whole program, some code is oddly placed and grouped, so just follow the comments
#To avoid confusion, the 'Player' class is the knight

#THIS IS ALL THE STUFF BEING LOADED BEFORE THE MENU SCREEN
#Load modules
import pygame
import sys
from pygame.locals import *
from Player import Player
from enemy import Enemy
from Key import Key
from enemy2 import Enemy2
from enemy3 import Enemy3
from wizard import wizard
pygame.init()

#Set screen dimensions
screen = pygame.display.set_mode((1000, 652))

#Load backgrounds
background = pygame.image.load("images/citybackground.png").convert_alpha();
background2 = pygame.image.load("images/castle2.jpg").convert_alpha();
background3 = pygame.image.load("images/castle1.jpeg").convert_alpha();
background4 = pygame.image.load("images/castle4.jpeg").convert_alpha();
backgroundWin = pygame.image.load("images/win.png").convert_alpha();
backgroundLose = pygame.image.load("images/lose.png").convert_alpha();
screen.blit(background, (0, 0))

#Set window title and font
pygame.display.set_caption('Dungeon Delver (version 1.2)')
font = pygame.font.SysFont(None, 36)

#Load characters
player = Player()
wizard = wizard()

#Load enemies and key off-screen
enemy = Enemy(2000, 2000)
enemy2 = Enemy2(2000, 2000)
enemy3 = Enemy3(2000, 2000)
key = Key(2000, 2000)

#Create groups
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)
enemy_group.add(enemy2)
enemy_group.add(enemy3)

all_group = pygame.sprite.Group()
all_group.add(player)
all_group.add(wizard)
all_group.add(enemy)
all_group.add(key)
all_group.add(enemy2)
all_group.add(enemy3)

#Set score
main_clock = pygame.time.Clock()

#Disable directional controls in menu
direction = -1

#Show score
time = 0
font = pygame.font.SysFont(None, 30)
time_text = font.render('score: %s' %int(time), 1, (255, 255, 255))
time_rect = time_text.get_rect()
time_rect.topleft = (50, 50)

#Show lives
lives = 3
lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
lives_rect = lives_text.get_rect()
lives_rect.topleft = (50, 100)

#Load the menu screen and make it unable to be played like the rest of the levels
state = 1
jump_state = 0
jump_timer = 0
grounded = False

#Start the actual game
while True:
    for event in pygame.event.get():

        #Quit the game if the game has been quitted(lol)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #Load key presses and collisions(very oddly grouped code)
    keys = pygame.key.get_pressed()
    collide_list2 = pygame.sprite.spritecollide(player, enemy_group, False, collided = None)
    collide_list = pygame.sprite.spritecollide(wizard, enemy_group, False, collided = None)

    #Lose lives and score if the player hits an enemy
    if len(collide_list) > 0:
        wizard.subtract_lives()
        time -= 100
        lives -= 1
        for enemies in collide_list:
            enemies.collision()
    if len(collide_list2) > 0:
        player.subtract_lives()
        time -= 100
        lives -= 1
        for enemies1 in collide_list2:
            enemies1.collision()

    #From now on, most of the code is the same apart from "if state ==", so you dont have to read everything
    #I will write new states in all caps
    #For some reason, the first area code comes before the main menu code, so don't get confused

    #STATE 0 IS FIRST BATTLE AREA IN FOREST
    if state == 0:

        #Set directional controls
        if keys[K_a]:
            direction = 1
        elif keys[K_d]:
            direction = 0
        elif keys[K_w]:
            direction = 2
        elif keys[K_s]:
            direction = 3
        else:
            direction = -1

        #Show timer and background
        main_clock.tick(60)
        time -= .015
        time_text = font.render('score: %s' % int(time), 1, (255, 255, 255))
        screen.blit(background2, (0, 0))
        screen.blit(time_text, time_rect)

        #Show message
        instructions_rect.topleft = (200, 50)
        instructions = font.render('You start with three lives, and lose one when you hit a zombie.  Be careful!', 1, (255, 255, 255))
        screen.blit(instructions, instructions_rect)

        #Show lives
        lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
        screen.blit(lives_text, lives_rect)

        #Update player and enemy movements
        player.update(direction)
        wizard.update(direction)
        enemy.update()
        enemy2.update()
        enemy3.update()
        all_group.clear(screen, background2)
        all_group.draw(screen)

        #Return to main menu if player losses all lives
        if player.get_lives() <= 0:
            state = 5
        elif wizard.get_lives() <= 0:
            state = 5

        #If the player passes the edge of the screen, move onto the next area and reset enemies and player
        if player.rect.x >= 1000:
            player.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 500
            enemy.rect.x = 500
            enemy.rect.y = 100
            state = 2
            time += 100
        elif wizard.rect.x >= 1000:
            wizard.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 100
            enemy.rect.x = 500
            enemy.rect.y = 100
            state = 2
            time += 100

        #Update the screen
        pygame.display.update()

    #STATE 1 IS MAIN MENU
    elif state == 1:

        #Render background image
        screen.blit(background, (0, 0))

        #Create input for character selection and set character lives, then move onto state 0
        if keys[K_m]:
            player.set_lives(3)
            player.rect.x = -2000
            wizard.rect.x = 0
            enemy.rect.x = 500
            enemy.rect.y = 100
            enemy2.rect.x = 2000
            enemy3.rect.x = 2000
            key.rect.x = 2000
            time = 0
            wizard.set_lives(3)
            state = 0

        elif keys[K_k]:
            enemy.rect.x = 500
            enemy.rect.y = 100
            enemy2.rect.x = 2000
            enemy3.rect.x = 2000
            key.rect.x = 2000
            wizard.rect.x = -2000
            player.rect.x = 0
            time = 0
            wizard.set_lives(3)
            player.set_lives(3)
            state = 0

        #Show instructions

        instructions = font.render('Welcome to Dungeon Delver!  Press M to Play as a Wizard or K to Play as a Knight.', 1, (0, 0, 0))
        instructions_rect = instructions.get_rect()
        instructions_rect.topleft = (50, 50)
        screen.blit(instructions, instructions_rect)


        #Update the screen
        pygame.display.update()

    #STATE 2 IS OUTSIDE THE DUNGEON WITH THE KEY
    elif state == 2:

        #Set location of the key
        key.rect.x = 700
        key.rect.y = 100

        #Set directional controls
        if keys[K_a]:
            direction = 1
        elif keys[K_d]:
            direction = 0
        elif keys[K_w]:
            direction = 2
        elif keys[K_s]:
            direction = 4
            wizard.update(direction)
            player.update(direction)
        else:
            direction = -1

        #Set score and background
        main_clock.tick(60)
        time -= .015
        time_text = font.render('score: %s' % int(time), 1, (255, 255, 255))
        screen.blit(background3, (0, 0))
        screen.blit(time_text, time_rect)

        #Show lives
        lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
        screen.blit(lives_text, lives_rect)

        #Show message
        instructions_rect.topleft = (200, 50)
        instructions = font.render('Get the key!', 1, (255, 255, 255))
        screen.blit(instructions, instructions_rect)

        #Update movements
        player.update(direction)
        wizard.update(direction)
        enemy.update()
        enemy2.update()
        enemy3.update()
        all_group.clear(screen, background3)
        all_group.draw(screen)

        #If the player hits the key, then the next level begins
        if player.rect.x >= 700 and player.rect.x <= 800 and player.rect.y >= 100 and player.rect.y <= 125:
            wizard.rect.x = -2000
            player.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 500
            enemy.rect.x = 500
            enemy.rect.y = 100
            enemy3.rect.x = 700
            enemy3.rect.y = 100
            state = 3
            time += 200
        elif wizard.rect.x >= 700 and wizard.rect.x <= 800 and wizard.rect.y >= 100 and wizard.rect.y <= 125:
            player.rect.x = -2000
            wizard.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 500
            enemy.rect.x = 500
            enemy.rect.y = 100
            enemy3.rect.x = 700
            enemy3.rect.y = 100
            state = 3
            time += 200

        #If the player loses lives, the game ends
        if player.get_lives() <= 0:
            state = 5
        elif wizard.get_lives() <= 0:
            state = 5

        #Update screen
        pygame.display.update()

    #STATE 3 IS THE FINAL LEVEL, THE DUNGEON
    elif state == 3:

        #Remove the key from the last level
        key.rect.x = 2000
        key.rect.y = 2000

        #If the player reaches the end of the level, the game ends
        if player.rect.x >= 1000:
            state = 4
            time += 300
        elif wizard.rect.x >= 1000:
            state = 4
            time += 300

        #Set directional controls
        if keys[K_a]:
                direction = 1
        elif keys[K_d]:
                direction = 0
        elif keys[K_w]:
                direction = 2
        elif keys[K_s]:
                direction = 4
                player.update(direction)
                wizard.update(direction)
        else:
            direction = -1

        #Set score and background
        main_clock.tick(60)
        time -= .015
        time_text = font.render('score: %s' % int(time), 1, (255, 255, 255))
        screen.blit(background4, (0, 0))
        screen.blit(time_text, time_rect)

        #Show lives
        lives_text = font.render('lives: %s' %int(lives), 1, (255, 255, 255))
        screen.blit(lives_text, lives_rect)

        #Show message
        instructions_rect.topleft = (200, 50)
        instructions = font.render('You got the key and opened the doors to the dungeon.', 1, (255, 255, 255))
        screen.blit(instructions, instructions_rect)

        #Update movements
        player.update(direction)
        wizard.update(direction)
        enemy.update()
        enemy2.update()
        enemy3.update()

        #Removing this code makes the third level invisible, but I still don't know why it's here
        all_group.clear(screen, background4)
        all_group.draw(screen)

        #If the player loses too many lives, the game ends
        if player.get_lives() <= 0:
            state = 5
        elif wizard.get_lives() <= 0:
            state = 5

        #Update screen
        pygame.display.update()

    #STATE 4 IS THE WIN SCREEN
    if state == 4:

        #Render background image
        instructions = font.render('You beat the game!  Your score was ' + str(time) + '.  Want to play again?  Press "y".', 1, (0, 0, 0))
        instructions_rect = time_rect
        screen.blit(backgroundWin, (0, 0))
        screen.blit(instructions, instructions_rect)

        #Return to the main menu after hitting y
        if keys[K_y]:
            state = 1

        #Update screen
        pygame.display.update()

    #STATE 5 IS THE LOSE SCREEN
    if state == 5:
        #Render background image
        instructions = font.render('You lost!  Your score was ' + str(time) + '.  Want to play again?  Press "y".', 1, (0, 0, 0))
        instructions_rect = time_rect
        screen.blit(backgroundLose, (0, 0))
        screen.blit(instructions, instructions_rect)

        #Return to the main menu after hitting y
        if keys[K_y]:
            state = 1

        #Update screen
        pygame.display.update()

#And that's it!  I want to add some attacks and new classes, maybe even potions and multiple adventures.