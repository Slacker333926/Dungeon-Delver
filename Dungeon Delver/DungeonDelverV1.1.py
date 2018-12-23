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
screen.blit(background, (0, 0))

#Set window title and font
pygame.display.set_caption('Dungeon Delver (version 1.1)')
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

#Set clock
main_clock = pygame.time.Clock()

#Disable directional controls(I think...)
direction = -1

#Show timer
time = 0
font = pygame.font.SysFont(None, 30)
time_text = font.render('time: %s' %int(time), 1, (0, 0, 0))
time_rect = time_text.get_rect()
time_rect.topleft = (50, 50)

#Load the menu screen and make it unable to be played like the rest of the levels
state = 1
jump_state = 0
jump_timer = 0
grounded = False

#THIS IS WHERE THE GAME STARTS
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

    #Lose lives if the player hits an enemy
    if len(collide_list) > 0:
        wizard.subtract_lives()
        for enemies in collide_list:
            enemies.collision()
    if len(collide_list2) > 0:
        player.subtract_lives()
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

        #Set timer for state
        main_clock.tick(60)
        time += .015
        time_text = font.render('time: %s' % int(time), 1, (0, 0, 0))

        #Render background image
        screen.blit(background2, (0, 0))

        #Show timer
        screen.blit(time_text, time_rect)

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
            print("You've lost all three of your lives!  Care to play again?")
            state = 1
        elif wizard.get_lives() <= 0:
            print("You've lost all three of your lives!  Care to play again?")
            state = 1

        #If the player passes the edge of the screen, move onto the next area and reset enemies and player
        if player.rect.x >= 1000:
            player.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 500
            enemy.rect.x = 500
            enemy.rect.y = 100
            state = 2
        elif wizard.rect.x >= 1000:
            wizard.rect.x = 0
            enemy2.rect.x = 300
            enemy2.rect.y = 100
            enemy.rect.x = 500
            enemy.rect.y = 100
            state = 2

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
            #Tell player that they have 3 lives
            print("You start with three lives, and lose one when you hit a zombie.  Be careful, wizard!")

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
            #Tell player that they have 3 lives
            print("You start with three lives, and lose one when you hit a zombie.  Be careful, knight!")


        #Show instructions and, for some reason, the background is loaded again
        instructions = font.render('Welcome to Dungeon Delver!  Press M to Play as a Wizard or K to Play as a Knight.', 1, (0, 0, 0))
        instructions_rect = time_rect
        screen.blit(background, (0, 0))
        screen.blit(instructions, instructions_rect)

        #Update the screen
        pygame.display.update()

        #This was a failed score screen that we may be able to revive
        '''
    elif state == 1:
        if keys[K_RETURN]:
            state = 5
        instructions = font.render('Press ENTER to Play Again.', 1, (0, 0, 0))
        instructions_rect = score_rect
        screen.blit(background, (0, 0))
        screen.blit(instructions, instructions_rect)
        '''

    #STATE 2 IS OUTSIDE THE DUNGEON WITH THE KEY
    elif state == 2:

        #Print 'get the key!' at the start of the level
        if player.rect.x == 0:
            print("Get the key!")
        elif wizard.rect.x == 0:
            print("Get the key!")

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

        #Load timer
        main_clock.tick(60)
        time += .015
        time_text = font.render('time: %s' % int(time), 1, (0, 0, 0))
        screen.blit(background3, (0, 0))
        screen.blit(time_text, time_rect)

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
            print("You got the key and opened the doors to the dungeon.")
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
            print("You got the key and opened the doors to the dungeon.")

        #If the player loses lives, the game ends
        if player.get_lives() <= 0:
            print("You've lost all three of your lives!  Care to play again?")
            state = 1
        elif wizard.get_lives() <= 0:
            print("You've lost all three of your lives!  Care to play again?")
            state = 1

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
        elif wizard.rect.x >= 1000:
            state = 4

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

        #Set the timer
        main_clock.tick(60)
        time += .015
        time_text = font.render('time: %s' % int(time), 1, (0, 0, 0))
        screen.blit(background4, (0, 0))
        screen.blit(time_text, time_rect)

        #Update movements
        player.update(direction)
        wizard.update(direction)
        enemy.update()
        enemy2.update()
        enemy3.update()

        #?
        all_group.clear(screen, background4)
        all_group.draw(screen)

        #If the player loses too many lives, the game ends
        if player.get_lives() <= 0:
            print("You've lost all three of your lives!  Care to play again?")
            state = 1
        elif wizard.get_lives() <= 0:
            print("You've lost all three of your lives!  Care to play again?")
            state = 1

        #Update screen
        pygame.display.update()

        #STATE 4 IS JUST A TRANSITION BACK TO THE MAIN MENU ONCE THE PLAYER HAS WON
        if state == 4:

            #Notify the player that they have won
            print ("You won!  Want to play again?")

            #Return to the main menu
            state = 1

#And that's it!  I want to add some attacks and new classes, maybe even potions and multiple adventures.